from __future__ import annotations
import time
from datetime import datetime
import os

from robocorp.tasks import task
from loguru import logger

from src.FlyAway.config import Config
from src.FlyAway.config import get_environment_variables
from src.FlyAway.services.gol import VoeGolScrapper
from src.FlyAway.services.json_parser import JsonParser


def start_scrapper():
    config = get_environment_variables()
    flights = VoeGolScrapper(config).release_the_spider()
    JsonParser().save_file(flights)
    logger.info(f"Last run : {datetime.now()}")


@task
def VoeGol():
    start_scrapper()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import schedule
    
    load_dotenv()
    PERIOD  = os.getenv("PERIOD", 2)
    logger.info("FlyAway Scrapper")
    logger.info(f"It will run every {PERIOD} hours")

    schedule.every(int(PERIOD)).hours.do(start_scrapper)
    while True:
        schedule.run_pending()
        time.sleep(1)
