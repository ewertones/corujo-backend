from sqlalchemy.orm import Session
from models import models
from schemas import assets, asset_values, asset_predictions
from datetime import date


def get_asset(db: Session, asset_id: int):
    return db.query(models.Assets).filter(models.Assets.id == asset_id).first()


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    assets = (
        db.query(models.Assets)
        .with_entities(
            models.Assets.id,
            models.Assets.name,
            models.Assets._type,
            models.Assets.description,
            models.Assets.symbol,
        )
        .order_by(models.Assets.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return assets


def get_asset_prediction(db: Session, asset_id: int, date: date):
    return (
        db.query(models.AssetPredictions)
        .with_entities(
            models.AssetPredictions.asset_id,
            models.AssetPredictions.date,
            models.AssetPredictions.close,
        )
        .filter(
            models.AssetPredictions.asset_id == asset_id
            and models.AssetPredictions.date == date
        )
        .first()
    )


def get_asset_predictions(db: Session, asset_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.AssetPredictions)
        .with_entities(
            models.AssetPredictions.asset_id,
            models.AssetPredictions.date,
            models.AssetPredictions.close,
        )
        .filter(models.AssetPredictions.asset_id == asset_id)
        .order_by(models.AssetPredictions.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_asset_value(db: Session, asset_id: int, date: date):
    return (
        db.query(models.AssetValues)
        .with_entities(
            models.AssetValues.asset_id,
            models.AssetValues.date,
            models.AssetValues._open,
            models.AssetValues.close,
            models.AssetValues.high,
            models.AssetValues.low,
            models.AssetValues.volume,
        )
        .filter(
            models.AssetValues.asset_id == asset_id and models.AssetValues.date == date
        )
        .first()
    )


def get_asset_values(db: Session, asset_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.AssetValues)
        .with_entities(
            models.AssetValues.asset_id,
            models.AssetValues.date,
            models.AssetValues._open,
            models.AssetValues.close,
            models.AssetValues.high,
            models.AssetValues.low,
            models.AssetValues.volume,
        )
        .filter(models.AssetValues.asset_id == asset_id)
        .order_by(models.AssetValues.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
