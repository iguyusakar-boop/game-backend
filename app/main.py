from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.quest import Quest
from app.models.stat import UserStat
from app.models.streak import UserStreak

from app.routers.auth import router as auth_router
from app.routers.actions import router as action_router
from app.routers.quests import router as quest_router
from app.routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Game Backend API")

app.include_router(auth_router)
app.include_router(action_router)
app.include_router(quest_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Game backend is running"}