from __future__ import annotations

import time
from datetime import datetime
from typing import List

from loguru import logger
from RPA.Browser.Selenium import By
from RPA.Browser.Selenium import Selenium

from src.FlyAway.config import Config
from src.FlyAway.dto.flight import FlightInfo
from src.FlyAway.dto.result import Result
from src.FlyAway.services import (
    ACCEPT_COOKIES_BUTTON,
    ADD_NUMBER_OF_ADULTS_BUTTON,
    DEPARTURE_CITY_INPUT,
    DEPARTURE_CITY_SELECT,
    DEPARTURE_DATE_INPUT,
    DESTINATION_CITY_INPUT,
    DESTINATION_CITY_SELECT,
    DESTINATION_XPATH,
    DURATION_XPATH,
    FLIGHT_SUBMIT_BUTTON,
    FLIGHT_XPATH,
    FLIGHTS_RESULTS,
    NUMBER_OF_ADULTS_ELEMENT,
    NUMBER_OF_CHILDREN_BUTTON,
    ORIGINATION_XPATH,
    PRICE_XPATH,
    RETURN_DATE_INPUT,
    ROUND_TRIP_OPTION,
    ROUTE_TYPE,
    ROUTE_XPATH,
    SUBMIT_BUTTON,
)

class VoeGolScrapper():
    url = "https://www.voegol.com.br/"

    def __init__(self, config : Config):
        self.robot = Selenium()
        self.logger = logger
        self.config = config
        self.outbound_flights = list()
        self.return_flights = list()

    def select_route(self):
        self.logger.info("Select route")
        self.robot.click_element_when_clickable(ROUTE_TYPE)
        self.robot.click_element_when_clickable(ROUND_TRIP_OPTION)

    def select_cities(self):
        self.logger.info("Select departure and destination cities")
        self.robot.click_element_when_clickable(DEPARTURE_CITY_SELECT)
        self.robot.input_text(DEPARTURE_CITY_INPUT, self.config.origin_city)
        self.robot.press_keys(DEPARTURE_CITY_INPUT, "ENTER")

        self.robot.click_element_when_clickable(DESTINATION_CITY_SELECT)
        self.robot.input_text(DESTINATION_CITY_INPUT, self.config.destination_city)
        self.robot.press_keys(DESTINATION_CITY_INPUT, "ENTER")

    def select_number_of_passengers(self):
        self.logger.info("Select number of passengers")
        self.robot.click_element_when_clickable(NUMBER_OF_ADULTS_ELEMENT)
        for adults in range(self.config.number_of_adults - 1): #por padrão, o site já vem com 1 adulto
            self.robot.click_element_when_clickable(ADD_NUMBER_OF_ADULTS_BUTTON)

        for children in range(self.config.number_of_children):
            self.robot.click_element_when_clickable(NUMBER_OF_CHILDREN_BUTTON)

    def select_dates(self):
        self.logger.info("Select departure and return dates")
        self.robot.input_text(DEPARTURE_DATE_INPUT, self.config.departure_date)
        self.robot.press_keys(DEPARTURE_DATE_INPUT, "ENTER")

        self.robot.input_text(RETURN_DATE_INPUT, self.config.return_date)
        self.robot.press_keys(RETURN_DATE_INPUT, "ENTER")

    def make_search(self):
        self.select_route()
        self.select_cities()
        self.select_number_of_passengers()
        self.select_dates()

        self.robot.click_element_when_clickable(ACCEPT_COOKIES_BUTTON)
        self.robot.click_element_when_clickable(SUBMIT_BUTTON)

    def select_outbound_flight(self):
        self.logger.info("Select outbound flight")
        time.sleep(10)
        flight_results_elements = self.robot.get_webelements(FLIGHTS_RESULTS)
        for element in flight_results_elements:
            origination = element.find_element(By.XPATH, ORIGINATION_XPATH).text
            destination = element.find_element(By.XPATH, DESTINATION_XPATH).text
            flight_info = FlightInfo(
                type = "outbound",
                origination=origination,
                destination=destination,
                duration=element.find_element(By.XPATH, DESTINATION_XPATH).text,
                price=element.find_element(By.XPATH, PRICE_XPATH).text,
                departure_time=origination.split("-")[1].strip(),
                arrival_time = destination.split("-")[1].strip(),
                route=element.find_element(By.XPATH, ROUTE_XPATH).text,
                airline='Gol'
                )
            self.outbound_flights.append(flight_info)
            time.sleep(1)
        self.robot.click_element_when_clickable(FLIGHT_XPATH)
        self.logger.info("outbound flight selected")
        time.sleep(1)
        self.logger.info("submit outbound flight")
        self.robot.click_button(FLIGHT_SUBMIT_BUTTON)

    def select_return_flight(self):
        self.logger.info("Select return flight")
        time.sleep(10)
        flights_elements = self.robot.get_webelements(FLIGHTS_RESULTS)
        for element in flights_elements:
            origination = element.find_element(By.XPATH, ORIGINATION_XPATH).text
            destination = element.find_element(By.XPATH, DESTINATION_XPATH).text
            flight_info = FlightInfo(
                type = "return",
                origination=origination,
                destination=destination,
                duration=element.find_element(By.XPATH, DURATION_XPATH).text,
                price=element.find_element(By.XPATH, PRICE_XPATH).text,
                departure_time=origination.split("-")[1].strip(),
                arrival_time = destination.split("-")[1].strip(),
                route=element.find_element(By.XPATH, ROUTE_XPATH).text,
                airline='Gol'
                )
            self.return_flights.append(flight_info)

    def select_cheapest_flight(self, flights: List[FlightInfo]) -> FlightInfo:
        return min(flights, key=lambda flight: flight.price)

    def release_the_spider(self) -> Result:
        try:
            self.logger.info("Start VoeGol scrapper")

            self.robot.open_available_browser(self.url, headless=True)
            self.make_search()
            self.select_outbound_flight()
            self.select_return_flight()
            self.logger.info(self.outbound_flights)
            self.logger.info(self.return_flights)
            self.logger.info("Finished")
            self.robot.close_all_browsers()

            return Result(
                outbound_flights=self.outbound_flights,
                return_flights=self.return_flights,
                datetime=str(datetime.now()),
                outbound_cheapest_flight = self.select_cheapest_flight(self.outbound_flights),
                return_cheapest_flight = self.select_cheapest_flight(self.return_flights)
            )

        except Exception as error:
            self.robot.close_all_browsers()
            self.logger.error(error)
            raise error
