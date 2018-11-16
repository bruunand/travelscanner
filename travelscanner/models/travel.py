from peewee import CharField, IntegerField, FloatField, PrimaryKeyField, BooleanField, DateField, TextField, \
    DateTimeField

from travelscanner.models.meta import MetaModel
from travelscanner.options.travel_options import Countries


class Travel(MetaModel):
    id = PrimaryKeyField()
    crawler = IntegerField()
    vendor = IntegerField()
    hotel = CharField()
    country = IntegerField()
    area = CharField()
    hotel_rating = FloatField()
    duration_days = IntegerField()
    departure_date = DateField()
    departure_airport = IntegerField()
    guests = IntegerField(default=2)
    has_pool = BooleanField()
    has_childpool = BooleanField(null=True)
    has_bar = BooleanField(null=True)
    internet_in_rooms = BooleanField(null=True)
    distance_city = CharField(null=True)
    distance_beach = CharField(null=True)
    outbound_departure_date = DateTimeField(null=True)
    outbound_arrival_date = DateTimeField(null=True)
    inbound_departure_date = DateTimeField(null=True)
    inbound_arrival_date = DateTimeField(null=True)
    link = TextField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prices = set()

    def __hash__(self):
        return hash((self.hotel, self.area, self.country, self.departure_date, self.departure_airport,
                     self.crawler, self.guests, self.duration_days, self.hotel_rating, self.vendor))

    def upsert(self):
        """ Returns the amount of newly inserted travels"""
        # Skip entries which have no country specified
        if self.country == Countries.UNKNOWN:
            return 0

        existing = Travel.select().where(Travel.departure_airport == self.departure_airport,
                                         Travel.guests == self.guests, Travel.crawler == self.crawler,
                                         Travel.departure_date == self.departure_date, Travel.country == self.country,
                                         Travel.hotel_rating == self.hotel_rating, Travel.hotel == self.hotel,
                                         Travel.vendor == self.vendor, Travel.duration_days == self.duration_days,
                                         Travel.area == self.area).first()

        if existing is None:
            return self.save()
        else:
            existing.prices = self.prices
            return existing.save()

    def save(self, force_insert=False, only=None):
        super().save(force_insert, only)

        created_sum = 0
        for price in self.prices:
            price.travel = self
            created_sum = created_sum + price.upsert()

        return created_sum

    '''Ensure that duplicate prices are not added and always add the lowest price'''
    def add_price(self, new):
        for existing in self.prices:
            if existing.meal == new.meal and existing.room == new.room and existing.sub_room == new.sub_room:
                if new.price < existing.price:
                    self.prices.remove(existing)
                else:
                    return

                break

        # If no duplicates are found, we can safely add the price
        self.prices.add(new)

    class Meta:
        indexes = ((('hotel', 'area', 'country', 'departure_date', 'departure_airport', 'crawler', 'guests', 'vendor',
                     'duration_days', 'hotel_rating'), True),)
