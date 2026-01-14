from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class DataRetentionLog(Base):
    __tablename__="data_retention_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    target = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
