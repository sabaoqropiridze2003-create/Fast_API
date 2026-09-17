from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    duration: int


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True