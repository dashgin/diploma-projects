from sqlmodel import SQLModel  # noqa

from .common import Message, Token, TokenPayload
from .feedback import AIFeedback, LearningResource, FeedbackCreate, FeedbackRead, ResourceCreate, ResourceRead
from .item import Item, ItemCreate, ItemPatch, ItemRead
from .quiz import (
    Quiz,
    QuizCreate,
    QuizUpdate,
    QuizRead,
    QuizQuestion,
    QuestionCreate,
    QuestionUpdate,
    QuestionRead,
    QuestionOption,
    OptionCreate,
    OptionUpdate,
    OptionRead,
    KnowledgeArea,
    KnowledgeAreaRead
)
from .user import (
    NewPassword,
    UpdatePassword,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
    UserRegister,
    UsersPublic,
    UserUpdateMe,
)
from .base import TimestampMixin
from .attempt import (
    QuizAssignment,
    AssignmentCreate,
    AssignmentRead,
    StudentAttempt,
    AttemptCreate,
    AttemptUpdate,
    AttemptRead,
    StudentResponse,
    ResponseCreate,
    ResponseRead
)
from .class_model import StudyClass

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UsersPublic",
    "UpdatePassword",
    "NewPassword",
    "UserRegister",
    "UserUpdateMe",
    # Item models
    "Item",
    "ItemCreate",
    "ItemPatch",
    "ItemRead",
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
