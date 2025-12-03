from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import M2M_ITEM_TAG, BaseModel

if TYPE_CHECKING:
    from .item import Item
    from .user import User


class Tag(BaseModel):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_tag_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="tags")
    items: Mapped[list["Item"]] = relationship(secondary=M2M_ITEM_TAG, back_populates="tags")
