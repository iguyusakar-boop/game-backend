from app.database import SessionLocal
from app.models.action import ActionLog
from app.models.user import User
from app.models.user_stats import UserStats
from app.models.streak import UserStreak
from app.engines.xp_engine import calculate_xp
from app.engines.level_engine import calculate_level
from app.engines.streak_engine import update_streak
from app.engines.quest_engine import ensure_daily_quests, apply_action_to_quests


def process_action(data):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == data.user_id).first()

        if not user:
            user = User(
                id=data.user_id,
                username=f"user_{data.user_id}",
                level=1,
                xp=0
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        stats = db.query(UserStats).filter(UserStats.user_id == user.id).first()

        if not stats:
            stats = UserStats(user_id=user.id)
            db.add(stats)
            db.commit()
            db.refresh(stats)

        streak = db.query(UserStreak).filter(UserStreak.user_id == user.id).first()

        if not streak:
            streak = UserStreak(user_id=user.id)
            db.add(streak)
            db.commit()
            db.refresh(streak)

        ensure_daily_quests(db, user.id)

        current_streak = update_streak(streak)

        action = ActionLog(
            user_id=data.user_id,
            action_type=data.action_type,
            value=data.value
        )
        db.add(action)

        xp = calculate_xp(data.action_type, data.value)
        old_level = user.level
        user.xp += xp

        if data.action_type == "study":
            stats.focus += data.value
            stats.discipline += data.value
        elif data.action_type == "workout":
            stats.strength += data.value
            stats.energy += data.value
        elif data.action_type == "meditation":
            stats.focus += data.value
            stats.energy += data.value

        completed_quests, bonus_xp = apply_action_to_quests(
            db=db,
            user=user,
            action_type=data.action_type,
            value=data.value
        )

        user.level = calculate_level(user.xp)
        leveled_up = user.level > old_level

        db.commit()
        db.refresh(action)
        db.refresh(user)
        db.refresh(stats)
        db.refresh(streak)

        return {
            "action_id": action.id,
            "user_id": user.id,
            "action_type": action.action_type,
            "value": action.value,
            "xp_gained": xp,
            "quest_bonus_xp": bonus_xp,
            "completed_quests": completed_quests,
            "total_xp": user.xp,
            "level": user.level,
            "leveled_up": leveled_up,
            "streak": current_streak,
            "stats": {
                "strength": stats.strength,
                "discipline": stats.discipline,
                "focus": stats.focus,
                "energy": stats.energy
            }
        }
    finally:
        db.close()