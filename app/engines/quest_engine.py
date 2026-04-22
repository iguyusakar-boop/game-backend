from app.models.quest import Quest

def ensure_daily_quests(db, user_id: int):
    existing = db.query(Quest).filter(Quest.user_id == user_id).all()

    if existing:
        return existing

    quests = [
        Quest(
            user_id=user_id,
            title="Bugün 3 kez study yap",
            action_type="study",
            target_value=3,
            progress_value=0,
            reward_xp=30,
            is_completed=False
        ),
        Quest(
            user_id=user_id,
            title="Bugün 1 kez meditation yap",
            action_type="meditation",
            target_value=1,
            progress_value=0,
            reward_xp=20,
            is_completed=False
        ),
        Quest(
            user_id=user_id,
            title="Bugün 1 kez workout yap",
            action_type="workout",
            target_value=1,
            progress_value=0,
            reward_xp=25,
            is_completed=False
        )
    ]

    for quest in quests:
        db.add(quest)

    db.commit()

    return db.query(Quest).filter(Quest.user_id == user_id).all()


def apply_action_to_quests(db, user, action_type: str, value: int):
    quests = db.query(Quest).filter(
        Quest.user_id == user.id,
        Quest.is_completed == False
    ).all()

    completed_quests = []
    bonus_xp = 0

    for quest in quests:
        if quest.action_type != action_type:
            continue

        quest.progress_value += value

        if quest.progress_value >= quest.target_value:
            quest.progress_value = quest.target_value
            quest.is_completed = True
            bonus_xp += quest.reward_xp
            completed_quests.append({
                "quest_id": quest.id,
                "title": quest.title,
                "reward_xp": quest.reward_xp
            })

    user.xp += bonus_xp

    return completed_quests, bonus_xp