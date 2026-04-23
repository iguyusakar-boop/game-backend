from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.database import Base


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quest_type = Column(String, nullable=False)

    target_value = Column(Integer, default=1)
    progress = Column(Integer, default=0)

    completed = Column(Boolean, default=False)
    xp_reward = Column(Integer, default=0)

    quest_date = Column(Date, nullable=False)