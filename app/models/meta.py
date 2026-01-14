from sqlalchemy import Column, Integer, String
from app.core.database import Base

class CaseType(Base):
    __tablename__ = "case_types"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True)
    case_type_slug = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    title = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
