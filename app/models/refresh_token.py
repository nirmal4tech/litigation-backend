from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
    device_id = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
