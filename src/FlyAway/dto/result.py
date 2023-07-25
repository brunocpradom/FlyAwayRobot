from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.FlyAway.dto.flight import FlightInfo

@dataclass
class Result:
    outbound_flights : List[FlightInfo]
    return_flights : List[FlightInfo]
    datetime : str
    outbound_cheapest_flight : FlightInfo
    return_cheapest_flight : FlightInfo
