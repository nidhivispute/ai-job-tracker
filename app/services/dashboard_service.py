from collections import Counter

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.match_analysis import MatchAnalysis
from app.models.resume import Resume
from app.models.user import User
from app.schemas.dashboard import DashboardStats


def get_dashboard_stats(db: Session, current_user: User) -> DashboardStats:
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    analyses = (
        db.query(MatchAnalysis)
        .filter(MatchAnalysis.user_id == current_user.id)
        .all()
    )

    jobs_by_status = Counter(job.status for job in jobs)

    if analyses:
        average_match_score = round(
            sum(analysis.match_score for analysis in analyses) / len(analyses),
            2,
        )
    else:
        average_match_score = None

    missing_skill_counter: Counter[str] = Counter()

    for analysis in analyses:
        for skill in analysis.missing_skills:
            missing_skill_counter[skill] += 1

    top_missing_skills = [
        {"skill": skill, "count": count}
        for skill, count in missing_skill_counter.most_common(5)
    ]

    return DashboardStats(
        total_jobs=len(jobs),
        jobs_by_status=dict(jobs_by_status),
        total_resumes=len(resumes),
        total_analyses=len(analyses),
        average_match_score=average_match_score,
        top_missing_skills=top_missing_skills,
    )