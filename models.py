from sqlalchemy import Column, Integer, Float, String
from database import Base

class Crop(Base):
    __tablename__ = "crop_prediction"

    id = Column(Integer, primary_key=True, index=True)

    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    soil_ph = Column(Float)

    predicted_crop = Column(String)
    confidence = Column(Float)
    estimated_yield = Column(Float)