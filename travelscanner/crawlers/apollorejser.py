import asyncio
import concurrent
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import parse_qsl, urlsplit

from bs4 import BeautifulSoup

import json
import requests

from travelscanner.crawlers.crawler import Crawler, Crawlers
from travelscanner.options.travel_options import Airports, Countries, RoomTypes

import xml.etree.ElementTree as ET

from logging import getLogger


class Apollorejser(Crawler):
    BaseUrl = "http://ksb.apollorejser.dk/huvudsidor/lastmin"
    DateFormat = "%y%m%d"
    ThreadedWorkers = 30
    FlightDateFormat = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: 'aal', Airports.COPENHAGEN: 'cph', Airports.BILLUND: 'bll',
                                   Airports.ODENSE: 'ode', Airports.KRARUP: 'krp', Airports.AARHUS: 'aar'}

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, Apollorejser.DateFormat)

    @staticmethod
    def parse_flight_date(date):
        return datetime.strptime(date, Apollorejser.FlightDateFormat)

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

        with ThreadPoolExecutor(max_workers=Apollorejser.ThreadedWorkers) as executor:
            futures = []

            for offer in offers.iter("offer"):
                # Skip if unspecified travel or flight
                if offer.find('type').text != 'hotel':
                    continue

                # Extract offer information
                guests = int(offer.find('numAdultPassengers').text)
                price = int(offer.find('price').text) * guests
                duration = int(offer.find('duration').text)
                departure_date = Apollorejser.parse_date(offer.find('date').text)
                country = Countries.parse_da(offer.find('country').text)
                hotel = offer.find('hotel').text
                url = offer.find('url').text

                # Compare against duration requirement
                if self.get_options().min_duration_days is not None and duration < self.get_options().min_duration_days:
                    continue

                # Compare price against requirements
                min_price, max_price = self.get_options().min_price, self.get_options().max_price
                if (min_price is not None and price < min_price) or (max_price is not None and price > max_price):
                    continue

                futures.append(executor.submit(self.get_offer_details, url, guests, price, duration, departure_date,
                                               country, hotel))

            for future in futures:
                result = future.result()

                if result is not None:
                    travels.add(result)

        print(travels)

        return travels

    def get_duration_group_code(self, url):
        query_dict = Crawler.parse_url_query(url)
        if 'durationGroupCode' in query_dict:
            return query_dict['durationGroupCode']
        else:
            getLogger().error('Failed to retrieve duration group code')

            return None

    def get_hotel_rating(self, soup):
        classification_tag = soup.find('i', attrs={'class': 'classification'})
        if classification_tag:
            for class_name in classification_tag.attrs['class']:
                if not class_name.startswith('value'):
                    continue

                # Take the last two digits of the string and divide by 10 to get proper rating
                # E.g. the class value35 results in a rating of 3.5
                return int(class_name[-2:]) / 10

        getLogger().error('Failed to retrieve hotel rating')

        return None

    def get_is_property_checked(self, soup, property_class):
        property_tag = soup.find('div', attrs={'class': property_class})
        if property_tag:
            checkbox_tag = property_tag.find('i', attrs={'class': 'icon-sprite'})
            if checkbox_tag:
                return 'icon-checked' in checkbox_tag.attrs['class']

        getLogger().error('Failed to determine value of property with class %s', property_class)

        return None

    def get_fact(self, soup, fact_class):
        fact_tag = soup.find('div', attrs={'class': fact_class})
        if fact_tag:
            value_tag = fact_tag.find('span', attrs={'class': 'fact_value'})
            if value_tag:
                return value_tag.text

        getLogger().error('Failed to determine value of fact with class %s', fact_class)

        return None

    def get_initial_data(self, url):
        landing_page = requests.get(url, headers=Crawler.BaseHeaders)
        required_keys = ['hotel_rating', 'duration_group_code', 'has_pool', 'has_childpool']

        # Parse HTML of booking page
        soup = BeautifulSoup(landing_page.text, 'html.parser')

        # Get return values
        return_values = {'hotel_rating': self.get_hotel_rating(soup),
                         'duration_group_code': self.get_duration_group_code(landing_page.url),
                         'has_pool': self.get_is_property_checked(soup, 'pool_type_pool'),
                         'has_bar': self.get_is_property_checked(soup, 'restaurant_bar'),
                         'has_childpool': self.get_is_property_checked(soup, 'pool_type_children_s_pool'),
                         'internet_in_rooms': self.get_is_property_checked(soup, 'facilities_internet_in_rooms'),
                         'distance_beach': self.get_fact(soup, 'distance_to_beach'),
                         'distance_center': self.get_fact(soup, 'distance_to_center')}

        # If any of the dictionary values is None, return None
        for key, value in return_values.items():
            if value is None and key in required_keys:
                return None

        return return_values


    def get_duration_group(self, booking_page):
        # Extract duration group from redirected URL
        # The duration group code is typically the duration, but in a few cases some random number
        query_dict = Crawler.parse_url_query(booking_page.url)
        if 'durationGroupCode' in query_dict:
            return query_dict['durationGroupCode']

        getLogger().error("Failed to retrieve duration group code")

        return None

    def get_meal_data(self, product_code):
        print(product_code)

    def get_flight_data(self, query_dict, duration_group):
        flight_query = {'productCategoryCode': query_dict['productCategoryCode'],
                        'departureAirportCode': query_dict['departureAirportCode'],
                        'departureDate': query_dict['departureDate'],
                        'durationGroupCode': duration_group,
                        'hotelId': query_dict['travelAreaCode'] + query_dict['hotelCode'],
                        'paxAges': query_dict['paxAges']}

        flight_data = requests.get("https://www.apollorejser.dk/api/Flight/Flights",
                                   params=flight_query, headers=Crawler.BaseHeaders).text
        flight_json = json.loads(flight_data)

        # Get preselected package identifier
        if 'PreselectedFlightPackageCode' in flight_json:
            preselected_code = flight_json['PreselectedFlightPackageCode']

            # Then return flight information from that package
            if 'FlightPackages' in flight_json:
                for package in flight_json['FlightPackages']:
                    if package['FlightPackageCode'] != preselected_code:
                        continue

                    # Both information about inbound and outbound flights are saved
                    outbound = package['Outbound']
                    inbound = package['Inbound']

                    # TODO: Parse as dates
                    return {'inbound_depature': Apollorejser.parse_flight_date(inbound['DepartureDateTime']),
                            'inbound_arrival': Apollorejser.parse_flight_date(inbound['ArrivalDateTime']),
                            'outbound_departure': Apollorejser.parse_flight_date(outbound['DepartureDateTime']),
                            'outbound_arrival': Apollorejser.parse_flight_date(outbound['ArrivalDateTime']),
                            'flight_package': preselected_code}

        getLogger().error("Failed to retrieve flight data (HotelId: %s)",
                          query_dict['travelAreaCode'] + query_dict['hotelCode'])

        return None

    def get_rooms(self, query_dict, flight_package_code):
        room_query = {'productCategoryCode': query_dict['productCategoryCode'],
                      'hotelId': query_dict['travelAreaCode'] + query_dict['hotelCode'],
                      'paxAges': query_dict['paxAges'],
                      'flightPackageCode':flight_package_code}
        room_data = requests.get("https://www.apollorejser.dk/api/RoomType/FindAvailableRoomTypes", params=room_query,
                                 headers=Crawler.BaseHeaders).text
        room_json = json.loads(room_data)

        # Sort rooms by price to avoid duplicates
        sorted_rooms = sorted(room_json, key=lambda r: r['CurrentTotalPrice'])

        # Iterate over rooms and add to collection
        rooms = []
        for room in sorted_rooms:
            # Parse room type
            room_type = RoomTypes.parse_da(room['RoomTypeName'])

            # Different configurations specify the amount of beds, rooms etc.
            # Not all vendors support this, so we just take the cheapest configuration
            alternatives = []
            for configuration in room['RoomConfigurations']:
                for alternative in configuration['Alternatives']:
                    alternatives.append({'type': room['RoomTypeName'], 'price': alternative['Price'],
                                         'code': alternative['ProductCode'], 'subtype': alternative['SubRoomTypeName']})

            # Add alternative with cheapest price
            if alternatives:
                rooms.append(min(alternatives, key=lambda a: a['price']))

        return rooms

    def get_offer_details(self, url, guests, price, duration_days, departure_date, country, hotel):
        # Parse URL query
        query_dict = Crawler.parse_url_query(url)

        # Retrieve booking page information (rating and duration group)
        initial_data = self.get_initial_data(url)
        if initial_data is None:
            return None

        # Retrieve flight information
        flight_data = self.get_flight_data(query_dict, initial_data['duration_group_code'])
        if flight_data is None:
            return None

        # Retrieve room information
        rooms = self.get_rooms(query_dict, flight_data['flight_package'])

        # Retrieve meal information from each room
        for room in rooms:
            self.get_meal_data(room['code'])

        return initial_data['hotel_rating']
