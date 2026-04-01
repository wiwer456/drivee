from pydantic import BaseModel

class Location(BaseModel):
    carId: str
    lat: float
    lon: float
    speed: float = 0
    timestamp: float