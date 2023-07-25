from __future__ import annotations

from robocorp.tasks import task

from src.FlyAway.config import Config
from src.FlyAway.config import get_environment_variables
from src.FlyAway.services.gol import VoeGolScrapper
from src.FlyAway.services.json_parser import JsonParser


@task
def VoeGol():
    config = get_environment_variables()
    VoeGolScrapper(config).release_the_spider()


if __name__ == "__main__":
    config = get_environment_variables()
    flights = VoeGolScrapper(config).release_the_spider()
    JsonParser().save_file(flights)
