from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate


def create_job(db: Session, current_user: User, job_data: JobCreate) -> Job:
    job = Job(
        user_id=current_user.id,
        company_name=job_data.company_name,
        job_title=job_data.job_title,
        job_description=job_data.job_description,
        job_url=job_data.job_url,
        location=job_data.location,
        status=job_data.status,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs(db: Session, current_user: User) -> list[Job]:
    return (
        db.query(Job)
        .filter(Job.user_id == current_user.id)
        .order_by(Job.created_at.desc())
        .all()
    )


def get_job_by_id(db: Session, current_user: User, job_id: int) -> Job:
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user.id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


def update_job(
    db: Session,
    current_user: User,
    job_id: int,
    job_data: JobUpdate,
) -> Job:
    job = get_job_by_id(db, current_user, job_id)

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(db: Session, current_user: User, job_id: int) -> None:
    job = get_job_by_id(db, current_user, job_id)

    db.delete(job)
    db.commit()