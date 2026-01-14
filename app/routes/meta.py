from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.meta import CaseType, Stage
from app.schemas.meta import CaseTypeOut, StageOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/case-types", response_model=list[CaseTypeOut])
def get_case_types(db: Session = Depends(get_db)):
    return db.query(CaseType).all()


@router.get("/stages", response_model=list[StageOut])
def get_stages(case_type: str, db: Session = Depends(get_db)):
    return db.query(Stage).filter(Stage.case_type_slug == case_type).all()
