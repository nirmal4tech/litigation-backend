from pydantic import BaseModel
from datetime import date

class CostCreate(BaseModel):
    case_id: str
    amount: float
    paid_to: str
    reason: str | None = None
    entry_date: date
    stage_slug: str | None = None


class CostOut(BaseModel):
    id: int
    case_id: str
    amount: float
    paid_to: str
    reason: str | None
    entry_date: date
    stage_slug: str | None

    class Config:
        orm_mode = True
