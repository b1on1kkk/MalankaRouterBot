from dataclasses import dataclass

@dataclass
class PointCoordinates:
    locationId: str
    lat: float
    lon: float