from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.resume import ResumeRead
from app.services.resume_service import (
    delete_resume,
    get_resume_by_id,
    get_resumes,
    upload_resume,
)


router = APIRouter()


@router.post("/upload", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
def upload_new_resume(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_resume(db, current_user, file, title)


@router.get("/", response_model=list[ResumeRead])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_resumes(db, current_user)


@router.get("/{resume_id}", response_model=ResumeRead)
def get_single_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_resume_by_id(db, current_user, resume_id)


@router.delete("/{resume_id}")
def remove_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_resume(db, current_user, resume_id)

    return {
        "message": "Resume deleted successfully"
    }