from datetime import datetime

from pydantic import BaseModel


class MatchAnalysisCreate(BaseModel):
    resume_id: int
    job_id: int


class MatchAnalysisRead(BaseModel):
    id: int
    user_id: int
    resume_id: int
    job_id: int
    match_score: int
    strong_matches: list[str]
    missing_skills: list[str]
    resume_suggestions: list[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }