from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean
from app.core.database import Base
from datetime import datetime

class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id = Column(Integer, primary_key=True)
    case_id = Column(String, nullable=False)
    stage_slug = Column(String, nullable=False)
    entry_date = Column(Date, nullable=False)
    what_happened = Column(Text, nullable=False)
    personal_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)
