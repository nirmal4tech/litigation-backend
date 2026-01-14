from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.case import Case
from app.models.hearing import HearingEntry, HearingStageSelection
from app.models.meta import Stage
from app.services.access import is_user_paid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def case_history(case_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(
        Case.id == case_id,
        Case.user_id == user.id
    ).first()

    if not case:
        raise HTTPException(404, "Case not found")

    query = db.query(
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
        HearingEntry.case_id == case_id,
        HearingEntry.is_archived == False
    )

    if not is_user_paid(user):
        limit_date = datetime.utcnow() - timedelta(days=30)
        query = query.filter(HearingEntry.created_at >= limit_date)

    rows = query.order_by(HearingEntry.created_at.asc()).all()

    return [
        {
            "date": r.created_at,
            "stage": r.title,
            "raw_text": r.raw_text
        }
        for r in rows
    ]
