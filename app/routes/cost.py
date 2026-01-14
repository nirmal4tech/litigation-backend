from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.case import Case
from app.models.cost import CostEntry
from app.models.meta import Stage
from app.schemas.cost import CostCreate, CostOut
from app.services.access import is_user_paid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CostOut)
def create_cost_entry(data: CostCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == data.case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    if data.stage_slug:
        stage = db.query(Stage).filter(Stage.slug == data.stage_slug).first()
        if not stage:
            raise HTTPException(400, "Invalid stage")

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
def get_cost_entries(case_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id, Case.user_id == user.id).first()
    if not case:
        raise HTTPException(404, "Case not found")

    query = db.query(CostEntry)\
        .filter(CostEntry.case_id == case_id)\
        .filter(CostEntry.is_archived == False)

    if not is_user_paid(user):
        limit_date = date.today() - timedelta(days=30)
        query = query.filter(CostEntry.entry_date >= limit_date)

    return query.order_by(CostEntry.entry_date.asc()).all()
