from django.db import models

from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.stadium.stadium_entity import StadiumEntity


class SeatEntity(EditableEntity, DeletableEntity):
    stadium = models.ForeignKey(StadiumEntity, on_delete=models.DO_NOTHING)
    col = models.IntegerField()
    row = models.IntegerField()
    section = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField()

    class Meta:
        db_table = 'seas_seat'
        app_label = 'app'
