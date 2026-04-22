from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.user_stats import UserStats
from app.models.streak import UserStreak
from app.models.quest import Quest
from app.engines.level_engine import get_level_progress

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/{user_id}/profile")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()

    return {
        "user_id": user.id,
        "username": user.username,
        "xp": user.xp,
        "level": user.level,
        "streak": streak.current_streak if streak else 0,
        "stats": {
            "strength": stats.strength if stats else 0,
            "discipline": stats.discipline if stats else 0,
            "focus": stats.focus if stats else 0,
            "energy": stats.energy if stats else 0
        }
    }


@router.get("/users/{user_id}/dashboard")
def get_user_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    quests = db.query(Quest).filter(Quest.user_id == user_id).all()

    level, xp, level_min, level_max = get_level_progress(user.xp)

    xp_in_level = xp - level_min
    xp_range = level_max - level_min
    progress_percent = int((xp_in_level / xp_range) * 100) if xp_range > 0 else 0

    return {
        "profile": {
            "user_id": user.id,
            "username": user.username,
            "xp": user.xp,
            "level": level,
            "streak": streak.current_streak if streak else 0,
            "level_progress": {
                "current_xp": xp,
                "level_min_xp": level_min,
                "level_max_xp": level_max,
                "xp_to_next_level": level_max - xp,
                "progress_percent": progress_percent
            }
        },
        "stats": {
            "strength": stats.strength if stats else 0,
            "discipline": stats.discipline if stats else 0,
            "focus": stats.focus if stats else 0,
            "energy": stats.energy if stats else 0
        },
        "today_quests": [
            {
                "id": q.id,
                "title": q.title,
                "action_type": q.action_type,
                "target_value": q.target_value,
                "progress_value": q.progress_value,
                "reward_xp": q.reward_xp,
                "is_completed": q.is_completed
            }
            for q in quests
        ]
    }