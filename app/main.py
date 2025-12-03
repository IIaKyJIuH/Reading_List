# main.py
from fastapi import FastAPI

from app.db import ENGINE

from .models.base import BaseModel
from .routers import items, tags, users

BaseModel.metadata.create_all(bind=ENGINE)

app = FastAPI(title="Reading List API")

app.include_router(users.router)
app.include_router(items.router)
app.include_router(tags.router)
