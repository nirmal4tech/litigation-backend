from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.case import Case
from app.models.diary import DiaryEntry
from app.models.meta import Stage
from app.schemas.diary import DiaryCreate, DiaryOut
from app.services.access import is_user_paid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DiaryOut)
def create_diary_entry(data: DiaryCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == data.case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    stage = db.query(Stage).filter(Stage.slug == data.stage_slug).first()
    if not stage:
        raise HTTPException(400, "Invalid stage")

    entry = DiaryEntry(
        case_id=data.case_id,
        stage_slug=data.stage_slug,
        entry_date=data.entry_date,
        what_happened=data.what_happened,
        personal_note=data.personal_note,
        is_archived=False
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


@router.get("/", response_model=list[DiaryOut])
def get_diary(case_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    query = db.query(DiaryEntry)\
        .filter(DiaryEntry.case_id == case_id)\
        .filter(DiaryEntry.is_archived == False)

    if not is_user_paid(user):
        limit_date = date.today() - timedelta(days=30)
        query = query.filter(DiaryEntry.entry_date >= limit_date)

    return query.order_by(DiaryEntry.entry_date.asc()).all()
