import json
from datetime import datetime
from json import JSONDecodeError

import re
from urllib.parse import unquote, parse_qs, urlparse
import requests
from logging import getLogger

from travelscanner.crawlers.threaded_crawler import crawl_multi_threaded
from travelscanner.models.travel import Travel
from travelscanner.options.travel_options import Airports, Countries, MealTypes, RoomTypes, Vendors, TravelOptions
from travelscanner.crawlers.crawler import Crawler, join_values, log_on_failure, get_default_if_none, Crawlers
from travelscanner.models.price import Price


class Travelmarket(Crawler):
    BaseUrl = "https://www.travelmarket.dk/"
    ScanUrl = BaseUrl + "tmcomponents/modules/tm_charter/public/ajax/charter_v7_requests.cfm"
    DateFormat = "%Y-%m-%d"
    UrlRegex = re.compile(r'&url=(.*?)')

    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708",
                                   Airports.COPENHAGEN: "500055"}
        self.country_dictionary = {Countries.CAPE_VERDE: "500104", Countries.CYPRUS: "500122",
                                   Countries.EGYPT: "500297", Countries.FRANCE: "500439", Countries.GREECE: "500575",
                                   Countries.MALTA: "501574", Countries.PORTUGAL: "502079", Countries.SPAIN: "500347",
                                   Countries.THAILAND: "502685", Countries.UK: "500481"}
        self.current_departure_date = datetime.today()

    def set_agent(self, agent):
        super().set_agent(agent)

        # Warn about options that cannot be satisfied
        if not self.get_options().number_of_guests is None:
            getLogger().warning(f"Number of guests option cannot be satisfied by {self.__class__.__name__}")

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
        return self.current_departure_date.strftime(Travelmarket.DateFormat)

    def get_flex_days(self):
        return TravelOptions.TIMEDELTA.days

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
        try:
            result = self.post(page)
            data = json.loads(result.text)
        except JSONDecodeError as error:
            getLogger().error(f"Unable to parse JSON ({result.status_code}): {result.text}, {error}")

            return travels

        for item in data['HOTELS']:
            # Instantiate and add travel
            travel = Travel(crawler=int(self.get_id()), vendor=Vendors.parse_da(item['COMPANY']['NAME']),
                            country=Countries.parse_da(item['COUNTRY']), area=item['DESTINATION'],
                            hotel_stars=item['STARS'], duration_days=item['DURATION'],
                            departure_date=Travelmarket.parse_date(item['DEPARTUREDATE']).date(),
                            has_pool=item['HASPOOL'] == 1, hotel=item['HOTELNAME'],
                            departure_airport=Airports.parse_da(item['DEPARTURE']),
                            has_childpool=item['HASCHILDPOOL'] == 1)

            # Add prices
            for price in item['PRICES']:
                link = price['BOOKINGSTATLINK']
                if "&url=" in link:
                    queries = parse_qs(urlparse(link).query)

                    if 'url' in queries:
                        link = queries['url'][0]

                travel.add_price(Price(price=price['PRICE'], all_inclusive=price['ISALLINCLUSIVE'] == 1,
                                       room=RoomTypes.parse_da(price['ROOMTYPE']), travel=travel,
                                       meal=MealTypes.parse_da(price['MEALTYPE']), link=link))
            # Add travel
            travels.add(travel)

        return travels

    def get_id(self):
        return Crawlers.TRAVELMARKET

    def crawl(self, current_departure_date):
        self.current_departure_date = current_departure_date

        return crawl_multi_threaded(crawl_function=self.get_travels, start_page=1, max_workers=30)
