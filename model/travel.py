class Travel(object):
    def __init__(self, scanner, vendor="Unknown", country="Unknown", hotel_name="Unknown", hotel_stars=None, lowest_price=None, area="Unknown", duration_days=None, departure=None):
        self.scanner = scanner
        self.vendor = vendor
        self.country = country
        self.hotel_name = hotel_name
        self.lowest_price = lowest_price
        self.area = area
        self.hotel_stars = hotel_stars
        self.tripadvisor_rating = None
        self.duration_days = duration_days
        self.departure = departure

    def get_hash(self):
        return (self.hotel_name, self.country, self.scanner.get_alias()).__hash__()

    def get_tripadvisor_rating(self):
        pass

    def __str__(self):
        return "{0} in {1}, {2} for {3} DKK. {4} days departing on {5}.".format(self.hotel_name, self.area, self.country, self.lowest_price, self.duration_days, self.departure)