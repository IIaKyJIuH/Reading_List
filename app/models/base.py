from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


M2M_ITEM_TAG = Table(
    "m2m_item_tag",
    BaseModel.metadata,
    Column("item_id", ForeignKey("item.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)
