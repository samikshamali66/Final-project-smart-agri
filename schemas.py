from pydantic import BaseModel

class CropCreate(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    soil_ph: float

class CropResponse(CropCreate):
    id: int
    predicted_crop: str
    confidence: float
    estimated_yield: float

    class Config:
        from_attributes = True