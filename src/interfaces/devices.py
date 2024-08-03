from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Tariff:
    id: str
    startTime: str
    finishTime: str
    name: str
    amount: float
    tariffTypeId: str
    tariffType: str
    description: str
    work24_7: bool
    power: Optional[float]
    days: List[str]
    daysMap: dict
    isCurrent: bool

@dataclass
class ReservationTariff:
    id: str
    name: str
    time: int
    type: str
    amount: float
    days: List[str]
    daysMap: dict

@dataclass
class Connector:
    connectorId: str
    typeEn: str
    typeRu: str
    status: str
    codeByProtocol: int
    amperageType: str
    blockAmount: float
    deviceNumber: Optional[int]
    deviceId: Optional[int]
    power: float
    dynamicAllocation: Optional[bool]
    booking: bool
    locationId: Optional[int]
    activeBooking: bool
    unavailableDueBooking: bool
    evseNumber: int
    isPressedEmergencyBtn: Optional[bool]
    tariffs: List[Tariff]
    reservationTariffs: List[ReservationTariff]
    dynamicAllocationTariffs: Optional[List[dict]]

@dataclass
class Device:
    number: int
    connectors: List[Connector]
    displayCodeByProtocol: bool
    locationNumber: str
    pressedEmergencyBtn: bool

@dataclass
class RootDevice:
    devices: List[Device]
    interestingPoints: List[dict]