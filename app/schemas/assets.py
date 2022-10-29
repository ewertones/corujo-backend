from pydantic import BaseModel


class AssetBase(BaseModel):
    name: str
    _type: str
    description: str


class AssetCreate(AssetBase):
    pass


class AssetResponse(AssetBase):
    pass


class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True
