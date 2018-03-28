from peewee import *

from travelscanner.data.database import Database
from travelscanner.models.meta import MetaModel
from travelscanner.models.travel import Travel


class Price(MetaModel):
    id = PrimaryKeyField()
    price = FloatField()
    predicted_price = FloatField(null=True)
    meal = IntegerField()
    all_inclusive = BooleanField(default=False)
    travel = ForeignKeyField(Travel)
    room = IntegerField()

    def __hash__(self):
        return hash((self.price, self.meal, self.all_inclusive, self.travel, self.room))

    def upsert(self):
        existing = Price.select().where(Price.price == self.price, Price.meal == self.meal,
                                        Price.all_inclusive == self.all_inclusive, Price.travel == self.travel,
                                        Price.room == self.room).first()

        if existing is None:
            self.save()
        else:
            existing.save()

    class Meta:
        indexes = ((('price', 'meal', 'room', 'travel', 'all_inclusive'), True),)
