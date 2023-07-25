from __future__ import annotations

from dataclasses import dataclass

@dataclass
class FlightInfo:
    type : str
    origination : str
    destination : str
    duration : str
    price : str
    departure_time : str
    arrival_time : str
    route : str
    airline : str
