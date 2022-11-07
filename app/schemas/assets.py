from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    name: str
    type: str = Field(alias="_type")
    description: str


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    symbol: str

    class Config:
        orm_mode = True
