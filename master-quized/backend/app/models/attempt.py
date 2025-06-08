from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .class_model import StudyClass
    from .feedback import AIFeedback
    from .quiz import QuestionOption, Quiz, QuizQuestion
    from .user import User

# Import UserPublic for the AttemptRead model
from .user import UserPublic


class AssignmentBase(SQLModel):
    """Base model for quiz assignment schema"""

    quiz_id: int
    student_id: int
    class_id: int | None = Field(default=None)
    due_date: datetime | None = Field(default=None)


class AssignmentCreate(AssignmentBase):
    """Schema for quiz assignment creation"""

    pass


class AssignmentRead(AssignmentBase):
    """Response schema for quiz assignments"""

    id: int


class QuizAssignment(TimestampMixin, AssignmentBase, table=True):
    """Assignment of a quiz to a student"""

    __tablename__ = "quiz_assignment"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    student_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    class_id: int | None = Field(
        default=None, foreign_key="study_class.id", ondelete="CASCADE"
    )

    # Relationships
    quiz: "Quiz" = Relationship(back_populates="assignments")
    student: "User" = Relationship(back_populates="assigned_quizzes")
    study_class: Optional["StudyClass"] = Relationship(back_populates="assignments")
    attempts: list["StudentAttempt"] = Relationship(
        back_populates="assignment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class AttemptBase(SQLModel):
    """Base model for student attempt schema"""

    student_id: int
    quiz_id: int
    assignment_id: int | None = Field(default=None)
    is_completed: bool = Field(default=False)


class AttemptCreate(AttemptBase):
    """Schema for student attempt creation"""

    pass


class AttemptCreateApiSchema(SQLModel):
    """Schema for student attempt creation from API"""

    quiz_id: int
    assignment_id: int | None = Field(default=None)
    is_completed: bool = Field(default=False)


class AttemptUpdate(SQLModel):
    """Schema for student attempt update"""

    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    score: float | None = Field(default=None)
    is_completed: bool | None = Field(default=None)


class AttemptRead(AttemptBase):
    """Response schema for student attempts"""

    id: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    score: float | None = None
    student: UserPublic


class StudentAttempt(TimestampMixin, AttemptBase, table=True):
    """Record of a student attempting a quiz"""

    __tablename__ = "student_attempt"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    assignment_id: int | None = Field(
        default=None, foreign_key="quiz_assignment.id", ondelete="CASCADE"
    )
    student_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")
    quiz_id: int = Field(foreign_key="quiz.id", ondelete="CASCADE")
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    score: float | None = Field(default=None)

    # Relationships
    assignment: Optional["QuizAssignment"] = Relationship(back_populates="attempts")
    student: "User" = Relationship(back_populates="quiz_attempts")
    quiz: "Quiz" = Relationship(back_populates="attempts")
    responses: list["StudentResponse"] = Relationship(
        back_populates="attempt",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ResponseBase(SQLModel):
    """Base model for student response schema"""

    attempt_id: int
    question_id: int
    answer_text: str
    is_correct: bool | None = Field(default=None)
    selected_option_id: int | None = Field(default=None)


class ResponseCreate(ResponseBase):
    """Schema for student response creation"""

    pass


class ResponseRead(ResponseBase):
    """Response schema for student responses"""

    id: int


class OptionData(SQLModel):
    """Option data for response details"""

    id: int
    text: str
    is_correct: bool


class QuestionData(SQLModel):
    """Question data for response details"""

    id: int
    text: str
    question_type: str
    model_answer: str | None = None
    options: list[OptionData] | None = None


class AnswerData(SQLModel):
    """Answer data for response details"""

    type: str
    answer: str | dict
    is_correct: bool
    created_at: datetime


class EnhancedResponse(SQLModel):
    """Detailed response with question and answer information"""

    id: int
    question: QuestionData
    answer: AnswerData
    explanation: str | None = None


class AttemptSummary(SQLModel):
    """Summary data for an attempt"""

    id: int
    is_completed: bool
    score: float
    total_questions: int
    correct_answers: int


class AttemptResponsesDetailed(SQLModel):
    """Complete attempt with detailed responses"""

    attempt: AttemptSummary
    responses: list[EnhancedResponse]


class StudentResponse(TimestampMixin, ResponseBase, table=True):
    """Student's answer to a question in a quiz attempt"""

    __tablename__ = "student_response"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key="student_attempt.id", ondelete="CASCADE")
    question_id: int = Field(foreign_key="quiz_question.id", ondelete="CASCADE")
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


# Pagination models
class AssignmentsPublic(SQLModel):
    """Paginated assignments response"""

    data: list[AssignmentRead]
    count: int


class AttemptsPublic(SQLModel):
    """Paginated attempts response"""

    data: list[AttemptRead]
    count: int


class ResponsesPublic(SQLModel):
    """Paginated responses response"""

    data: list[ResponseRead]
    count: int
