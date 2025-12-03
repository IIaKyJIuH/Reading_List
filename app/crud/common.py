from typing import TypeVar

from pydantic import BaseModel as BaseScheme
from sqlalchemy.orm import Session

from ..models.base import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)
TScheme = TypeVar("TScheme", bound=BaseScheme)


def update(db: Session, model: TModel, data: TScheme) -> TModel:
    for field, value in data.model_dump().items():
        setattr(model, field, value)
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model: TModel) -> None:
    db.delete(model)
    db.commit()
