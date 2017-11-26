from abc import ABCMeta, abstractmethod
from travel_options import Airports, Countries
import json


def search_dictionary(source, needles, haystack):
    for item in needles:
        if not haystack.__contains__(item):
            print("{0} is not supported by {1}, will be skipped.".format(item, source.__class__.__name__))


def join_dictionary_values(keys, dictionary, separator):
    values = []

    for key in keys:
        if dictionary.__contains__(key):
            values.append(dictionary[key])

    return separator.join(values)


def log_on_failure(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exception:
            print("Error in {0}: {1}".format(func.__qualname__, exception))

    return wrapper


class Scanner(metaclass=ABCMeta):
    def __init__(self):
        self.agent = None

        # Dictionaries used to convert values by different platforms
        self.airport_dictionary = {}
        self.country_dictionary = {}

    @abstractmethod
    def scan(self):
        pass

    def set_agent(self, agent):
        self.agent = agent

        # Print items missing in own dictionaries
        # This is to inform the user of any desired options that cannot be fulfilled by certain scanners
        search_dictionary(self, self.get_options().destination_countries, self.country_dictionary)
        search_dictionary(self, self.get_options().departure_airports, self.airport_dictionary)

    def get_options(self):
        return self.agent.travel_options


class TravelMarketScanner(Scanner):
    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708", Airports.COPENHAGEN: "500055"}
        self.country_dictionary = {Countries.CAPE_VERDE: "500104", Countries.CYPRUS: "500122",
                                   Countries.EGYPT: "500297", Countries.FRANCE: "500439", Countries.GREECE: "500575",
                                   Countries.MALTA: "501574", Countries.PORTUGAL: "502079", Countries.SPAIN: "500347",
                                   Countries.THAILAND: "502685", Countries.UNITED_KINGDOM: "500481"}

    def get_duration(self):
        duration_days = self.get_options().duration_days

        if duration_days is not None:
            if duration_days < 7:
                return '1'
            elif duration_days < 14:
                return '2'
            elif duration_days < 21:
                return '3'

        return ''

    def get_all_inclusive(self):
        return 1 if self.get_options().all_inclusive else 0

    def get_minimum_stars(self):
        return 0 if self.get_options().minimum_hotel_stars is None else self.get_options().minimum_hotel_stars

    def get_departure(self):
        return self.get_options().earliest_departure_date.strftime('%Y-%m-%d')

    def get_flex_days(self):
        return 0 if self.get_options().maximum_days_from_departure is None else self.get_options().maximum_days_from_departure

    def synthesize_filter_json(self, page):
        filters = {"bSpecified": True,
                   "strKeyDestination": "",
                   "sHotelName": "",
                   "bAllInclusive": self.get_all_inclusive(),
                   "bFlightOnly": False,
                   "bPool": 0,
                   "bChildPool": 0,
                   "nCurrentPage": page,
                   "nSortBy": 1,
                   "nMinStars": self.get_minimum_stars(),
                   "nMatrixWeek": 0,
                   "nMatrixPrice": 0,
                   "lDestinations": "",
                   "lSubAreas": "",
                   "lAreas": "",
                   "lSuppliers": "",
                   "lDepartures": join_dictionary_values(self.get_options().departure_airports,
                                                         self.airport_dictionary, ","),
                   "lDeparture": self.get_departure(),
                   "lDurations": self.get_duration(),
                   "lCountries": join_dictionary_values(self.get_options().destination_countries,
                                                        self.country_dictionary, ","),
                   "flexdays": self.get_flex_days()}

        return json.dumps(filters)

    @log_on_failure
    def scan(self):
        pass


class AfbudsrejserScanner(Scanner):
    @log_on_failure
    def scan(self):
        pass


class SpiesScanner(Scanner):
    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708", Airports.COPENHAGEN: "500055"}

    @log_on_failure
    def scan(self):
        pass
