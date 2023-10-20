from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)

