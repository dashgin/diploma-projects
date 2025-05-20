from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import QuizAssignment, StudentAttempt
    from .class_model import StudyClass, StudyClassEnrollment
    from .item import Item
    from .quiz import Quiz


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    role: str = Field(default="student", max_length=10)  # student or educator


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, TimestampMixin, table=True):
    __tablename__ = "auth_user"

    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    last_login: datetime | None = Field(default=None)
    date_joined: datetime = Field(default_factory=datetime.utcnow)

    # Keep existing relationship for compatibility
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)

    # New relationships from db.md
    created_quizzes: list["Quiz"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    managed_classes: list["StudyClass"] = Relationship(
        back_populates="educator",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    enrolled_classes: list["StudyClassEnrollment"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    quiz_attempts: list["StudentAttempt"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    assigned_quizzes: list["QuizAssignment"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
