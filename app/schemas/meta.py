from pydantic import BaseModel

class CaseTypeOut(BaseModel):
    slug: str
    title: str

    class Config:
        orm_mode = True


class StageOut(BaseModel):
    slug: str
    title: str
    short_desc: str

    class Config:
        orm_mode = True
