from datetime import date
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.stat import UserStat
from app.models.quest import Quest
from app.models.streak import UserStreak

from app.engines.level_engine import get_level_info
from app.engines.quest_engine import ensure_daily_quests


def get_user_dashboard_data(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    stats = db.query(UserStat).filter(UserStat.user_id == user_id).first()
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()

    if not stats:
        stats = UserStat(
            user_id=user_id,
            strength=0,
            discipline=0,
            focus=0,
            energy=0
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)

    if not streak:
        streak = UserStreak(
            user_id=user_id,
            current_streak=0,
            last_action_date=None
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)

    ensure_daily_quests(db, user_id)

    today = date.today()
    today_quests = db.query(Quest).filter(
        Quest.user_id == user_id,
        Quest.quest_date == today
    ).all()

    level_info = get_level_info(user.xp)

    return {
        "profile": {
            "user_id": user.id,
            "username": user.username,
            "xp": user.xp,
            "level": level_info["level"],
            "streak": streak.current_streak,
            "level_progress": {
                "current_xp": level_info["current_xp"],
                "level_min_xp": level_info["level_min_xp"],
                "level_max_xp": level_info["level_max_xp"],
                "xp_to_next_level": level_info["xp_to_next_level"],
                "progress_percent": level_info["progress_percent"]
            }
        },
        "stats": {
            "strength": stats.strength,
            "discipline": stats.discipline,
            "focus": stats.focus,
            "energy": stats.energy
        },
        "today_quests": [
            {
                "id": q.id,
                "title": q.title,
                "description": q.description,
                "quest_type": q.quest_type,
                "target_value": q.target_value,
                "progress": q.progress,
                "completed": q.completed,
                "xp_reward": q.xp_reward,
                "quest_date": str(q.quest_date)
            }
            for q in today_quests
        ]
    }