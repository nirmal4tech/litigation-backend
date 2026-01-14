from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.case import Case
from app.models.hearing import HearingEntry, HearingStageSelection
from app.models.meta import Stage
from app.schemas.hearing import HearingInput, HearingStageSelect

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entry")
def create_hearing(data: HearingInput, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == data.case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    entry = HearingEntry(
        case_id=data.case_id,
        raw_text=data.raw_text,
        is_archived=False
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"hearing_entry_id": entry.id}


@router.post("/")
def submit_hearing(data: HearingInput, case_type:str, db:Session=Depends(get_db)):

    matches = match_hearing(data.raw_text, case_type, db)

    return [
        {
            "slug": s.slug,
            "title": s.title,
            "short_desc": s.short_desc
        }
        for s in matches
    ]

@router.post("/select")
def select_stage(data: HearingStageSelect, user=Depends(get_current_user), db: Session = Depends(get_db)):

    entry = db.query(HearingEntry).filter(HearingEntry.id == data.hearing_entry_id).first()
    if not entry:
        raise HTTPException(404, "Hearing entry not found")

    case = db.query(Case).filter(Case.id == entry.case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    stage = db.query(Stage).filter(
        Stage.slug == data.stage_slug,
        Stage.case_type_slug == case.case_type
    ).first()

    if not stage:
        raise HTTPException(400, "Invalid stage for this case")

    selection = HearingStageSelection(
        hearing_entry_id=data.hearing_entry_id,
        stage_slug=data.stage_slug
    )

    db.add(selection)
    db.commit()

    return {
        "hearing_entry_id": data.hearing_entry_id,
        "stage_slug": data.stage_slug
    }
