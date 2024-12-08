from django.db import models

from seas.app.enums.match.match_enums import MatchStateType
from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.stadium.stadium_entity import StadiumEntity


class MatchEntity(EditableEntity, DeletableEntity):
    stadium = models.ForeignKey(StadiumEntity, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=80)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    start_selling_time = models.DateTimeField(db_index=True)
    end_selling_time = models.DateTimeField(db_index=True)
    state = models.CharField(max_length=9, choices=MatchStateType.choices, db_index=True)

    class Meta:
        db_table = 'seas_match'
        app_label = 'app'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_state_valid", check=models.Q(state__in=MatchStateType.values)
            )
        ]
