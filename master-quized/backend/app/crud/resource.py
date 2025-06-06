from sqlmodel import Session

from app.models import LearningResource, ResourceCreate


def create_resource(
    *, session: Session, resource_in: ResourceCreate
) -> LearningResource:
    """Create a new learning resource"""
    resource = LearningResource.model_validate(resource_in)
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


def get_resources_by_feedback(
    *, session: Session, feedback_id: int
) -> list[LearningResource]:
    """Get resources for a specific feedback"""
    return (
        session.query(LearningResource)
        .filter(LearningResource.feedback_id == feedback_id)
        .all()
    )
