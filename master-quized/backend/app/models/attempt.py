from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from .base import TimestampMixin

if TYPE_CHECKING:
    from .class_model import StudyClass
    from .feedback import AIFeedback
    from .quiz import QuestionOption, Quiz, QuizQuestion
    from .user import User


class QuizAssignment(TimestampMixin, table=True):
    """Assignment of a quiz to a student"""

    __tablename__ = "quiz_assignment"

    id: int = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    student_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    class_id: int | None = Field(
        default=None, foreign_key="study_class.id", ondelete="CASCADE"
    )
    due_date: datetime | None = Field(default=None)

    # Relationships
    quiz: "Quiz" = Relationship(back_populates="assignments")
    student: "User" = Relationship(back_populates="assigned_quizzes")
    study_class: Optional["StudyClass"] = Relationship(back_populates="assignments")
    attempts: list["StudentAttempt"] = Relationship(
        back_populates="assignment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class StudentAttempt(TimestampMixin, table=True):
    """Record of a student attempting a quiz"""

    __tablename__ = "student_attempt"

    id: int = Field(default=None, primary_key=True)
    assignment_id: int | None = Field(
        default=None, foreign_key="quiz_assignment.id", ondelete="CASCADE"
    )
    student_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    completed_at: datetime | None = Field(default=None)
    score: float | None = Field(default=None)
    is_completed: bool = Field(default=False)

    # Relationships
    assignment: Optional["QuizAssignment"] = Relationship(back_populates="attempts")
    student: "User" = Relationship(back_populates="quiz_attempts")
    quiz: "Quiz" = Relationship(back_populates="attempts")
    responses: list["StudentResponse"] = Relationship(
        back_populates="attempt",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class StudentResponse(TimestampMixin, table=True):
    """Student's answer to a question in a quiz attempt"""

    __tablename__ = "student_response"

    id: int = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key="student_attempt.id", ondelete="CASCADE")
    question_id: int = Field(foreign_key="quiz_question.id", ondelete="CASCADE")
    answer_text: str = Field()
    is_correct: bool | None = Field(default=None)
    selected_option_id: int | None = Field(
        default=None, foreign_key="question_option.id", ondelete="SET NULL"
    )

    # Relationships
    attempt: StudentAttempt = Relationship(back_populates="responses")
    question: "QuizQuestion" = Relationship(back_populates="responses")
    selected_option: Optional["QuestionOption"] = Relationship(
        back_populates="selected_in"
    )
    feedback: Optional["AIFeedback"] = Relationship(
        back_populates="response", sa_relationship_kwargs={"uselist": False}
    )
