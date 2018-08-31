from datetime import datetime
from urllib.parse import parse_qsl, urlsplit

import requests

from travelscanner.crawlers.crawler import Crawler, Crawlers
from travelscanner.options.travel_options import Airports, Countries

import xml.etree.ElementTree as ET


class Apollorejser(Crawler):
    BaseUrl = "http://ksb.apollorejser.dk/huvudsidor/lastmin" #aal_cms2.xml
    DateFormat = "%y%m%d"

    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: 'aal', Airports.COPENHAGEN: 'cph', Airports.BILLUND: 'bll'}

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, Apollorejser.DateFormat)

    def get_crawler_identifier(self):
        return Crawlers.APOLLOREJSER

    ''' Note that the crawl function for Apollo ignores the from date, since all travels are in one XML document'''
    def crawl(self, from_date):
        travels = set()

        airports = self.agent.get_travel_options().departure_airports

        # Include all departure airports in search if none selected in agent
        if airports is None:
            airports = self.airport_dictionary.keys()

        for airport in airports:
            if airport in self.airport_dictionary:
                travels.update(self.get_travels(airport))

        return travels

    def get_travels(self, airport):
        travels = set()
        data = requests.get(f'{Apollorejser.BaseUrl}/{self.airport_dictionary[airport]}_cms2.xml',
                            headers=Crawler.BaseHeaders).text

        # Parse XML data
        offers = ET.fromstring(data)
        if offers is None:
            return travels

        for offer in offers.iter("offer"):
            # Skip if unspecified travel or flight
            if offer.find('type').text != 'hotel':
                continue

            # Extract offer information
            guests = int(offer.find('numAdultPassengers').text)
            price = int(offer.find('price').text) * guests
            duration_days = int(offer.find('duration').text)
            departure_date = Apollorejser.parse_date(offer.find('date').text)
            country = Countries.parse_da(offer.find('country').text)
            url = offer.find('url').text

            # Compare against duration requirement
            if self.get_options().min_duration_days is not None and duration_days < self.get_options().min_duration_days:
                continue

            # Compare price against requirements (note that total price is calculated)
            min_price, max_price = self.get_options().min_price, self.get_options().max_price
            if (min_price is not None and price < min_price) or (max_price is not None and price > max_price):
                continue

            travels.update(self.get_offer_details(url, guests, price, duration_days, departure_date, country))

        return travels

    def get_offer_details(self, url, guests, price, duration_days, departure_date, country):
        travels = set()

        # Parse URL query
        query_dict = dict(parse_qsl(urlsplit(url).query))

        return travels
