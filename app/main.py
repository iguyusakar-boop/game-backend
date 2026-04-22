from fastapi import FastAPI
from app.database import Base, engine

from app.routers.actions import router as actions_router
from app.routers.quests import router as quests_router
from app.api.user import router as user_router
from app.api.view import router as view_router
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(actions_router)
app.include_router(quests_router)
app.include_router(user_router)
app.include_router(view_router)
app.include_router(auth_router)