from peewee import IntegerField, CharField, FloatField

from travelscanner.models.meta import MetaModel


class TripAdvisorRating(MetaModel):
    country = IntegerField()
    area = CharField()
    hotel_name = CharField()
    rating = FloatField()