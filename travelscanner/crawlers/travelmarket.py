import json
from datetime import datetime

import requests
from logging import getLogger

from travelscanner.models.travel import Travel
from travelscanner.options.travel_options import Airports, Countries, MealTypes
from travelscanner.crawlers.crawler import Crawler, join_values, log_on_failure, get_default_if_none, Crawlers
from travelscanner.models.price import Price


class Travelmarket(Crawler):
    BaseUrl = "https://www.travelmarket.dk/"
    ScanUrl = BaseUrl + "tmcomponents/modules/tm_charter/public/ajax/charter_v7_requests.cfm"
    DateFormat = "%Y-%m-%d"

    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708",
                                   Airports.COPENHAGEN: "500055"}
        self.country_dictionary = {Countries.CAPE_VERDE: "500104", Countries.CYPRUS: "500122",
                                   Countries.EGYPT: "500297", Countries.FRANCE: "500439", Countries.GREECE: "500575",
                                   Countries.MALTA: "501574", Countries.PORTUGAL: "502079", Countries.SPAIN: "500347",
                                   Countries.THAILAND: "502685", Countries.UK: "500481"}

    def set_agent(self, agent):
        super().set_agent(agent)

        # Warn about options that cannot be satisfied
        if not self.get_options().number_of_guests is None:
            getLogger().warning(f"Number of guests option cannot be satisfied by {self.__class__.__name__}.")

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
        return get_default_if_none(self.get_options().minimum_hotel_stars, 0)

    def get_departure_date(self):
        return self.get_options().earliest_departure_date.strftime(Travelmarket.DateFormat)

    def get_flex_days(self):
        return get_default_if_none(self.get_options().maximum_days_from_departure, 0)

    def get_min_price(self):
        return get_default_if_none(self.get_options().min_price, 0)

    def get_max_price(self):
        return get_default_if_none(self.get_options().max_price, 0)

    def get_countries(self):
        if self.get_options().destination_countries is None:
            return ''
        else:
            return join_values(self.get_options().destination_countries, self.country_dictionary, ",")

    def get_departure_airports(self):
        if self.get_options().departure_airports is None:
            return ''
        else:
            return join_values(self.get_options().departure_airports, self.airport_dictionary, ",")

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, Travelmarket.DateFormat)

    @staticmethod
    def parse_country(name):
        return Travelmarket.parse(name, {'Spanien': Countries.SPAIN,
                                         'Grækenland': Countries.GREECE,
                                         'Cypern': Countries.CYPRUS,
                                         'Tyskland': Countries.GERMANY,
                                         'Letland': Countries.LATVIA,
                                         'Østrig': Countries.AUSTRIA,
                                         'Polen': Countries.POLAND,
                                         'Belgien': Countries.BELGIUM,
                                         'Storbritannien': Countries.UK,
                                         'Tyrkiet': Countries.TURKEY,
                                         'Frankrig': Countries.FRANCE,
                                         'Ungarn': Countries.HUNGARY,
                                         'Egypten': Countries.EGYPT,
                                         'Italien': Countries.ITALY,
                                         'Tjekkiet': Countries.CZECH_REPUBLIC,
                                         'Holland': Countries.NETHERLANDS,
                                         'USA': Countries.USA,
                                         'Malta': Countries.MALTA,
                                         'Forenede Arabiske Emirater': Countries.UAE,
                                         'Portugal': Countries.PORTUGAL,
                                         'Irland': Countries.IRELAND,
                                         'Hong Kong': Countries.HONG_KONG,
                                         'Thailand': Countries.THAILAND,
                                         'Sverige': Countries.SWEDEN
                                         }, Countries.UNKNOWN)

    @staticmethod
    def parse_airport(name):
        return Travelmarket.parse(name, {'København': Airports.COPENHAGEN,
                                         'Aalborg': Airports.AALBORG,
                                         'Billund': Airports.BILLUND
                                         }, Airports.UNKNOWN)

    @staticmethod
    def parse_meal_type(name):
        return Travelmarket.parse(name, {'Ikke angivet': MealTypes.NOT_SPECIFIED,
                                         'Med morgenmad': MealTypes.BREAKFAST,
                                         'Halvpension': MealTypes.HALF_BOARD,
                                         'Uden pension': MealTypes.NONE,
                                         'All Inclusive': MealTypes.ALL_INCLUSIVE,
                                         '': MealTypes.NONE}, MealTypes.UNKNOWN)

    @staticmethod
    def parse(value, dictionary, default=None):
        ret_val = dictionary.get(value, default)

        if ret_val is default:
            getLogger().warning(f"Unable to parse {value} in {Travelmarket.__name__}.")

        return ret_val

    def synthesize_filters(self, page):
        filters = dict(bSpecified=True, bUnSpecified=False, strKeyDestination="", sHotelName="",
                       bAllinclusive=self.get_all_inclusive(), flexdays=self.get_flex_days(),
                       bFlightOnly=False, bPool=0, bChildPool=0, nCurrentPage=page, nSortBy=1,
                       nMinStars=self.get_minimum_stars(), nMatrixWeek=0, nMatrixPrice=0, lDestinations="",
                       nMinPrice=self.get_min_price(), nMaxPrice=self.get_max_price(), lSubAreas="", lAreas="",
                       lDepartures=self.get_departure_airports(),
                       lDeparture=self.get_departure_date(), lDurations=self.get_duration(), lSuppliers="",
                       lCountries=self.get_countries())

        return json.dumps(filters)

    def post(self, page):
        data = dict(action="getListJSON", filters=self.synthesize_filters(page), dDeparture=self.get_departure_date(),
                    sLanguage="DK", nLanguageID=2, nSupplierId=21)

        return requests.post(Travelmarket.ScanUrl, data=data, headers=Crawler.BaseHeaders)

    @log_on_failure
    def get_travels(self, page):
        travels = set()
        result = json.loads(self.post(page).text)

        for item in result['HOTELS']:
            # Instantiate prices associated with this travel
            prices = set()

            for price in item['PRICES']:
                prices.add(Price(price=price['PRICE'], all_inclusive=price['ISALLINCLUSIVE'] == 1,
                                 meal=Travelmarket.parse_meal_type(price['MEALTYPE']), data_dump=price))

            # Instantiate and add travel
            travels.add(Travel(crawler=self.get_id(), vendor=item['COMPANY']['NAME'], hotel_name=item['HOTELNAME'],
                               country=Travelmarket.parse_country(item['COUNTRY']), area=item['DESTINATION'],
                               hotel_stars=item['STARS'], duration_days=item['DURATION'], data_dump=item,
                               departure_date=Travelmarket.parse_date(item['DEPARTUREDATE']),
                               departure_airport=Travelmarket.parse_airport(item['DEPARTURE']), prices=prices))

        return travels

    def get_id(self):
        return Crawlers.TRAVELMARKET

    def crawl(self):
        all_travels = set()
        current_page = 1

        while True:
            travels = self.get_travels(current_page)

            if travels is None or len(travels) == 0:
                break
            else:
                all_travels.update(travels)

                current_page = current_page + 1

        return all_travels
