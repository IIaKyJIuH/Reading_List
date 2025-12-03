from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routers.auth import get_user_id

from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=schemas.TagOut)
def create_tag(tag: schemas.TagCreate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    return crud.tag.create(db, user_id, tag)


@router.get("/", response_model=list[schemas.TagOut])
def list_tags(user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    return crud.tag.read_many(db, user_id)


@router.patch("/{tag_id}", response_model=schemas.TagOut)
def update_tag(
    tag_id: int, data: schemas.TagUpdate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)
):
    tag = crud.tag.read(db, user_id, tag_id)
    if not tag or tag.user_id != user_id:
        raise HTTPException(status_code=404, detail="Тег не найден")
    return crud.common.update(db, tag, data)


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    tag = crud.tag.read(db, user_id, tag_id)
    if not tag or tag.user_id != user_id:
        raise HTTPException(status_code=404, detail="Тег не найден")
    crud.common.delete(db, tag)
    return {"detail": "Тег удалён"}
