from peewee import *

from travelscanner.data.database import Database
from travelscanner.models.meta import MetaModel
from travelscanner.models.travel import Travel


class Price(MetaModel):
    id = PrimaryKeyField()
    price = FloatField()
    meal = IntegerField()
    all_inclusive = BooleanField(default=False)
    travel = ForeignKeyField(Travel)
    room = IntegerField()

    def __hash__(self):
        return hash((self.price, self.meal, self.all_inclusive, self.travel, self.travel))

    def upsert(self):
        existing = Database.retrieve_from_cache(self)

        if existing is None:
            self.save()
        else:
            existing.save()
