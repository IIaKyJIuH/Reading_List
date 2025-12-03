from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routers.auth import get_user_id

from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.user.create(db, data)
    return user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.read(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не существует")
    return user


@router.patch("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int, data: schemas.UserUpdate, current_user_id: int = Depends(get_user_id), db: Session = Depends(get_db)
):
    user = crud.user.read(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_id != current_user_id or not crud.user.check_privileges(db, current_user_id):
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return crud.common.update(db, user, data)


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    user = crud.user.read(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_id != current_user_id or not crud.user.check_privileges(db, current_user_id):
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    crud.common.delete(db, user)
    return {"detail": "Пользователь удалён"}
