from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums import KindEnum, PriorityEnum, StatusEnum
from .base import M2M_ITEM_TAG, BaseModel

if TYPE_CHECKING:
    from .tag import Tag
    from .user import User


class Item(BaseModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    kind: Mapped[KindEnum] = mapped_column(Enum(KindEnum))
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum))
    priority: Mapped[PriorityEnum] = mapped_column(Enum(PriorityEnum))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="items")
    tags: Mapped[list["Tag"]] = relationship(secondary=M2M_ITEM_TAG, back_populates="items")
