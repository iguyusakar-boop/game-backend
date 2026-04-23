from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Temel bilgiler
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Oyun sistemi
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)

    # Stat sistemi
    discipline = Column(Integer, default=0)
    focus = Column(Integer, default=0)
    strength = Column(Integer, default=0)
    energy = Column(Integer, default=0)