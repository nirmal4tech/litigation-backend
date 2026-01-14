from pydantic import BaseModel
from datetime import date

class DiaryCreate(BaseModel):
    case_id: str
    stage_slug: str
    entry_date: date
    what_happened: str
    personal_note: str | None = None


class DiaryOut(BaseModel):
    id: int
    case_id: str
    stage_slug: str
    entry_date: date
    what_happened: str
    personal_note: str | None

    class Config:
        orm_mode = True
