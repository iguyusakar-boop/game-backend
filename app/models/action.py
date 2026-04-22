from sqlalchemy import Column, Integer, String
from app.database import Base

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False)
    value = Column(Integer, nullable=False, default=1)