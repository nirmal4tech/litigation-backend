from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_paid = Column(Boolean, default=False)
    paid_until = Column(DateTime, nullable=True)