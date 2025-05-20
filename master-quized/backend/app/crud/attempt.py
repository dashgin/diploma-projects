from datetime import datetime
from sqlmodel import Session, select

from app.models import StudentAttempt, AttemptCreate, AttemptUpdate


def create_attempt(*, session: Session, attempt_in: AttemptCreate) -> StudentAttempt:
    """Create a new student attempt"""
    attempt = StudentAttempt.model_validate(attempt_in)
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt


def get_attempt(*, session: Session, attempt_id: int) -> StudentAttempt | None:
    """Get a specific attempt by ID"""
    return session.get(StudentAttempt, attempt_id)


def complete_attempt(*, session: Session, db_attempt: StudentAttempt, score: float | None = None) -> StudentAttempt:
    """Mark an attempt as completed"""
    update_data = {
        "is_completed": True,
        "completed_at": datetime.now(),
    }
    if score is not None:
        update_data["score"] = score
        
    db_attempt.sqlmodel_update(update_data)
    session.add(db_attempt)
    session.commit()
    session.refresh(db_attempt)
    return db_attempt


def get_attempts(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[StudentAttempt]:
    """Get a list of student attempts"""
    statement = select(StudentAttempt).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_user_attempts(
    *, session: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[StudentAttempt]:
    """Get attempts for a specific user"""
    statement = select(StudentAttempt).where(StudentAttempt.student_id == user_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all() 