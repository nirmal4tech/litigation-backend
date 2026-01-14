from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.case import Case
from app.models.meta import CaseType

router = APIRouter()

@router.post("/")
def export_case(case_id: str, user = Depends(require_paid_user)):
    return {"status": "export allowed"}
