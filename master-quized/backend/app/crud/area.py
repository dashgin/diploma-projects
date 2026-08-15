from sqlmodel import Session, select

from app.models import KnowledgeArea


def get_areas(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[KnowledgeArea]:
    """Get a list of knowledge areas"""
    statement = select(KnowledgeArea).offset(skip).limit(limit)
    return session.exec(statement).all()
