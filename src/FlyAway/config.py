from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from loguru import logger
from RPA.Robocorp.WorkItems import WorkItems

load_dotenv()

ROBOCORP_CLOUD = os.getenv("ROBOCORP_CLOUD", "false")

@dataclass
class Config:
    origin_city : str
    destination_city : str
    departure_date : str   #"dd/mm/yyyy"
    return_date : str      #"dd/mm/yyyy"
    number_of_adults : int
    number_of_children : int


def get_work_item_variable():
    work_itens = WorkItems()
    work_itens.get_input_work_item()

    return Config(
        origin_city = work_itens.get_value("origin_city"),
        destination_city = work_itens.get_value("destination_city"),
        departure_date = work_itens.get_value("departure_date"),
        return_date = work_itens.get_value("return_date"),
        number_of_adults = int(work_itens.get_value("number_of_adults")),
        number_of_children = int(work_itens.get_value("number_of_children"))
    )


def get_environment_variables():
    logger.info("Get environment variables")
    if ROBOCORP_CLOUD.lower() == "true":
        return get_work_item_variable()
    return Config(
        origin_city = os.getenv("ORIGIN_CITY"),
        destination_city = os.getenv("DESTINATION_CITY"),
        departure_date = os.getenv("DEPARTURE_DATE"),
        return_date = os.getenv("RETURN_DATE"),
        number_of_adults = int(os.getenv("NUMBER_OF_ADULTS")),
        number_of_children = int(os.getenv("NUMBER_OF_CHILDREN"))
    )
