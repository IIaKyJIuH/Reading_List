from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routers.auth import get_user_id

from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=schemas.TagOut)
def create_tag(tag: schemas.TagCreate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    return crud.create_tag(db, user_id, tag)


@router.get("/", response_model=list[schemas.TagOut])
def list_tags(user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    return crud.get_tags(db, user_id)


@router.patch("/", response_model=schemas.TagOut)
def update_tag(data: schemas.TagUpdate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    tag = crud.get_tag(db, user_id, data.id)
    if not tag or tag.user_id != user_id:
        raise HTTPException(status_code=404, detail="Тэг не найден")
    return crud.update_tag(db, tag, data)
