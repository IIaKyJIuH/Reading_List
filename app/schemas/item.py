from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.enums import KindEnum, PriorityEnum, StatusEnum

from .tag import TagOut


class ItemBase(BaseModel):
    title: str
    kind: KindEnum
    status: StatusEnum
    priority: PriorityEnum
    notes: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] | None = None


class ItemCreate(ItemBase):
    tag_ids: list[int] = Field(default_factory=list)


class ItemUpdate(BaseModel):
    title: str | None = None
    kind: KindEnum | None = None
    status: StatusEnum | None = None
    priority: PriorityEnum | None = None
    notes: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] | None = None
    tag_ids: list[int] | None = Field(default=None)


class ItemOut(ItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
