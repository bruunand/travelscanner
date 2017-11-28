import json
import requests
from scanner import Scanner, join_values, log_on_failure
from travel_options import Airports, Countries


class TravelMarketScanner(Scanner):
    BaseUrl = "https://www.travelmarket.dk/"
    ScanUrl = BaseUrl + "tmcomponents/modules/tm_charter/public/ajax/charter_v7_requests.cfm"

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
        return 0 if self.get_options().minimum_hotel_stars is None else self.get_options().minimum_hotel_stars

    def get_departure(self):
        return self.get_options().earliest_departure_date.strftime('%Y-%m-%d')

    def get_flex_days(self):
        return 0 if self.get_options().maximum_days_from_departure is None else self.get_options().maximum_days_from_departure

    def synthesize_filter_json(self, page):
        filters = dict(bSpecified=True, bUnspecified=False, strKeyDestination="", sHotelName="",
                       bAllInclusive=self.get_all_inclusive(),
                       bFlightOnly=False, bPool=0, bChildPool=0, nCurrentPage=page, nSortBy=1,
                       nMinStars=self.get_minimum_stars(), nMatrixWeek=0, nMatrixPrice=0, lDestinations="",
                       lSubAreas="", lAreas="", lSuppliers="",
                       lDepartures=join_values(self.get_options().departure_airports, self.airport_dictionary, ","),
                       lDeparture=self.get_departure(), lDurations=self.get_duration(),
                       lCountries=join_values(self.get_options().destination_countries, self.country_dictionary, ","),
                       flexdays=self.get_flex_days())

        return json.dumps(filters)

    def post(self, page):
        data = {"action": "getListJSON", "filters": self.synthesize_filter_json(page),
                "dDeparture": self.get_departure(), "sLanguage": "DK"}

        return requests.post(TravelMarketScanner.ScanUrl, data=data, headers=Scanner.BaseHeaders)

    @log_on_failure
    def scan(self):
        print(self.post(1).text)
