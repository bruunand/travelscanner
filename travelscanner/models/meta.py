from datetime import datetime

from peewee import DateTimeField, Model

from travelscanner.data.database import Database


class MetaModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(MetaModel, self).save(*args, **kwargs)

    class Meta:
        database = Database.get_driver()
