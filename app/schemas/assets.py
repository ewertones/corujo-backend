from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    name: str
    _type: str = Field(alias="type")
    description: str


class AssetCreate(AssetBase):
    pass


class AssetResponse(AssetBase):
    pass


class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True
