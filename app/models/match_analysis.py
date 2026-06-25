from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MatchAnalysis(Base):
    __tablename__ = "match_analysis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    match_score: Mapped[int] = mapped_column(Integer, nullable=False)
    strong_matches: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    missing_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    resume_suggestions: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )