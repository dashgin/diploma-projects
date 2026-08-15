from datetime import datetime

from sqlmodel import Session, col, select

from app.models import AttemptCreate, StudentAttempt, User


def create_attempt(*, session: Session, attempt_in: AttemptCreate) -> StudentAttempt:
    """Create a new student attempt"""
    attempt = StudentAttempt.model_validate(attempt_in)
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    # Fetch the student data for the response
    user = session.get(User, attempt.student_id)
    if user:
        attempt.student = user

    return attempt


def get_attempt(*, session: Session, attempt_id: int) -> StudentAttempt | None:
    """Get a specific attempt by ID with student data"""
    statement = (
        select(StudentAttempt, User)
        .join(User, col(StudentAttempt.student_id) == col(User.id))
        .where(StudentAttempt.id == attempt_id)
    )
    result = session.exec(statement).first()
    if result:
        attempt, user = result
        # Attach the user data to the attempt for the response model
        attempt.student = user
        return attempt
    return None


def complete_attempt(
    *, session: Session, db_attempt: StudentAttempt, score: float | None = None
) -> StudentAttempt:
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

    # Fetch the student data for the response
    user = session.get(User, db_attempt.student_id)
    if user:
        db_attempt.student = user

    return db_attempt


def get_attempts(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[StudentAttempt]:
    """Get a list of student attempts with student data"""
    statement = (
        select(StudentAttempt, User)
        .join(User, col(StudentAttempt.student_id) == col(User.id))
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()

    attempts = []
    for attempt, user in results:
        # Attach the user data to the attempt for the response model
        attempt.student = user
        attempts.append(attempt)

    return attempts


def get_user_attempts(
    *, session: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[StudentAttempt]:
    """Get attempts for a specific user with student data"""
    statement = (
        select(StudentAttempt, User)
        .join(User, col(StudentAttempt.student_id) == col(User.id))
        .where(StudentAttempt.student_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()

    attempts = []
    for attempt, user in results:
        # Attach the user data to the attempt for the response model
        attempt.student = user
        attempts.append(attempt)

    return attempts
