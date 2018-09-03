from peewee import *

from travelscanner.data.database import Database
from travelscanner.models.meta import MetaModel
from travelscanner.models.travel import Travel


class Price(MetaModel):
    id = PrimaryKeyField()
    price = FloatField()
    brochure_price = FloatField(null=True)
    predicted_price = FloatField(null=True)
    meal = IntegerField()
    travel = ForeignKeyField(Travel)
    room = CharField()
    sub_room = CharField(null=True)

    def __hash__(self):
        return hash((self.price, self.meal, self.travel, self.room, self.sub_room))

    '''Returns the amount of newly inserted prices.'''

    def upsert(self):
        existing = Price.select().where(Price.price == self.price, Price.meal == self.meal, Price.travel == self.travel,
                                        Price.room == self.room).first()

        if existing is None:
            self.save()
            return 1
        else:
            existing.save()
            return 0

    class Meta:
        indexes = ((('price', 'meal', 'room', 'travel', 'sub_room'), True),)
