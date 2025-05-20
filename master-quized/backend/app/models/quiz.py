from typing import TYPE_CHECKING, Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import QuizAssignment, StudentAttempt, StudentResponse
    from .feedback import LearningResource
    from .user import User


class KnowledgeArea(TimestampMixin, table=True):
    """Subject/topic category for quizzes and questions"""

    __tablename__ = "knowledge_area"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    description: str | None = Field(default=None)

    # Relationships
    quizzes: list["Quiz"] = Relationship(back_populates="area")
    questions: list["QuizQuestion"] = Relationship(back_populates="area")
    resources: list["LearningResource"] = Relationship(back_populates="area")


class Quiz(TimestampMixin, table=True):
    """Quiz containing multiple questions"""

    __tablename__ = "quiz"

    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    instructions: str | None = Field(default=None)
    creator_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )
    is_active: bool = Field(default=True)

    # Relationships
    creator: "User" = Relationship(back_populates="created_quizzes")
    area: KnowledgeArea | None = Relationship(back_populates="quizzes")
    questions: list["QuizQuestion"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    assignments: list["QuizAssignment"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    attempts: list["StudentAttempt"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class QuizQuestion(TimestampMixin, table=True):
    """Individual question within a quiz"""

    __tablename__ = "quiz_question"

    id: int = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )
    text: str = Field()
    question_type: str = Field(max_length=15)  # multiple_choice, short_answer, etc.
    order_position: int = Field(default=0)
    correct_answer: str | None = Field(default="")
    model_answer: str | None = Field(default="")

    # JSONB fields
    key_concepts: dict[str, Any] | None = Field(default=None, sa_type=JSONB)
    ai_guidance: dict[str, Any] | None = Field(default=None, sa_type=JSONB)

    # Relationships
    quiz: Quiz = Relationship(back_populates="questions")
    area: KnowledgeArea | None = Relationship(back_populates="questions")
    options: list["QuestionOption"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    responses: list["StudentResponse"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class QuestionOption(SQLModel, table=True):
    """Option for multiple-choice questions"""

    __tablename__ = "question_option"

    id: int = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="quiz_question.id", ondelete="CASCADE")
    text: str = Field(max_length=200)
    is_correct: bool = Field(default=False)
    order_position: int = Field(default=0)

    # Relationships
    question: QuizQuestion = Relationship(back_populates="options")
    selected_in: list["StudentResponse"] = Relationship(
        back_populates="selected_option",
    )
