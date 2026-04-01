import math
from storage.memory_store import last_locations

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def process_location(loc):
    car_id = loc.carId

    if car_id not in last_locations:
        last_locations[car_id] = loc
        return loc

    prev = last_locations[car_id]

    dt = loc.timestamp - prev.timestamp
    if dt <= 0:
        return prev

    dist = distance(prev.lat, prev.lon, loc.lat, loc.lon)

    # анти-скачок
    speed = dist / dt
    if speed > 0.01:  # подберёшь позже
        return prev

    # сглаживание
    smoothed_lat = (prev.lat + loc.lat) / 2
    smoothed_lon = (prev.lon + loc.lon) / 2

    loc.lat = smoothed_lat
    loc.lon = smoothed_lon

    last_locations[car_id] = loc
    return loc