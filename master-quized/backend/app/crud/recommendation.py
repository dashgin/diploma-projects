from sqlmodel import Session, select

from app.models import LearningResource, ResourceCreate


def create_recommendation(
    *, session: Session, resource_in: ResourceCreate
) -> LearningResource:
    """Create a new learning resource recommendation"""
    resource = LearningResource.model_validate(resource_in)
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


def get_recommendation(
    *, session: Session, resource_id: int
) -> LearningResource | None:
    """Get a specific resource recommendation by ID"""
    return session.get(LearningResource, resource_id)


def get_recommendations_by_feedback(
    *, session: Session, feedback_id: int, skip: int = 0, limit: int = 100
) -> list[LearningResource]:
    """Get resource recommendations for a specific feedback"""
    statement = select(LearningResource).where(
        LearningResource.feedback_id == feedback_id
    )
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()
