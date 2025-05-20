from sqlmodel import Session, select

from app.models import Quiz, ResponseCreate, StudentAttempt, StudentResponse


def create_response(
    *, session: Session, response_in: ResponseCreate
) -> StudentResponse:
    """Create a new student response"""
    response = StudentResponse.model_validate(response_in)
    session.add(response)
    session.commit()
    session.refresh(response)
    return response


def get_response(*, session: Session, response_id: int) -> StudentResponse | None:
    """Get a specific response by ID"""
    return session.get(StudentResponse, response_id)


def get_response_with_relationships(
    *, session: Session, response_id: int
) -> tuple[StudentResponse, StudentAttempt, Quiz] | None:
    """Get response with related attempt and quiz in a single query"""
    statement = (
        select(StudentResponse, StudentAttempt, Quiz)
        .join(StudentAttempt, StudentResponse.attempt_id == StudentAttempt.id)
        .join(Quiz, StudentAttempt.quiz_id == Quiz.id)
        .where(StudentResponse.id == response_id)
    )
    result = session.exec(statement).first()
    return result


def get_responses_by_attempt(
    *, session: Session, attempt_id: int, skip: int = 0, limit: int = 100
) -> list[StudentResponse]:
    """Get responses for a specific attempt"""
    statement = select(StudentResponse).where(StudentResponse.attempt_id == attempt_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()
