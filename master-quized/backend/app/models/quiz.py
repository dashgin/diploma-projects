from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import QuizAssignment, StudentAttempt, StudentResponse
    from .feedback import LearningResource
    from .user import User


class KnowledgeAreaBase(SQLModel):
    """Base model for knowledge area schema"""
    name: str = Field(max_length=100)
    description: str | None = Field(default=None)


class KnowledgeAreaRead(KnowledgeAreaBase):
    """Response schema for knowledge areas"""
    id: int


class KnowledgeArea(TimestampMixin, KnowledgeAreaBase, table=True):
    """Subject/topic category for quizzes and questions"""

    __tablename__ = "knowledge_area"

    id: int = Field(default=None, primary_key=True)

    # Relationships
    quizzes: list["Quiz"] = Relationship(back_populates="area")
    questions: list["QuizQuestion"] = Relationship(back_populates="area")
    resources: list["LearningResource"] = Relationship(back_populates="area")


class QuizBase(SQLModel):
    """Base model for quiz schema"""
    title: str = Field(max_length=200)
    instructions: str | None = Field(default=None)
    area_id: int | None = Field(default=None)
    is_active: bool = Field(default=True)


class QuizCreate(QuizBase):
    """Schema for quiz creation"""
    pass


class QuizUpdate(SQLModel):
    """Schema for quiz update"""
    title: str | None = Field(default=None, max_length=200)
    instructions: str | None = Field(default=None)
    area_id: int | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class QuizRead(QuizBase):
    """Response schema for quizzes"""
    id: int
    creator_id: int


class Quiz(TimestampMixin, QuizBase, table=True):
    """Quiz containing multiple questions"""

    __tablename__ = "quiz"

    id: int = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )

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


class QuestionBase(SQLModel):
    """Base model for question schema"""
    quiz_id: int
    area_id: int | None = Field(default=None)
    text: str
    question_type: str = Field(max_length=15)  # multiple_choice, short_answer, etc.
    order_position: int = Field(default=0)
    correct_answer: str | None = Field(default="")
    model_answer: str | None = Field(default="")
    key_concepts: dict[str, Any] | None = None
    ai_guidance: dict[str, Any] | None = None


class QuestionCreate(QuestionBase):
    """Schema for question creation"""
    pass


class QuestionUpdate(SQLModel):
    """Schema for question update"""
    area_id: int | None = Field(default=None)
    text: str | None = Field(default=None)
    question_type: str | None = Field(default=None, max_length=15)
    order_position: int | None = Field(default=None)
    correct_answer: str | None = Field(default=None)
    model_answer: str | None = Field(default=None)
    key_concepts: dict[str, Any] | None = Field(default=None)
    ai_guidance: dict[str, Any] | None = Field(default=None)


class QuestionRead(QuestionBase):
    """Response schema for questions"""
    id: int


class QuizQuestion(TimestampMixin, QuestionBase, table=True):
    """Individual question within a quiz"""

    __tablename__ = "quiz_question"

    id: int = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    area_id: int | None = Field(
        default=None, foreign_key="knowledge_area.id", ondelete="SET NULL"
    )
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


class OptionBase(SQLModel):
    """Base model for question option schema"""
    question_id: int
    text: str = Field(max_length=200)
    is_correct: bool = Field(default=False)
    order_position: int = Field(default=0)


class OptionCreate(OptionBase):
    """Schema for option creation"""
    pass


class OptionUpdate(SQLModel):
    """Schema for option update"""
    text: str | None = Field(default=None, max_length=200)
    is_correct: bool | None = Field(default=None)
    order_position: int | None = Field(default=None)


class OptionRead(OptionBase):
    """Response schema for options"""
    id: int


class QuestionOption(OptionBase, table=True):
    """Option for multiple-choice questions"""

    __tablename__ = "question_option"

    id: int = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="quiz_question.id", ondelete="CASCADE")

    # Relationships
    question: QuizQuestion = Relationship(back_populates="options")
    selected_in: list["StudentResponse"] = Relationship(
        back_populates="selected_option",
    )
