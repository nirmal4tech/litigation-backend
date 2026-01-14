from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import SessionLocal
from app.dependencies.access import require_paid_user
from app.models.case import Case
from app.models.hearing import HearingEntry, HearingStageSelection
from app.models.diary import DiaryEntry
from app.models.cost import CostEntry
from app.models.meta import Stage
from app.models.retention import DataRetentionLog

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def export_case(case_id: str, user = Depends(require_paid_user), db: Session = Depends(get_db)):

    # Ownership check
    case = db.query(Case).filter(
        Case.id == case_id,
        Case.user_id == user.id
    ).first()

    if not case:
        raise HTTPException(404, "Case not found")

    # History
    history_rows = db.query(
        HearingEntry.created_at,
        HearingEntry.raw_text,
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
    ).order_by(
        HearingEntry.created_at.asc()
    ).all()

    history = [
        {
            "date": r.created_at,
            "stage": r.title,
            "raw_text": r.raw_text
        }
        for r in history_rows
    ]

    # Diary
    diary_rows = db.query(DiaryEntry)\
        .filter(DiaryEntry.case_id == case_id)\
        .filter(DiaryEntry.is_archived == False)\
        .order_by(DiaryEntry.entry_date.asc())\
        .all()

    diary = [
        {
            "date": d.entry_date,
            "stage_slug": d.stage_slug,
            "what_happened": d.what_happened,
            "personal_note": d.personal_note
        }
        for d in diary_rows
    ]

    # Costs
    cost_rows = db.query(CostEntry)\
        .filter(CostEntry.case_id == case_id)\
        .filter(CostEntry.is_archived == False)\
        .order_by(CostEntry.entry_date.asc())\
        .all()

    costs = [
        {
            "date": c.entry_date,
            "amount": float(c.amount),
            "paid_to": c.paid_to,
            "reason": c.reason,
            "stage_slug": c.stage_slug
        }
        for c in cost_rows
    ]

    # Retention log
    db.add(DataRetentionLog(
        user_id=user.id,
        action="exported",
        target=f"case:{case_id}"
    ))
    db.commit()

    return {
        "case": {
            "id": case.id,
            "case_type": case.case_type,
            "created_at": case.created_at
        },
        "history": history,
        "diary": diary,
        "costs": costs,
        "exported_at": datetime.utcnow(),
        "exported_by": user.id
    }
