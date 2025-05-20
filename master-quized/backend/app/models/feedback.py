from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import StudentResponse
    from .quiz import KnowledgeArea


class AIFeedback(TimestampMixin, table=True):
    """AI-generated feedback for student responses"""

    __tablename__ = "ai_feedback"

    id: int = Field(default=None, primary_key=True)
    response_id: int = Field(
        foreign_key="student_response.id", ondelete="CASCADE", unique=True
    )
    feedback_text: str = Field()
    error_type: str | None = Field(default="", max_length=50)
    confidence_score: float | None = Field(default=None)

    # JSONB fields
    feedback_content: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB)
    ai_metadata: dict[str, Any] | None = Field(default=None, sa_type=JSONB)

    # Relationships
    response: "StudentResponse" = Relationship(back_populates="feedback")
    resources: list["LearningResource"] = Relationship(
        back_populates="feedback",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class LearningResource(TimestampMixin, table=True):
    """Learning resources recommended based on AI feedback"""

    __tablename__ = "learning_resource"

    id: int = Field(default=None, primary_key=True)
    feedback_id: int = Field(foreign_key="ai_feedback.id", ondelete="CASCADE")
    title: str = Field(max_length=200)
    description: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=200)
    resource_type: str = Field(max_length=50)
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )
    relevance_score: float | None = Field(default=None)

    # Relationships
    feedback: AIFeedback = Relationship(back_populates="resources")
    area: Optional["KnowledgeArea"] = Relationship(back_populates="resources")
