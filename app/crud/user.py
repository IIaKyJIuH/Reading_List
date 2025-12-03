from sqlalchemy.orm import Session

from .. import models, schemas


def check_privileges(db: Session, user_id: int) -> bool:
    return bool(db.query(models.User).filter(models.User.id == user_id).first())  # Здесь должна быть проверка роли


def create(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()
