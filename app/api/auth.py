from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.user_stats import UserStats
from app.models.streak import UserStreak


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    username: str


@router.post("/auth/login")
def login_or_create_user(data: LoginRequest, db: Session = Depends(get_db)):
    username = data.username.strip()

    if not username:
        return {"error": "Username cannot be empty"}

    user = db.query(User).filter(User.username == username).first()

    if not user:
        user = User(
            username=username,
            level=1,
            xp=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        stats = UserStats(user_id=user.id)
        db.add(stats)

        streak = UserStreak(user_id=user.id)
        db.add(streak)

        db.commit()

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }