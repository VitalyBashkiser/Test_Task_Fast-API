from fastapi import FastAPI

from user.router import router as user_router
from post.router import router as post_router
from db.session import engine
from user import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
