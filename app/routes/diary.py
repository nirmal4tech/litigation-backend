from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.diary import DiaryEntry
from app.models.meta import Stage
from app.schemas.diary import DiaryCreate, DiaryOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DiaryOut)
def create_diary_entry(data: DiaryCreate, db: Session = Depends(get_db)):

    # Validate stage exists
    exists = db.query(Stage).filter(Stage.slug == data.stage_slug).first()
    if not exists:
        raise HTTPException(status_code=400, detail="Invalid stage")

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
def get_diary(case_id: str, db: Session = Depends(get_db)):

    return db.query(DiaryEntry)\
             .filter(DiaryEntry.case_id == case_id)\
             .filter(DiaryEntry.is_archived==False)\
             .order_by(DiaryEntry.entry_date.asc())\
             .all()
