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

DAILY_QUESTS = [
    ("Bugün 1 action tamamla",  "daily_action",     1, 20),
    ("Disiplin geliştir",       "daily_discipline",  2, 30),
    ("Seriyi koru",             "daily_streak",      1, 25),
]


def ensure_daily_quests(user_id: int, db: Session):
    today = date.today()
    existing = db.query(Quest).filter(
        Quest.user_id == user_id,
        Quest.quest_date == today,
    ).first()

    if existing:
        return

    for title, qtype, target, xp_reward in DAILY_QUESTS:
        db.add(Quest(
            user_id=user_id,
            title=title,
            description="",
            quest_type=qtype,
            target_value=target,
            progress=0,
            completed=False,
            xp_reward=xp_reward,
            quest_date=today,
        ))
    db.flush()


def ensure_stats(user_id: int, db: Session) -> UserStat:
    stats = db.query(UserStat).filter(UserStat.user_id == user_id).first()
    if not stats:
        stats = UserStat(user_id=user_id, strength=0, discipline=0, focus=0, energy=0)
        db.add(stats)
        db.flush()
    return stats


def ensure_streak(user_id: int, db: Session) -> UserStreak:
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not streak:
        streak = UserStreak(user_id=user_id, current_streak=0, last_action_date=None)
        db.add(streak)
        db.flush()
    return streak


@router.post("")
def create_action(
    action_type: str = "study",
    value: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = date.today()

    ensure_daily_quests(current_user.id, db)

    stats  = ensure_stats(current_user.id, db)
    streak = ensure_streak(current_user.id, db)

    xp_gain = value * 10
    current_user.xp += xp_gain
    if current_user.xp >= current_user.level * 100:
        current_user.level += 1

    if action_type == "study":
        stats.discipline += value
        stats.focus      += value
    elif action_type == "work":
        stats.strength += value
    elif action_type == "health":
        stats.energy += value

    if streak.last_action_date != today:
        streak.current_streak  += 1
        streak.last_action_date = today

    quests = db.query(Quest).filter(
        Quest.user_id    == current_user.id,
        Quest.completed  == False,
        Quest.quest_date == today,
    ).all()

    for quest in quests:
        if quest.quest_type == "daily_action":
            quest.progress += value
        elif quest.quest_type == "daily_discipline":
            if action_type in ("study", "work"):
                quest.progress += value
        elif quest.quest_type == "daily_streak":
            quest.progress = min(quest.progress + 1, quest.target_value)

        if quest.progress >= quest.target_value:
            quest.completed = True
            current_user.xp += quest.xp_reward
            if current_user.xp >= current_user.level * 100:
                current_user.level += 1

    db.commit()

    all_today_quests = db.query(Quest).filter(
        Quest.user_id    == current_user.id,
        Quest.quest_date == today,
    ).all()

    return {
        "message":   "action işlendi",
        "xp_gained": xp_gain,
        "total_xp":  current_user.xp,
        "level":     current_user.level,
        "streak":    streak.current_streak,
        "stats": {
            "discipline": stats.discipline,
            "focus":      stats.focus,
            "strength":   stats.strength,
            "energy":     stats.energy,
        },
        "quests": [
            {
                "id":           q.id,
                "title":        q.title,
                "quest_type":   q.quest_type,
                "progress":     q.progress,
                "target_value": q.target_value,
                "completed":    q.completed,
                "xp_reward":    q.xp_reward,
            }
            for q in all_today_quests
        ],
    }