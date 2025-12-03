from fastapi import Header, HTTPException

from .. import models
from ..db import SESSION_LOCAL


def get_user_id(
    x_user_id: int = Header(alias="X-User-Id"),
) -> int:
    with SESSION_LOCAL() as db:
        user = db.query(models.User).filter(models.User.id == x_user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Несуществующий пользователь")

        return user.id
