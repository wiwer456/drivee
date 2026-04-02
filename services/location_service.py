import math
import time
import requests
from storage.memory_store import last_locations

API_KEY = "aab4be73-be88-4924-9a84-a0f898c0b2ec"

# расстояние (простое, для прототипа)
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

# привязка к дороге (snap to road)
def snap_to_road(lat, lon):
    url = "https://graphhopper.com/api/1/route"

    params = {
        "point": f"{lat},{lon}",
        "vehicle": "car",
        "locale": "en",
        "calc_points": "true",
        "key": API_KEY
    }

    try:
        res = requests.get(url, params=params, timeout=2)
        data = res.json()

        if "paths" in data and len(data["paths"]) > 0:
            snapped = data["paths"][0]["points"]["coordinates"][0]
            return snapped[1], snapped[0]  # lat, lon

        return lat, lon

    except:
        return lat, lon


# обработка входящей точки
def process_location(loc):
    car_id = loc.carId

    # первая точка
    if car_id not in last_locations:
        lat, lon = snap_to_road(loc.lat, loc.lon)
        loc.lat = lat
        loc.lon = lon

        last_locations[car_id] = loc
        return loc

    prev = last_locations[car_id]

    dt = loc.timestamp - prev.timestamp
    if dt <= 0:
        return prev

    # привязка к дороге
    lat, lon = snap_to_road(loc.lat, loc.lon)
    loc.lat = lat
    loc.lon = lon

    # расстояние
    dist = distance(prev.lat, prev.lon, loc.lat, loc.lon)

    # анти-скачок
    speed = dist / dt
    if speed > 0.01:
        return prev

    # сглаживание
    smoothed_lat = (prev.lat + loc.lat) / 2
    smoothed_lon = (prev.lon + loc.lon) / 2

    loc.lat = smoothed_lat
    loc.lon = smoothed_lon

    last_locations[car_id] = loc
    return loc


def predict_location(loc):
    now = time.time()
    dt = now - loc.timestamp

    status = "ok"

    if dt < 2:
        return {
            "carId": loc.carId,
            "lat": loc.lat,
            "lon": loc.lon,
            "speed": loc.speed,
            "timestamp": loc.timestamp,
            "status": status
        }

    if dt > 2:
        status = "predicted"

    if dt > 30:
        loc.speed = 0
        status = "stopped"

    # берём предыдущую точку
    prev = last_locations.get(loc.carId)

    if not prev:
        return loc

    # направление движения
    dx = loc.lat - prev.lat
    dy = loc.lon - prev.lon

    # нормализация
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return loc

    dx /= length
    dy /= length

    # движение вперёд
    loc.lat += dx * loc.speed * dt * 0.00001
    loc.lon += dy * loc.speed * dt * 0.00001

    loc.timestamp = now

    return {
        "carId": loc.carId,
        "lat": loc.lat,
        "lon": loc.lon,
        "speed": loc.speed,
        "timestamp": loc.timestamp,
        "status": status
    }