from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.diary import DiaryEntry
from app.models.hearing import HearingEntry
from app.models.cost import CostEntry
from app.models.retention import DataRetentionLog

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/delete-case")
def delete_case(case_id:str, user_id:str, db:Session=Depends(get_db)):

    db.query(DiaryEntry).filter(DiaryEntry.case_id==case_id).delete()
    db.query(HearingEntry).filter(HearingEntry.case_id==case_id).delete()
    db.query(CostEntry).filter(CostEntry.case_id==case_id).delete()

    db.add(DataRetentionLog(
        user_id=user_id,
        action="deleted",
        target=f"case:{case_id}"
    ))

    db.commit()

    return {"status":"case data deleted"}
