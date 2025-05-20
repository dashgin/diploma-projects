from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import StudentResponse
    from .quiz import KnowledgeArea


class FeedbackBase(SQLModel):
    """Base model for AI feedback schema"""

    response_id: int
    feedback_text: str
    error_type: str | None = Field(default="", max_length=50)
    confidence_score: float | None = Field(default=None)
    feedback_content: dict[str, Any] = Field(default_factory=dict)
    ai_metadata: dict[str, Any] | None = None


class FeedbackCreate(FeedbackBase):
    """Schema for AI feedback creation"""

    pass


class FeedbackRead(FeedbackBase):
    """Response schema for AI feedback"""

    id: int


class AIFeedback(TimestampMixin, FeedbackBase, table=True):
    """AI-generated feedback for student responses"""

    __tablename__ = "ai_feedback"

    id: int = Field(default=None, primary_key=True)
    response_id: int = Field(
        foreign_key="student_response.id", ondelete="CASCADE", unique=True
    )
    # JSONB fields
    feedback_content: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB)
    ai_metadata: dict[str, Any] | None = Field(default=None, sa_type=JSONB)

    # Relationships
    response: "StudentResponse" = Relationship(back_populates="feedback")
    resources: list["LearningResource"] = Relationship(
        back_populates="feedback",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ResourceBase(SQLModel):
    """Base model for learning resource schema"""

    feedback_id: int
    title: str = Field(max_length=200)
    description: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=200)
    resource_type: str = Field(max_length=50)
    area_id: int | None = Field(default=None)
    relevance_score: float | None = Field(default=None)


class ResourceCreate(ResourceBase):
    """Schema for learning resource creation"""

    pass


class ResourceRead(ResourceBase):
    """Response schema for learning resources"""

    id: int


class LearningResource(TimestampMixin, ResourceBase, table=True):
    """Learning resources recommended based on AI feedback"""

    __tablename__ = "learning_resource"

    id: int = Field(default=None, primary_key=True)
    feedback_id: int = Field(foreign_key="ai_feedback.id", ondelete="CASCADE")
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )

    # Relationships
    feedback: AIFeedback = Relationship(back_populates="resources")
    area: Optional["KnowledgeArea"] = Relationship(back_populates="resources")
