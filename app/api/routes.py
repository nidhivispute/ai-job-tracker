from fastapi import APIRouter

from app.api.auth import router as auth_router


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Job Tracker API is running"
    }


router.include_router(auth_router, prefix="/auth", tags=["Auth"])