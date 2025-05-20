from sqlmodel import SQLModel  # noqa

from .attempt import (
    AssignmentCreate,
    AssignmentRead,
    AttemptCreate,
    AttemptRead,
    AttemptUpdate,
    QuizAssignment,
    ResponseCreate,
    ResponseRead,
    StudentAttempt,
    StudentResponse,
)
from .base import TimestampMixin
from .class_model import StudyClass, StudyClassEnrollment
from .common import Message, Token, TokenPayload
from .feedback import (
    AIFeedback,
    FeedbackCreate,
    FeedbackRead,
    LearningResource,
    ResourceCreate,
    ResourceRead,
)
from .item import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from .quiz import (
    KnowledgeArea,
    KnowledgeAreaRead,
    OptionCreate,
    OptionRead,
    OptionUpdate,
    QuestionCreate,
    QuestionOption,
    QuestionRead,
    QuestionUpdate,
    Quiz,
    QuizCreate,
    QuizQuestion,
    QuizRead,
    QuizUpdate,
)
from .user import (
    NewPassword,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserPublic",
    "UsersPublic",
    "UserUpdate",
    "UpdatePassword",
    "NewPassword",
    "UserRegister",
    "UserUpdateMe",
    # Item models
    "Item",
    "ItemCreate",
    "ItemPublic",
    "ItemsPublic",
    "ItemUpdate",
    "Message",
    "Token",
    "TokenPayload",
    # Quiz models
    "Quiz",
    "QuizCreate",
    "QuizUpdate",
    "QuizRead",
    "QuizQuestion",
    "QuestionCreate",
    "QuestionUpdate",
    "QuestionRead",
    "QuestionOption",
    "OptionCreate",
    "OptionUpdate",
    "OptionRead",
    "KnowledgeArea",
    "KnowledgeAreaRead",
    # Class models
    "StudyClass",
    "StudyClassEnrollment",
    # Attempt models
    "QuizAssignment",
    "AssignmentCreate",
    "AssignmentRead",
    "StudentAttempt",
    "AttemptCreate",
    "AttemptUpdate",
    "AttemptRead",
    "StudentResponse",
    "ResponseCreate",
    "ResponseRead",
    # Feedback models
    "AIFeedback",
    "FeedbackCreate",
    "FeedbackRead",
    "LearningResource",
    "ResourceCreate",
    "ResourceRead",
    "TimestampMixin",
]
