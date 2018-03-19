from peewee import CharField, IntegerField, FloatField, PrimaryKeyField, TextField

from travelscanner.data.database import DateField
from travelscanner.models.meta import CrawledModel


class Travel(CrawledModel):
    id = PrimaryKeyField()
    crawler = IntegerField()
    vendor = CharField()
    hotel_name = CharField()
    country = IntegerField()
    area = CharField()
    hotel_stars = IntegerField()
    duration_days = IntegerField()
    departure_date = DateField()
    departure_airport = IntegerField(null=True)
    tripadvisor_rating = FloatField(null=True, default=None)
    guests = IntegerField(default=2)

    # Non-fields, used when saving
    prices = []

    def __hash__(self):
        return hash(
            (self.hotel_name, self.area, self.country, self.departure_date, self.departure_airport, self.crawler,
             self.guests, self.duration_days, self.hotel_stars, self.vendor))

    def save_or_update(self):
        existing = Travel.select().where(
            Travel.departure_airport == self.departure_airport, Travel.guests == self.guests,
            Travel.departure_date == self.departure_date, Travel.country == self.country,
            Travel.hotel_name == self.hotel_name, Travel.crawler == self.crawler,
            Travel.duration_days == self.duration_days).first()

        if existing is None:
            self.save()
        else:
            existing.prices = self.prices
            existing.save()

    def save(self, force_insert=False, only=None):
        super().save(force_insert, only)

        for price in self.prices:
            price.travel = self
            price.save_or_update()