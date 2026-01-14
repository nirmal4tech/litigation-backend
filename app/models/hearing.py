from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from app.core.database import Base
from datetime import datetime

class HearingEntry(Base):
    __tablename__="hearing_entries"

    id = Column(Integer, primary_key=True)
    case_id = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)

class HearingStageSelection(Base):
    __tablename__="hearing_stage_selection"

    id = Column(Integer, primary_key=True)
    hearing_entry_id = Column(Integer, ForeignKey("hearing_entries.id"))
    stage_slug = Column(String, nullable=False)
    selected_at = Column(DateTime, default=datetime.utcnow)
