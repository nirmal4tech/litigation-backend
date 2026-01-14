from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.cost import CostEntry
from app.models.meta import Stage
from app.schemas.cost import CostCreate, CostOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CostOut)
def create_cost_entry(data: CostCreate, db: Session = Depends(get_db)):

    # If stage provided, validate
    if data.stage_slug:
        exists = db.query(Stage).filter(Stage.slug == data.stage_slug).first()
        if not exists:
            raise HTTPException(status_code=400, detail="Invalid stage")

    entry = CostEntry(
        case_id=data.case_id,
        amount=data.amount,
        paid_to=data.paid_to,
        reason=data.reason,
        entry_date=data.entry_date,
        stage_slug=data.stage_slug,
        is_archived=False
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


@router.get("/", response_model=list[CostOut])
def get_cost_entries(case_id: str, db: Session = Depends(get_db)):

    return db.query(CostEntry)\
             .filter(CostEntry.case_id == case_id)\
             .filter(CostEntry.is_archived == False)\
             .order_by(CostEntry.entry_date.asc())\
             .all()
