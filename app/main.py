from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://web-production-6df2f.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(action_router)
app.include_router(quest_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Game backend is running"}