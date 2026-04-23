from datetime import date
from sqlalchemy.orm import Session

from app.models.quest import Quest


def ensure_daily_quests(db: Session, user_id: int):
    today = date.today()

    # bugün quest var mı kontrol et
    existing = db.query(Quest).filter(
        Quest.user_id == user_id,
        Quest.quest_date == today
    ).first()

    if existing:
        return  # zaten var

    # yoksa oluştur
    quests = [
        Quest(
            user_id=user_id,
            title="Bugün 1 action tamamla",
            description="Herhangi bir alanda 1 action gir",
            quest_type="daily_action",
            target_value=1,
            progress=0,
            completed=False,
            xp_reward=20,
            quest_date=today
        ),
        Quest(
            user_id=user_id,
            title="Disiplin geliştir",
            description="2 adet study veya work action gir",
            quest_type="daily_discipline",
            target_value=2,
            progress=0,
            completed=False,
            xp_reward=30,
            quest_date=today
        ),
        Quest(
            user_id=user_id,
            title="Seriyi koru",
            description="Bugün en az 1 işlem yap",
            quest_type="daily_streak",
            target_value=1,
            progress=0,
            completed=False,
            xp_reward=25,
            quest_date=today
        )
    ]

    db.add_all(quests)
    db.commit()