from sqlalchemy import delete

from app import models
from app.db import SESSION_LOCAL
from app.enums import KindEnum, PriorityEnum, StatusEnum


def init_db():
    with SESSION_LOCAL() as db:
        # Чистим старые данные
        db.execute(delete(models.Item))
        db.execute(delete(models.Tag))
        db.execute(delete(models.User))
        db.execute(delete(models.M2M_ITEM_TAG))
        db.commit()

        # Добавляем пользователей
        user1 = models.User(email="user1@test.com", display_name="User1")
        user2 = models.User(email="user2@test.com", display_name="User2")
        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        # Добавляем теги
        tag_python = models.Tag(user_id=user1.id, name="python")
        tag_fastapi = models.Tag(user_id=user1.id, name="fastapi")
        tag_ml = models.Tag(user_id=user1.id, name="ml")
        db.add_all([tag_python, tag_fastapi, tag_ml])
        db.commit()
        db.refresh(tag_python)
        db.refresh(tag_fastapi)
        db.refresh(tag_ml)

        # Добавляем items
        items = [
            models.Item(
                user_id=user1.id,
                title="FastAPI Guide",
                kind=KindEnum.BOOK,
                status=StatusEnum.READING,
                priority=PriorityEnum.HIGH,
                notes="Read for API design",
                tags=[tag_python, tag_fastapi],
            ),
            models.Item(
                user_id=user1.id,
                title="SQLAlchemy 2.0 Docs",
                kind=KindEnum.ARTICLE,
                status=StatusEnum.PLANNED,
                priority=PriorityEnum.NORMAL,
                notes=None,
                tags=[tag_python],
            ),
            models.Item(
                user_id=user1.id,
                title="ML in Production",
                kind=KindEnum.BOOK,
                status=StatusEnum.DONE,
                priority=PriorityEnum.LOW,
                notes="Good overview",
                tags=[tag_ml],
            ),
            models.Item(
                user_id=user2.id,
                title="sqlite3 Internals",
                kind=KindEnum.BOOK,
                status=StatusEnum.READING,
                priority=PriorityEnum.HIGH,
                notes=None,
            ),
            models.Item(
                user_id=user2.id,
                title="Pydantic 2.0 Docs",
                kind=KindEnum.ARTICLE,
                status=StatusEnum.READING,
                priority=PriorityEnum.LOW,
                notes="Updates",
                tags=[tag_python],
            ),
            models.Item(
                user_id=user2.id,
                title="Async Python",
                kind=KindEnum.ARTICLE,
                status=StatusEnum.PLANNED,
                priority=PriorityEnum.NORMAL,
                notes="",
            ),
        ]
        db.add_all(items)
        db.commit()

        print("Тестовые данные добавлены")


if __name__ == "__main__":
    init_db()
