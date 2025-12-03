from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.enums import ItemSorting, KindEnum, PriorityEnum, StatusEnum
from app.routers.auth import get_user_id

from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=schemas.ItemOut)
def create_item(item: schemas.ItemCreate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    return crud.create_item(db, user_id, item)


@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Item не найден")
    return item


@router.get("/", response_model=list[schemas.ItemOut])
def list_items(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
    status: StatusEnum | None = None,
    kind: KindEnum | None = None,
    priority: PriorityEnum | None = None,
    tag_ids: list[int] | None = Query(None),
    title: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 20,
    offset: int = 0,
    order_by: ItemSorting = ItemSorting.CREATED_AT,
    order_by_asc: bool = True,
):
    return crud.get_items(
        db,
        user_id,
        status=status,
        kind=kind,
        priority=priority,
        tag_ids=tag_ids,
        title_substr=title,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        order_by=order_by,
        order_by_asc=order_by_asc,
    )


@router.patch("/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int, data: schemas.ItemUpdate, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)
):
    item = crud.get_item(db, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Item не найден")
    return crud.update_item(db, item, data)


@router.delete("/{item_id}")
def delete_item(item_id: int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Item не найден")
    crud.delete_item(db, item)
    return {"detail": "Item удалён"}


@router.post("/{item_id}/tags", response_model=schemas.ItemOut)
def set_tags(item_id: int, tag_ids: list[int], user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.set_item_tags(db, item, tag_ids)
