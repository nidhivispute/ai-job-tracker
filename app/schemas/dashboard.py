from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_jobs: int
    jobs_by_status: dict[str, int]
    total_resumes: int
    total_analyses: int
    average_match_score: float | None
    top_missing_skills: list[dict[str, int]]