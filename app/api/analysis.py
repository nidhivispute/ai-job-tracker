from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.analysis import MatchAnalysisCreate, MatchAnalysisRead
from app.services.analysis_service import (
    create_match_analysis,
    get_match_analyses,
    get_match_analysis_by_id,
)


router = APIRouter()


@router.post(
    "/resume-match",
    response_model=MatchAnalysisRead,
    status_code=status.HTTP_201_CREATED,
)
def analyze_resume_match(
    analysis_data: MatchAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_match_analysis(db, current_user, analysis_data)


@router.get("/", response_model=list[MatchAnalysisRead])
def list_match_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_match_analyses(db, current_user)


@router.get("/{analysis_id}", response_model=MatchAnalysisRead)
def get_single_match_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_match_analysis_by_id(db, current_user, analysis_id)