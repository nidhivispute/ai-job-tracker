from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.jobs import router as jobs_router
from app.api.resumes import router as resumes_router


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Job Tracker API is running"
    }


router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
router.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])