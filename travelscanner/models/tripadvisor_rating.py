from peewee import IntegerField, CharField, FloatField, CompositeKey

from travelscanner.models.meta import MetaModel


class TripAdvisorRating(MetaModel):
    country = IntegerField()
    area = CharField()
    hotel_name = CharField()
    rating = FloatField()
    review_count = IntegerField()

    class Meta:
        primary_key = CompositeKey('country', 'area', 'hotel_name')