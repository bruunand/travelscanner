from peewee import *

from travelscanner.models.metamodel import MetaModel
from travelscanner.models.travel import Travel


class Price(MetaModel):
    id = PrimaryKeyField()
    price = FloatField()
    meal = CharField()
    all_inclusive = BooleanField(default=False)
    travel = ForeignKeyField(Travel)

    def save_or_update(self):
        existing = Price.select().where(Price.travel == self.travel, Price.all_inclusive == self.all_inclusive,
                                        Price.meal == self.meal, self.price == self.price).first()

        if existing is None:
            self.save()
        else:
            existing.save()
