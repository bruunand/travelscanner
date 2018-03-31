from logging import getLogger
from peewee import CharField, IntegerField, FloatField, PrimaryKeyField, BooleanField, DateField

import travelscanner.data
from travelscanner.models.meta import MetaModel
from travelscanner.options.travel_options import Countries


class Travel(MetaModel):
    id = PrimaryKeyField()
    crawler = IntegerField()
    vendor = IntegerField()
    hotel = CharField()
    country = IntegerField()
    area = CharField()
    hotel_stars = IntegerField()
    duration_days = IntegerField()
    departure_date = DateField()
    departure_airport = IntegerField()
    guests = IntegerField(default=2)
    has_pool = BooleanField()
    has_childpool = BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prices = set()

    def __hash__(self):
        return hash((self.hotel, self.area, self.country, self.departure_date, self.departure_airport,
                     self.crawler, self.guests, self.duration_days, self.hotel_stars, self.vendor))

    '''Returns the amount of newly inserted travels.'''

    def upsert(self):
        # Skip entries which have no country specified
        if self.country == Countries.UNKNOWN:
            return 0

        existing = Travel.select().where(Travel.departure_airport == self.departure_airport,
                                         Travel.guests == self.guests, Travel.crawler == self.crawler,
                                         Travel.departure_date == self.departure_date, Travel.country == self.country,
                                         Travel.hotel_stars == self.hotel_stars, Travel.hotel == self.hotel,
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
            if existing.meal == new.meal and existing.all_inclusive == new.all_inclusive and existing.room == new.room:
                if new.price < existing.price:
                    self.prices.remove(existing)
                else:
                    return

                break

        # If no duplicates are found, we can safely add the price
        self.prices.add(new)

    class Meta:
        indexes = ((('hotel', 'area', 'country', 'departure_date', 'departure_airport', 'crawler', 'guests', 'vendor',
                     'duration_days', 'hotel_stars'), True),)
