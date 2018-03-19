from peewee import *

from travelscanner.models.meta import CrawledModel
from travelscanner.models.travel import Travel


class Price(CrawledModel):
    id = PrimaryKeyField()
    price = FloatField()
    meal = IntegerField()
    all_inclusive = BooleanField(default=False)
    travel = ForeignKeyField(Travel)
    room = IntegerField()

    def __hash__(self):
        return hash((self.price, self.meal, self.all_inclusive))

    def save_or_update(self):
        existing = Price.select().where(Price.travel == self.travel, Price.all_inclusive == self.all_inclusive,
                                        Price.meal == self.meal, self.price == self.price).first()

        if existing is None:
            self.save()
        else:
            existing.save()
