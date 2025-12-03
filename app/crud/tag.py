from sqlalchemy.orm import Session

from .. import models, schemas


def create(db: Session, user_id: int, data: schemas.TagCreate) -> models.Tag:
    tag = models.Tag(user_id=user_id, **data.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def read(db: Session, user_id: int, tag_id: int) -> models.Tag | None:
    return db.query(models.Tag).filter(models.Tag.user_id == user_id, models.Tag.id == tag_id).first()


def read_many(db: Session, user_id: int) -> list[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.user_id == user_id).all()
