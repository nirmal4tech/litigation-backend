from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.hearing import HearingEntry, HearingStageSelection
from app.models.meta import Stage
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def case_history(case_id: str, db: Session = Depends(get_db)):

    rows = db.query(
        HearingEntry.id,
        HearingEntry.created_at,
        HearingEntry.raw_text,
        HearingStageSelection.stage_slug,
        Stage.title
    ).join(
        HearingStageSelection,
        HearingStageSelection.hearing_entry_id == HearingEntry.id
    ).join(
        Stage,
        Stage.slug == HearingStageSelection.stage_slug
    ).filter(
        HearingEntry.case_id == case_id
    ).filter(
        HearingEntry.is_archived == False
    ).order_by(
        HearingEntry.created_at.asc()
    ).all()

    return [
        {
            "date": r.created_at,
            "stage": r.title,
            "raw_text": r.raw_text
        }
        for r in rows
    ]
