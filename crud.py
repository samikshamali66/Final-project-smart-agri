from sqlalchemy.orm import Session
import models
import schemas


def create_crop(db: Session, crop: schemas.CropCreate,
                predicted_crop, confidence, estimated_yield):

    db_crop = models.Crop(

        nitrogen=crop.nitrogen,
        phosphorus=crop.phosphorus,
        potassium=crop.potassium,
        temperature=crop.temperature,
        humidity=crop.humidity,
        soil_ph=crop.soil_ph,

        predicted_crop=predicted_crop,
        confidence=confidence,
        estimated_yield=estimated_yield

    )

    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)

    return db_crop


def get_all(db: Session):
    return db.query(models.Crop).all()


def get_one(db: Session, crop_id: int):
    return db.query(models.Crop).filter(
        models.Crop.id == crop_id
    ).first()


def delete_crop(db: Session, crop_id: int):

    crop = db.query(models.Crop).filter(
        models.Crop.id == crop_id
    ).first()

    if crop:
        db.delete(crop)
        db.commit()

    return crop


def update_crop(db: Session, crop_id: int, crop: schemas.CropCreate):

    db_crop = db.query(models.Crop).filter(
        models.Crop.id == crop_id
    ).first()

    if db_crop:

        db_crop.nitrogen = crop.nitrogen
        db_crop.phosphorus = crop.phosphorus
        db_crop.potassium = crop.potassium
        db_crop.temperature = crop.temperature
        db_crop.humidity = crop.humidity
        db_crop.soil_ph = crop.soil_ph

        db.commit()
        db.refresh(db_crop)

    return db_crop