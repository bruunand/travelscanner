from enum import Enum, IntEnum
from datetime import datetime
from travelscanner.errors import DateExceededException


class Countries(IntEnum):
    UNKNOWN = 0
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
    UK = 12
    LATVIA = 13
    GERMANY = 14
    BELGIUM = 15
    TURKEY = 16
    POLAND = 17
    AUSTRIA = 18
    HUNGARY = 19
    CZECH_REPUBLIC = 20
    NETHERLANDS = 21
    USA = 22
    UAE = 23
    IRELAND = 24
    HONG_KONG = 25
    SWEDEN = 26
    MOROCCO = 27
    ISRAEL = 28
    MONTENEGRO = 29
    ICELAND = 30
    TANZANIA = 31
    INDONESIA = 32
    JAPAN = 33
    SRI_LANKA = 34
    DOMINICAN_REPUBLIC = 35
    MAURITIUS = 36
    MEXICO = 37
    MALDIVES = 38
    MALAYSIA = 39
    SEYCHELLES = 40
    BULGARIA = 41
    LITHUANIA = 42
    SINGAPORE = 43
    VIETNAM = 44
    CUBA = 45
    BARBADOS = 46
    BRAZIL = 47
    INDIA = 48
    ARUBA = 49
    TUNISIA = 50
    JORDAN = 51


class Airports(IntEnum):
    UNKNOWN = 0
    AALBORG = 1
    BILLUND = 2
    COPENHAGEN = 3


class MealTypes(IntEnum):
    UNKNOWN = 0
    NONE = 1
    NOT_SPECIFIED = 2
    BREAKFAST = 3
    HALF_BOARD = 4
    FULL_BOARD = 5
    ALL_INCLUSIVE = 6


class RoomTypes(IntEnum):
    UNKNOWN = 0
    APARTMENT = 1
    DOUBLE_ROOM = 2
    ECONOMY = 3
    STANDARD_ROOM = 4
    FAMILY = 5
    TWO_PERSON_ROOM = 6
    PREMIUM = 7
    TENT = 8
    BUNGALOW = 9


class TravelOptions(object):
    def __init__(self):
        # Price information
        self.min_price = None
        self.max_price = None

        # Country information
        self.destination_countries = None
        self.departure_airports = None

        # Date and duration information
        self.earliest_departure_date = datetime.today()
        self.maximum_days_from_departure = None
        self.duration_days = None

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
