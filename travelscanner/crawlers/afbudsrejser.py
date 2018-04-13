from json import JSONDecodeError

import requests
from datetime import datetime
from logging import getLogger

from flask import json

from travelscanner.crawlers.crawler import Crawler, join_values, log_on_failure, get_default_if_none, Crawlers
from travelscanner.crawlers.threaded_crawler import crawl_multi_threaded
from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.options.travel_options import Airports, Countries, TravelOptions, RoomTypes, MealTypes, Vendors


class Afbudsrejser(Crawler):
    BaseUrl = "http://www.afbudsrejser.dk/"
    ScanUrl = BaseUrl + "charter.json"
    DateFormat = "%Y-%m-%d"
    DateTimeFormat = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: 'AAL', Airports.BILLUND: 'BLL', Airports.COPENHAGEN: 'CPH'}
        self.country_dictionary = {Countries.SPAIN: 19841, Countries.GREECE: 19862, Countries.TURKEY: 19999,
                                   Countries.CYPRUS: 19828, Countries.BULGARIA: 19795}
        self.current_departure_date = datetime.today()

    def set_agent(self, agent):
        super().set_agent(agent)

        # Warn about options that cannot be satisfied
        if not self.get_options().number_of_guests is None:
            getLogger().warning(f"Number of guests option cannot be satisfied by {self.__class__.__name__}")

        if not self.get_options().min_price is None:
            getLogger().warning(f"Minimum price option cannot be satisfied by {self.__class__.__name__}")

    def get_duration(self):
        return get_default_if_none(self.get_options().duration_days, "")

    def get_minimum_stars(self):
        return get_default_if_none(self.get_options().minimum_hotel_stars, "1")

    def get_departure_date(self):
        return self.current_departure_date.strftime(Afbudsrejser.DateFormat)

    def get_flex_days(self):
        return TravelOptions.TIMEDELTA.days

    def get_max_price(self):
        return get_default_if_none(self.get_options().max_price, "")

    def get_countries(self):
        if self.get_options().destination_countries is None:
            return ''
        else:
            return join_values(self.get_options().destination_countries, self.country_dictionary, "-")

    def get_departure_airports(self):
        if self.get_options().departure_airports is None:
            return ''
        else:
            return join_values(self.get_options().departure_airports, self.airport_dictionary, ",")

    def get_id(self):
        return Crawlers.AFBUDSREJSER

    def synthesize_params(self, page):
        facilities = []

        if self.get_options().all_inclusive:
            facilities.append("all_inclusive")

        return dict(dest=self.get_countries(), duration=self.get_duration(), edepdate=self.get_departure_date(),
                    rating=self.get_minimum_stars(), sort='date', facilities='-'.join(facilities),
                    price=self.get_max_price(), orig=self.get_departure_airports(), page=page,
                    delta=TravelOptions.TIMEDELTA.days)

    def get_page(self, page):
        return requests.get(Afbudsrejser.ScanUrl, params=self.synthesize_params(page), headers=Crawler.BaseHeaders)

    @log_on_failure
    def get_travels(self, page):
        travels = set()
        try:
            result = self.get_page(page)
            data = json.loads(result.text)
        except JSONDecodeError as error:
            getLogger().error(f"Unable to parse JSON ({result.status_code}): {result.text}, {error}")

            return travels

        for item in data['offers']:
            facilities = item['metabool']
            has_childpool = 'childspool' in facilities
            has_pool = 'pool' in facilities
            all_inclusive = 'all_inclusive' in facilities

            # Instantiate travel
            travel = Travel(crawler=int(self.get_id()), vendor=Vendors.parse_da(item['supplier']['name']),
                            country=Countries.parse_da(item['destination']['country_name']), area=item['destination']['name'],
                            hotel_stars=item['hotel']['rating'], duration_days=item['number_of_nights'] + 1,
                            departure_date=Afbudsrejser.parse_datetime(item['origin']['dt']).date(),
                            has_pool=has_pool, hotel=item['hotel']['name'],
                            departure_airport=Airports.parse_da(item['origin']['airport_name']),
                            has_childpool=has_childpool)

            # Add price
            travel.add_price(Price(price=item['price'], all_inclusive=all_inclusive, link=item['booking_url'],
                                   room=RoomTypes.parse_da(item['hotel']['room_name']), travel=travel,
                                   meal=MealTypes.ALL_INCLUSIVE if all_inclusive else MealTypes.UNKNOWN))

            # Add travel
            travels.add(travel)

        return travels

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, Afbudsrejser.DateFormat)

    @staticmethod
    def parse_datetime(date):
        return datetime.strptime(date, Afbudsrejser.DateTimeFormat)

    @log_on_failure
    def crawl(self, current_departure_date):
        self.current_departure_date = current_departure_date

        return crawl_multi_threaded(crawl_function=self.get_travels, start_page=1, max_workers=30)
