from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import get_settings

_settings = get_settings()
ENGINE = create_engine(_settings.DATABASE_URL, pool_pre_ping=True)
SESSION_LOCAL = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)


def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
