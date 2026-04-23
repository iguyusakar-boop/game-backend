from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.quest import Quest
from app.models.stat import UserStat
from app.models.streak import UserStreak

router = APIRouter(prefix="/action", tags=["Actions"])


@router.post("")
def create_action(
    action_type: str = "study",
    value: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    xp_gain = value * 10
    today = date.today()

    current_user.xp += xp_gain

    if current_user.xp >= current_user.level * 100:
        current_user.level += 1

    stats = db.query(UserStat).filter(UserStat.user_id == current_user.id).first()
    if not stats:
        stats = UserStat(
            user_id=current_user.id,
            strength=0,
            discipline=0,
            focus=0,
            energy=0
        )
        db.add(stats)
        db.flush()

    streak = db.query(UserStreak).filter(UserStreak.user_id == current_user.id).first()
    if not streak:
        streak = UserStreak(
            user_id=current_user.id,
            current_streak=0,
            last_action_date=None
        )
        db.add(streak)
        db.flush()

    if action_type == "study":
        stats.discipline += value
        stats.focus += value
    elif action_type == "work":
        stats.strength += value
    elif action_type == "health":
        stats.energy += value

    if streak.last_action_date != today:
        streak.current_streak += 1
        streak.last_action_date = today

    quests = db.query(Quest).filter(
        Quest.user_id == current_user.id,
        Quest.completed == False
    ).all()

    for quest in quests:
        if quest.quest_type == "daily_action":
            quest.progress += value

        elif quest.quest_type == "daily_discipline":
            if action_type in ["study", "work"]:
                quest.progress += value

        elif quest.quest_type == "daily_streak":
            if quest.progress < 1:
                quest.progress = 1

        if quest.progress >= quest.target_value and not quest.completed:
            quest.completed = True
            current_user.xp += quest.xp_reward

            if current_user.xp >= current_user.level * 100:
                current_user.level += 1

    db.commit()
    db.refresh(current_user)
    db.refresh(stats)
    db.refresh(streak)

    updated_quests = db.query(Quest).filter(
        Quest.user_id == current_user.id
    ).all()

    return {
        "message": "action işlendi",
        "xp_gained": xp_gain,
        "total_xp": current_user.xp,
        "level": current_user.level,
        "streak": streak.current_streak,
        "stats": {
            "discipline": stats.discipline,
            "focus": stats.focus,
            "strength": stats.strength,
            "energy": stats.energy
        },
        "quests": [
            {
                "id": quest.id,
                "title": quest.title,
                "quest_type": quest.quest_type,
                "progress": quest.progress,
                "target_value": quest.target_value,
                "completed": quest.completed,
                "xp_reward": quest.xp_reward
            }
            for quest in updated_quests
        ]
    }