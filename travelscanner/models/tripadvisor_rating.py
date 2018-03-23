from peewee import IntegerField, CharField, FloatField, CompositeKey

from travelscanner.models.meta import MetaModel


class TripAdvisorRating(MetaModel):
    country = IntegerField()
    area = CharField()
    hotel = CharField()
    rating = FloatField()
    review_count = IntegerField()

    def __hash__(self):
        return hash((self.country, self.area, self.hotel))

    class Meta:
        primary_key = CompositeKey('country', 'area', 'hotel')