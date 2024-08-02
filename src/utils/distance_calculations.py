import os
import logging
import aiohttp
import asyncio

from typing import Dict, List, Tuple
from interfaces import ChargingPoint

from math import radians, sin, cos, sqrt, atan2

from constants import BOT_ANSWERS

class DistanceAPI:
    def __init__(self, user_connector: str):
        self._user_connector = user_connector
        self._charger_locations = None


    # get all charger points
    async def _get_chargers(self) -> List[ChargingPoint] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{os.getenv('CHARGING_POINTS_API')}?connectors={self._user_connector}") as response:
                charger_locations: List[ChargingPoint] = await response.json()
                self._charger_locations = charger_locations
                return charger_locations


    # get charger info about each station in the charger point
    async def _get_local_connector_info(self, id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{os.getenv('LOCATION_INF')}?locationId={id}") as response:
                devices: List[ChargingPoint] = await response.json()
                return devices


    async def _connector_info(self):
        local = []
        for charger in self._charger_locations:
            connectors = self._get_local_connector_info(charger["locationId"])
            local.append(connectors)

        results = await asyncio.gather(*local)

        local_connectors = {}
        for i in range(len(self._charger_locations)):
            local_connectors[self._charger_locations[i]["locationId"]] = results[i]

        return local_connectors 



class Distance(DistanceAPI):
    def __init__(self, user_coords: Dict[str, float], user_connector: str):
        super().__init__(user_connector)
        self._user_coords = user_coords
        self._local_connectors = None
        self._charger_locations = None


    def _calculate_distance(self, coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
        R = 6371.0

        lat1, lon1 = radians(coord1['latitude']), radians(coord1['longitude'])
        lat2, lon2 = radians(coord2['latitude']), radians(coord2['longitude'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance       


    def _is_connector_active(self, charger_id: str) -> bool:
        charger = self._local_connectors[charger_id]
        for device in charger["devices"]:
            for connector in device["connectors"]:
                if connector["typeRu"] == self._user_connector and connector["status"] == "Available":
                    return True
        return False


    async def find_location(self, n = 3) -> List[Tuple[ChargingPoint, int]]:
        try:
            self._charger_locations = await self._get_chargers()
            self._local_connectors = await self._connector_info()

            filtered_locations = list()
            for location in self._charger_locations:
                if (location["description"] is None or "за шлагбаумом" not in location["description"]) and self._is_connector_active(location["locationId"]):
                    filtered_locations.append(location)

            distances = list()
            for location in filtered_locations:
                location_coords = {"latitude": location["latitude"], "longitude": location["longitude"]}
                distance = self._calculate_distance(self._user_coords, location_coords)
                distances.append((location, distance))

            distances.sort(key=lambda x: x[1])

            return [(location, distance) for location, distance in distances[:n]]
        except Exception as e:
            logging.error(e)
            raise Exception(BOT_ANSWERS["error"])