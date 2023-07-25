from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import List

from src.FlyAway.dto.flight import FlightInfo


class JsonParser:

    def save_file(self, flights: List[FlightInfo]):
        with open(f"./output/flights{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w") as file:
            json.dump(asdict(flights), file)
