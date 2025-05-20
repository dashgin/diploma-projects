from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

if TYPE_CHECKING:
    from .attempt import QuizAssignment
    from .user import User


class StudyClass(TimestampMixin, table=True):
    """Class/group of students managed by an educator"""

    __tablename__ = "study_class"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    educator_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")

    # Relationships
    educator: "User" = Relationship(back_populates="managed_classes")
    enrollments: list["StudyClassEnrollment"] = Relationship(
        back_populates="study_class",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    assignments: list["QuizAssignment"] = Relationship(
        back_populates="study_class",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class StudyClassEnrollment(SQLModel, table=True):
    """Many-to-many relationship between students and classes"""

    __tablename__ = "study_class_enrollment"

    id: int = Field(default=None, primary_key=True)
    class_id: int = Field(foreign_key="study_class.id", ondelete="CASCADE")
    student_id: int = Field(foreign_key="auth_user.id", ondelete="CASCADE")

    # Relationships
    study_class: StudyClass = Relationship(back_populates="enrollments")
    student: "User" = Relationship(back_populates="enrolled_classes")
