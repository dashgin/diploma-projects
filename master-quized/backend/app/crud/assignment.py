from sqlmodel import Session, select

from app.models import QuizAssignment, AssignmentCreate


def create_assignment(*, session: Session, assignment_in: AssignmentCreate) -> QuizAssignment:
    """Create a new quiz assignment"""
    assignment = QuizAssignment.model_validate(assignment_in)
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


def get_assignment(*, session: Session, assignment_id: int) -> QuizAssignment | None:
    """Get a specific assignment by ID"""
    return session.get(QuizAssignment, assignment_id)


def get_assignments(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[QuizAssignment]:
    """Get a list of quiz assignments"""
    statement = select(QuizAssignment).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_user_assignments(
    *, session: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[QuizAssignment]:
    """Get assignments for a specific user"""
    statement = select(QuizAssignment).where(QuizAssignment.student_id == user_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all() 