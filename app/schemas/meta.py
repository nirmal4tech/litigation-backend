from pydantic import BaseModel
from pydantic import ConfigDict

class CaseTypeOut(BaseModel):
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)


class StageOut(BaseModel):
    slug: str
    title: str
    short_desc: str

    model_config = ConfigDict(from_attributes=True)
