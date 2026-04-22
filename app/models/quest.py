from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    action_type = Column(String, nullable=False)

    target_value = Column(Integer, nullable=False, default=1)
    progress_value = Column(Integer, nullable=False, default=0)

    reward_xp = Column(Integer, nullable=False, default=20)
    is_completed = Column(Boolean, default=False)