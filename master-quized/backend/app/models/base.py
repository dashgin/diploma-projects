from datetime import datetime
from typing import Any

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """Mixin for adding timestamp fields to models"""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)


class JSONBMixin(SQLModel):
    """Mixin for models with JSONB fields"""

    def __init__(self, **data: Any):
        super().__init__(**data)
