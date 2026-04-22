from fastapi import APIRouter
from app.database import SessionLocal
from app.models.quest import Quest
from app.engines.quest_engine import ensure_daily_quests

router = APIRouter(prefix="/quests", tags=["quests"])

@router.get("/today/{user_id}")
def get_today_quests(user_id: int):
    db = SessionLocal()
    try:
        ensure_daily_quests(db, user_id)

        quests = db.query(Quest).filter(Quest.user_id == user_id).all()

        return [
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
    finally:
        db.close()