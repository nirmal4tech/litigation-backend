from sqlalchemy import Column, String
from app.core.database import Base

class Stage(Base):
    __tablename__ = "stages"

    id = Column(String, primary_key=True)
    case_type = Column(String)
    title = Column(String)
    short_desc = Column(String)
