from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass 
class Connectors:
    connectorName: str
    connectorNameEn: str
    available: int
    charging: int
    reserved: int
    all: int
    locationId: str

@dataclass
class Time:
    id: str
    start: str
    finish: str
    time_zone: str

@dataclass
class LocationWorkTime:
    workTime24_7: bool
    time: Optional[Time]
    days: Optional[Dict[str, str]]
    months: Optional[Dict[str, str]]

@dataclass
class ChargingPoint:
    locationId: str
    latitude: float
    longitude: float
    name: str
    street: str
    house: str
    city: str
    description: Optional[str]
    working: bool
    photos: Optional[List[str]]
    connectors: List[Connectors]
    locationWorkTime: LocationWorkTime
    isFavorite: bool
    markers: Optional[List]