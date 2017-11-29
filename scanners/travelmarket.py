import json
import requests
from datetime import datetime
from travel import Travel
from scanner import Scanner, join_values, log_on_failure, get_default_if_none
from travel_options import Airports, Countries


class TravelMarketScanner(Scanner):
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
        return get_default_if_none(self.get_options().minimum_hotel_stars, 0)

    def get_departure(self):
        return self.get_options().earliest_departure_date.strftime(TravelMarketScanner.DateFormat)

    def get_flex_days(self):
        return get_default_if_none(self.get_options().maximum_days_from_departure, 0)

    def get_min_price(self):
        return get_default_if_none(self.get_options().min_price, 0)

    def get_max_price(self):
        return get_default_if_none(self.get_options().max_price, 0)

    def parse_date(date):
        return datetime.strptime(date, TravelMarketScanner.DateFormat)

    def synthesize_filters(self, page):
        filters = dict(bSpecified=True, bUnSpecified=False, strKeyDestination="", sHotelName="",
                       bAllinclusive=self.get_all_inclusive(), flexdays=self.get_flex_days(),
                       bFlightOnly=False, bPool=0, bChildPool=0, nCurrentPage=page, nSortBy=1,
                       nMinStars=self.get_minimum_stars(), nMatrixWeek=0, nMatrixPrice=0, lDestinations="",
                       nMinPrice=self.get_min_price(), nMaxPrice=self.get_max_price(), lSubAreas="", lAreas="",
                       lSuppliers="",
                       lDepartures=join_values(self.get_options().departure_airports, self.airport_dictionary, ","),
                       lDeparture=self.get_departure(), lDurations=self.get_duration(),
                       lCountries=join_values(self.get_options().destination_countries, self.country_dictionary, ","))

        return json.dumps(filters)

    def post(self, page):
        data = dict(action="getListJSON", filters=self.synthesize_filters(page), dDeparture=self.get_departure(),
                    sLanguage="DK", nLanguageID=2, nSupplierId=21)

        return requests.post(TravelMarketScanner.ScanUrl, data=data, headers=Scanner.BaseHeaders)

    @log_on_failure
    def get_travels(self, page):
        travels = []
        result = json.loads(self.post(page).text)

        for item in result['HOTELS']:
            lowest_price = None
            for price in item['PRICES']:
                if lowest_price is None or price['PRICE'] < lowest_price:
                    lowest_price = price['PRICE']

            travel = Travel(country=item['COUNTRY'], vendor=item['COMPANY']['NAME'], hotel_name=item['HOTELNAME'],
                            area=item['DESTINATION'], hotel_stars=item['STARS'], lowest_price=lowest_price,
                            duration_days=item['DURATION'], departure=TravelMarketScanner.parse_date(item['DEPARTUREDATE']))
            travels.append(travel)

        return travels

    def scan(self):
        all_travels = []
        current_page = 1

        while True:
            travels = self.get_travels(current_page)

            if len(travels) == 0:
                break
            else:
                [all_travels.append(travel) for travel in travels]
                current_page = current_page + 1

        for travel in all_travels:
            print(travel)

        print("Found {0} travels.".format(len(all_travels)))
