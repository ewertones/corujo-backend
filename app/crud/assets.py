from sqlalchemy.orm import Session
from models import models
from schemas import assets, asset_values, asset_predictions
from datetime import date


def get_asset(db: Session, asset_id: int):
    return db.query(models.Assets).filter(models.Assets.id == asset_id).first()


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Assets).offset(skip).limit(limit).all()


def get_asset_prediction(db: Session, asset_id: int, date: date):
    return (
        db.query(models.AssetPredictions)
        .filter(
            models.AssetPredictions.id == asset_id
            and models.AssetPredictions.date == date
        )
        .first()
    )


def get_asset_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AssetPredictions).offset(skip).limit(limit).all()


def get_asset_value(db: Session, asset_id: int, date: date):
    return (
        db.query(models.AssetValues)
        .filter(models.AssetValues.id == asset_id and models.AssetValues.date == date)
        .first()
    )


def get_asset_values(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AssetValues).offset(skip).limit(limit).all()


def create_asset(db: Session, asset: assets.AssetsCreate):
    db_asset = models.Assets(
        name=asset.name,
        _type=asset._type,
        description=asset.description,
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def create_asset_prediction(
    db: Session,
    asset_prediction: asset_predictions.AssetPredictionsCreate,
    asset_id: int,
):
    db_asset_prediction = models.AssetPredictions(
        **asset_prediction.dict(), asset_id=asset_id
    )
    db.add(db_asset_prediction)
    db.commit()
    db.refresh(db_asset_prediction)
    return db_asset_prediction


def create_asset_value(
    db: Session, asset_value: asset_values.AssetValuesCreate, asset_id: int
):
    db_asset_value = models.AssetValues(**asset_value.dict(), asset_id=asset_id)
    db.add(db_asset_value)
    db.commit()
    db.refresh(db_asset_value)
    return db_asset_value
