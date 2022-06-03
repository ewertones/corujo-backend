from pydantic import BaseModel


class AssetsBase(BaseModel):
    name: str
    _type: str
    description: str


class AssetsCreate(AssetsBase):
    pass


class Assets(AssetsBase):
    id: int

    class Config:
        orm_mode = True