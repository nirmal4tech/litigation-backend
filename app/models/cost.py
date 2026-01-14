from sqlalchemy import Boolean, Column, Integer, String, Numeric, Text, Date, DateTime
from app.core.database import Base
from datetime import datetime

class CostEntry(Base):
    __tablename__ = "cost_entries"

    id = Column(Integer, primary_key=True)
    case_id = Column(String, nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    paid_to = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    entry_date = Column(Date, nullable=False)
    stage_slug = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)
