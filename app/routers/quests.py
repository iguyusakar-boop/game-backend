from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.quest import Quest

router = APIRouter(prefix="/quests", tags=["Quests"])


@router.post("/create")
def create_quest(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quest = Quest(
        user_id=current_user.id,
        title="Disiplin geliştir",
        description="3 study action yap",
        quest_type="study",
        target_value=3,
        progress=0,
        completed=False,
        xp_reward=50
    )

    db.add(quest)
    db.commit()
    db.refresh(quest)

    return {
        "message": "quest oluşturuldu",
        "quest": {
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "quest_type": quest.quest_type,
            "target_value": quest.target_value,
            "progress": quest.progress,
            "completed": quest.completed,
            "xp_reward": quest.xp_reward
        }
    }


@router.get("")
def get_quests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quests = db.query(Quest).filter(Quest.user_id == current_user.id).all()

    return [
        {
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "quest_type": quest.quest_type,
            "target_value": quest.target_value,
            "progress": quest.progress,
            "completed": quest.completed,
            "xp_reward": quest.xp_reward
        }
        for quest in quests
    ]