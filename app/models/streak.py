from sqlalchemy import Column, Integer, Date, ForeignKey
from app.database import Base

class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    current_streak = Column(Integer, default=0)
    last_action_date = Column(Date, nullable=True)