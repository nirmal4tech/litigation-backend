from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.hearing import HearingInput, HearingStageSelect
from app.core.database import SessionLocal
from app.services.hearing_matcher import match_hearing
from app.models.hearing import HearingEntry, HearingStageSelection
from app.models.meta import Stage
from app.models.case import Case

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entry")
def create_hearing(data:HearingInput, db:Session=Depends(get_db)):

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
def select_stage(data:HearingStageSelect, db:Session=Depends(get_db)):

    # Validate stage exists
    case = db.query(Case).filter(Case.id == data.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    exists = db.query(Stage).filter(
        Stage.slug == data.stage_slug,
        Stage.case_type_slug == case.case_type
    ).first()

    if not exists:
        raise HTTPException(status_code=400, detail="Invalid stage for this case type")

    selection = HearingStageSelection(
        hearing_entry_id=data.hearing_entry_id,
        stage_slug=data.stage_slug
    )

    db.add(selection)
    db.commit()

    return {"status":"saved"}