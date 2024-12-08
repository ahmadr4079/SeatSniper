from django.db import models

from seas.app.models.base_entity import DeletableEntity, EditableEntity


class StadiumEntity(EditableEntity, DeletableEntity):
    name = models.CharField(max_length=80, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    capacity = models.IntegerField()

    class Meta:
        db_table = 'seas_stadium'
        app_label = 'app'
