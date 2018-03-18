from peewee import CharField, IntegerField, FloatField, PrimaryKeyField

from travelscanner.data.database import DateField
from travelscanner.models.metamodel import MetaModel


class Travel(MetaModel):
    id = PrimaryKeyField()
    crawler = IntegerField()
    vendor = CharField()
    hotel_name = CharField()
    country = CharField()  # Should probably be an enum for consistency
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
        return hash((self.hotel_name, self.country, self.departure_date, self.departure_airport, self.crawler))

    def save_or_update(self):
        existing = Travel.select().where(Travel.departure_airport == self.departure_airport,
                                         Travel.departure_date == self.departure_date, Travel.country == self.country,
                                         Travel.hotel_name == self.hotel_name, Travel.crawler == self.crawler).first()

        if existing is None:
            self.save()
        else:
            existing.prices = self.prices
            existing.save()

    def save(self, force_insert=False, only=None):
        super().save(force_insert, only)

        for price in self.prices:
            price.travel = self.id
            price.save_or_update()
