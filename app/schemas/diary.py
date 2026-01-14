from pydantic import BaseModel
from datetime import date
from pydantic import ConfigDict

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

    model_config = ConfigDict(from_attributes=True)
