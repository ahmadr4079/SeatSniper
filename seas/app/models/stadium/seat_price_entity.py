from django.db import models

from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.match.match_entity import MatchEntity
from seas.app.models.stadium.seat_entity import SeatEntity
from seas.app.models.stadium.stadium_entity import StadiumEntity


class SeatPriceEntity(EditableEntity, DeletableEntity):
    stadium = models.ForeignKey(StadiumEntity, on_delete=models.DO_NOTHING)
    match = models.ForeignKey(MatchEntity, on_delete=models.DO_NOTHING)
    seat = models.ForeignKey(SeatEntity, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()

    class Meta:
        db_table = 'seas_seat_price'
        app_label = 'app'
