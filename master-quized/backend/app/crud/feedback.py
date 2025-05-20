from sqlmodel import Session, select

from app.models import AIFeedback, FeedbackCreate


def create_feedback(*, session: Session, feedback_in: FeedbackCreate) -> AIFeedback:
    """Create a new AI feedback"""
    feedback = AIFeedback.model_validate(feedback_in)
    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


def get_feedback(*, session: Session, feedback_id: int) -> AIFeedback | None:
    """Get a specific feedback by ID"""
    return session.get(AIFeedback, feedback_id)


def get_feedback_by_response(
    *, session: Session, response_id: int
) -> AIFeedback | None:
    """Get feedback for a specific response"""
    statement = select(AIFeedback).where(AIFeedback.response_id == response_id)
    return session.exec(statement).first() 