from math import radians, sin, cos, sqrt, atan2

from typing import Dict, List
from interfaces import ChargingPoint

def haversine_distance(coord1: Dict[str, float], coord2: Dict[str, float]):
    R = 6371.0
    
    lat1, lon1 = radians(coord1['latitude']), radians(coord1['longitude'])
    lat2, lon2 = radians(coord2['latitude']), radians(coord2['longitude'])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance


def find_closest_locations(my_coords: Dict[str, float], locations: List[ChargingPoint], n=3):
    filtered_locations = [
        location for location in locations
        if location["description"] is None or "за шлагбаумом" not in location["description"]
    ]

    distances = [
        (location, haversine_distance(my_coords, {'latitude': location["latitude"], 'longitude': location["longitude"]})) 
        for location in filtered_locations
    ]
    
    distances.sort(key=lambda x: x[1])
    
    return [location for location, _ in distances[:n]]