from sqlalchemy.orm import Session
from varname import nameof

from app.enums import ItemSorting, KindEnum, PriorityEnum, StatusEnum

from .. import models, schemas


def _map_tag_ids_to_tags(db: Session, user_id: int, tag_ids: list[int]) -> list[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.id.in_(tag_ids), models.Tag.user_id == user_id).all()


def create(db: Session, user_id: int, data: schemas.ItemCreate) -> models.Item:
    serialized = data.model_dump()
    tags = []
    if data.tag_ids:
        tags = _map_tag_ids_to_tags(db, user_id, data.tag_ids)
        serialized.pop(nameof(schemas.ItemUpdate().tag_ids))
    item = models.Item(user_id=user_id, tags=tags, **serialized)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def read(db: Session, item_id: int) -> models.Item | None:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def read_many(
    db: Session,
    user_id: int,
    *,
    status: StatusEnum | None = None,
    kind: KindEnum | None = None,
    priority: PriorityEnum | None = None,
    tag_ids: list[int] | None = None,
    title_substr: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 20,
    offset: int = 0,
    order_by: ItemSorting = ItemSorting.CREATED_AT,
    order_by_asc: bool = True,
) -> list[models.Item]:
    q = db.query(models.Item).filter(models.Item.user_id == user_id)

    if status:
        q = q.filter(models.Item.status == status)
    if kind:
        q = q.filter(models.Item.kind == kind)
    if priority:
        q = q.filter(models.Item.priority == priority)
    if title_substr:
        q = q.filter(models.Item.title.ilike(f"%{title_substr}%"))
    if date_from:
        q = q.filter(models.Item.created_at >= date_from)
    if date_to:
        q = q.filter(models.Item.created_at <= date_to)
    if tag_ids:
        q = q.join(models.Item.tags).filter(models.Tag.id.in_(tag_ids))

    col = getattr(models.Item, order_by, models.Item.created_at)
    if not order_by_asc:
        col = col.desc()
    q = q.order_by(col)

    return q.offset(offset).limit(limit).all()


def update(db: Session, item: models.Item, data: schemas.ItemUpdate) -> models.Item:
    for field, value in data.model_dump(exclude={nameof(schemas.ItemUpdate().tag_ids)}).items():
        setattr(item, field, value)
    if data.tag_ids:
        tags = _map_tag_ids_to_tags(db, item.user_id, data.tag_ids)
        item.tags = tags
    db.commit()
    db.refresh(item)
    return item


def update_tags(db: Session, item: models.Item, tag_ids: list[int]) -> models.Item:
    tags = _map_tag_ids_to_tags(db, item.user_id, tag_ids)
    item.tags = tags
    db.commit()
    db.refresh(item)
    return item
