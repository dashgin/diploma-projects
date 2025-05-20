from sqlmodel import SQLModel  # noqa

from .attempt import QuizAssignment, StudentAttempt, StudentResponse
from .class_model import StudyClass, StudyClassEnrollment
from .common import Message, Token, TokenPayload
from .feedback import AIFeedback, LearningResource
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

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UsersPublic",
    "UpdatePassword",
    "UserRegister",
    "NewPassword",
    "UserUpdateMe",
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
    "StudyClassEnrollment",
    # Attempt models
    "QuizAssignment",
    "StudentAttempt",
    "StudentResponse",
    # Feedback models
    "AIFeedback",
    "LearningResource",
    "TimestampMixin",
]
