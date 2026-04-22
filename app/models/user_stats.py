from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    strength = Column(Integer, default=0)
    discipline = Column(Integer, default=0)
    focus = Column(Integer, default=0)
    energy = Column(Integer, default=0)