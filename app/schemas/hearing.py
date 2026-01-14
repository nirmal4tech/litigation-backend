from pydantic import BaseModel

class HearingInput(BaseModel):
    case_id:str
    raw_text:str

class HearingStageSelect(BaseModel):
    hearing_entry_id:int
    stage_slug:str
