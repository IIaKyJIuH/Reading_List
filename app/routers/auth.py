from fastapi import Header, HTTPException
from sqlalchemy import select

from .. import models
from ..db import SESSION_LOCAL


def get_user_id(
    x_user_id: int = Header(alias="X-User-Id"),
) -> int:
    with SESSION_LOCAL() as db:
        user = db.scalar(select(models.User).where(models.User.id == x_user_id))

        if not user:
            raise HTTPException(status_code=401, detail="Несуществующий пользователь")

        return user.id
