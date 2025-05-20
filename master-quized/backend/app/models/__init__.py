from sqlmodel import SQLModel  # type: ignore

from .attempt import QuizAssignment, StudentAttempt, StudentResponse
from .class_model import StudyClass, StudyClassEnrollment
from .common import Message, Token, TokenPayload
from .feedback import AIFeedback, LearningResource
from .item import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from .quiz import KnowledgeArea, QuestionOption, Quiz, QuizQuestion
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
    "UserUpdate",
    "UserPublic",
    "UsersPublic",
    "UpdatePassword",
    "UserRegister",
    "NewPassword",
    "UserUpdateMe",
    "Item",
    "ItemCreate",
    "ItemUpdate",
    "ItemPublic",
    "ItemsPublic",
    "Message",
    "Token",
    "TokenPayload",
    # Quiz models
    "KnowledgeArea",
    "Quiz",
    "QuizQuestion",
    "QuestionOption",
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
]
