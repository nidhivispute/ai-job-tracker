import uuid
from pathlib import Path

import fitz
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User


UPLOAD_DIR = Path("uploads/resumes")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts: list[str] = []

        for page in document:
            text_parts.append(page.get_text())

        document.close()

        return "\n".join(text_parts).strip()

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from PDF",
        ) from exc


def upload_resume(
    db: Session,
    current_user: User,
    file: UploadFile,
    title: str | None = None,
) -> Resume:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    file_bytes = file.file.read()
    file_size = len(file_bytes)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be 5 MB or less",
        )

    extracted_text = extract_text_from_pdf(file_bytes)

    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text could be extracted from this PDF",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    original_filename = file.filename or "resume.pdf"
    stored_filename = f"{uuid.uuid4()}.pdf"
    file_path = UPLOAD_DIR / stored_filename

    with open(file_path, "wb") as output_file:
        output_file.write(file_bytes)

    resume = Resume(
        user_id=current_user.id,
        title=title or original_filename,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        content_type=file.content_type,
        file_size=file_size,
        extracted_text=extracted_text,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resumes(db: Session, current_user: User) -> list[Resume]:
    return (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_resume_by_id(db: Session, current_user: User, resume_id: int) -> Resume:
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


def delete_resume(db: Session, current_user: User, resume_id: int) -> None:
    resume = get_resume_by_id(db, current_user, resume_id)

    file_path = Path(resume.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(resume)
    db.commit()