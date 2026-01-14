from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base
import uuid

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    case_type = Column(String)
