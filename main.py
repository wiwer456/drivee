from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Location
from services.location_service import process_location, predict_location
from storage.memory_store import last_locations

app = FastAPI()

# CORS (для frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "server running"}


@app.post("/location")
def update_location(loc: Location):
    processed = process_location(loc)
    return {"status": "ok", "data": processed}


@app.get("/location/{car_id}")
def get_location(car_id: str):
    loc = last_locations.get(car_id)

    if not loc:
        return None

    return predict_location(loc)