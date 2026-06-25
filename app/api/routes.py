from fastapi import APIRouter

from app.api.analysis import router as analysis_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
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
router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])