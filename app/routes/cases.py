from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.case import Case
from app.models.meta import CaseType

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_case(case_type: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    exists = db.query(CaseType).filter(CaseType.slug == case_type).first()
    if not exists:
        raise HTTPException(400, "Invalid case type")

    case = Case(user_id=user.id, case_type=case_type)
    db.add(case)
    db.commit()
    db.refresh(case)

    return case
