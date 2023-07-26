from __future__ import annotations
import time
from datetime import datetime, timedelta
import os

from robocorp.tasks import task
from loguru import logger

from src.FlyAway.config import Config
from src.FlyAway.config import get_environment_variables
from src.FlyAway.services.gol import VoeGolScrapper
from src.FlyAway.services.json_parser import JsonParser


@task
def VoeGol():
    config = get_environment_variables()
    flights = VoeGolScrapper(config).release_the_spider()
    JsonParser().save_file(flights)


def start_scrapper(period:int):
    logger.info(f"Now: {datetime.now()}")
    config = get_environment_variables()
    flights = VoeGolScrapper(config).release_the_spider()
    JsonParser().save_file(flights)
    logger.info(f"Next run : {datetime.now() + timedelta(hours=period)}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    import schedule
    
    load_dotenv()
    PERIOD  = os.getenv("PERIOD", 2)
    logger.info("FlyAway Scrapper")
    logger.info(f"It will run every {PERIOD} hours")

    schedule.every(int(PERIOD)).hours.do(start_scrapper(int(PERIOD)))
    while True:
        schedule.run_pending()
        time.sleep(1)
