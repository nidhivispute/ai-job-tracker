from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job_service import (
    create_job,
    delete_job,
    get_job_by_id,
    get_jobs,
    update_job,
)


router = APIRouter()


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_new_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_job(db, current_user, job_data)


@router.get("/", response_model=list[JobRead])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_jobs(db, current_user)


@router.get("/{job_id}", response_model=JobRead)
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_job_by_id(db, current_user, job_id)


@router.patch("/{job_id}", response_model=JobRead)
def edit_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_job(db, current_user, job_id, job_data)


@router.delete("/{job_id}")
def remove_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_job(db, current_user, job_id)

    return {
        "message": "Job deleted successfully"
    }