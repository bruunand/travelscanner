class Travel(object):
    UNKNOWN = "UNKNOWN"

    def __init__(self, scanner, prices, vendor=UNKNOWN, country=UNKNOWN, hotel_name=UNKNOWN, hotel_stars=None, area=UNKNOWN, duration_days=None, departure_date=None, departure_airport=UNKNOWN):
        self.scanner = scanner
        self.prices = prices
        self.vendor = vendor
        self.country = country
        self.hotel_name = hotel_name
        self.area = area
        self.hotel_stars = hotel_stars
        self.tripadvisor_rating = None
        self.duration_days = duration_days
        self.departure_date = departure_date
        self.departure_airport = departure_airport

    def get_tripadvisor_rating(self):
        pass

    def get_lowest_price(self):
        lowest_price = None
        
        for price in self.prices:
            if (lowest_price is None or price.price < lowest_price):
                lowest_price = price.price

        return lowest_price

    def __hash__(self):
        return hash((self.hotel_name, self.country, self.area, self.departure_date, self.departure_airport, self.scanner.get_alias()))
    
    def __str__(self):
        return f"{self.hotel_name} in {self.area}, {self.country} for {self.get_lowest_price()} DKK. {self.duration_days} days departing on {self.departure_date} from {self.departure_airport}."
    