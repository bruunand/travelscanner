from peewee import CharField, IntegerField, FloatField, PrimaryKeyField, BooleanField

from travelscanner.data.database import DateField, Database
from travelscanner.models.meta import MetaModel
from travelscanner.options.travel_options import Countries


class Travel(MetaModel):
    id = PrimaryKeyField()
    crawler = IntegerField()
    vendor = IntegerField()
    hotel_name = CharField()
    country = IntegerField()
    area = CharField()
    hotel_stars = IntegerField()
    duration_days = IntegerField()
    departure_date = DateField()
    departure_airport = IntegerField(null=True)
    tripadvisor_rating = FloatField(null=True, default=None)
    guests = IntegerField(default=2)
    has_pool = BooleanField()
    has_childpool = BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prices = set()

    def __hash__(self):
        return hash((self.hotel_name, self.area, self.country, self.departure_date, self.departure_airport,
                     self.crawler, self.guests, self.duration_days, self.hotel_stars, self.vendor))

    def upsert(self):
        # Skip entries which have no country specified
        if self.country == Countries.UNKNOWN:
            return

        existing = Database.retrieve_from_cache(self)

        if existing is None:
            self.save()
        else:
            existing.prices = self.prices
            existing.save()

    def save(self, force_insert=False, only=None):
        super().save(force_insert, only)

        for price in self.prices:
            price.travel = self
            price.upsert()
