from enum import Enum
from datetime import datetime
from errors import DateExceededException


class Countries(Enum):
    CAPE_VERDE = 1
    CROATIA = 2
    CYPRUS = 3
    EGYPT = 4
    FRANCE = 5
    GREECE = 6
    ITALY = 7
    MALTA = 8
    PORTUGAL = 9
    SPAIN = 10
    THAILAND = 11
    UNITED_KINGDOM = 12


class Airports(Enum):
    AALBORG = 1
    BILLUND = 2
    COPENHAGEN = 3


class TravelOptions(object):
    def __init__(self):
        # Price information
        self.min_price = None
        self.max_price = None

        # Country information
        self.destination_countries = []
        self.departure_airports = []

        # Date and duration information
        self.earliest_departure_date = datetime.today()
        self.maximum_days_from_departure = None
        self.duration_days = 7

        # Hotel information
        self.minimum_hotel_stars = None
        self.minimum_tripadvisor_rating = None
        self.all_inclusive = False

        # Guest information
        self.number_of_guests = None

    def set_earliest_departure_date(self, date_string):
        self.earliest_departure_date = datetime.strptime(date_string, '%d/%m/%Y')
        delta_time = datetime.today() - self.earliest_departure_date

        if delta_time.days > 0:
            raise DateExceededException(delta_time)
