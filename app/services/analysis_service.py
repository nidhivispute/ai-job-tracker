import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.match_analysis import MatchAnalysis
from app.models.user import User
from app.schemas.analysis import MatchAnalysisCreate
from app.services.job_service import get_job_by_id
from app.services.resume_service import get_resume_by_id


SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "fastapi",
    "django",
    "flask",
    "react",
    "node.js",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "git",
    "github",
    "rest api",
    "graphql",
    "microservices",
    "celery",
    "rabbitmq",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "ci/cd",
    "unit testing",
    "pytest",
    "html",
    "css",
]


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> set[str]:
    normalized_text = normalize_text(text)
    found_skills: set[str] = set()

    for skill in SKILLS:
        if skill in normalized_text:
            found_skills.add(skill)

    return found_skills


def generate_suggestions(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return [
            "Your resume covers the main skills found in this job description.",
            "Consider adding measurable achievements to make your resume stronger.",
        ]

    suggestions = []

    for skill in missing_skills[:5]:
        suggestions.append(
            f"Consider adding a project, bullet point, or experience that demonstrates {skill}."
        )

    suggestions.append(
        "Tailor your resume summary and project descriptions to match the job requirements more closely."
    )

    return suggestions


def create_match_analysis(
    db: Session,
    current_user: User,
    analysis_data: MatchAnalysisCreate,
) -> MatchAnalysis:
    resume = get_resume_by_id(db, current_user, analysis_data.resume_id)
    job = get_job_by_id(db, current_user, analysis_data.job_id)

    if not resume.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume does not have extracted text",
        )

    if not job.job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job does not have a description to analyze",
        )

    resume_skills = extract_skills(resume.extracted_text)
    job_skills = extract_skills(job.job_description)

    if not job_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No recognizable skills found in the job description",
        )

    strong_matches = sorted(resume_skills.intersection(job_skills))
    missing_skills = sorted(job_skills.difference(resume_skills))

    match_score = round((len(strong_matches) / len(job_skills)) * 100)

    resume_suggestions = generate_suggestions(missing_skills)

    analysis = MatchAnalysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        match_score=match_score,
        strong_matches=strong_matches,
        missing_skills=missing_skills,
        resume_suggestions=resume_suggestions,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def get_match_analyses(db: Session, current_user: User) -> list[MatchAnalysis]:
    return (
        db.query(MatchAnalysis)
        .filter(MatchAnalysis.user_id == current_user.id)
        .order_by(MatchAnalysis.created_at.desc())
        .all()
    )


def get_match_analysis_by_id(
    db: Session,
    current_user: User,
    analysis_id: int,
) -> MatchAnalysis:
    analysis = (
        db.query(MatchAnalysis)
        .filter(
            MatchAnalysis.id == analysis_id,
            MatchAnalysis.user_id == current_user.id,
        )
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    return analysis