from django.db import models

from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.customer.customer_entity import CustomerEntity
from seas.app.models.match.match_entity import MatchEntity
from seas.app.models.stadium.seat_entity import SeatEntity


class CustomerMatchSeatEntity(EditableEntity, DeletableEntity):
    match = models.ForeignKey(MatchEntity, on_delete=models.DO_NOTHING)
    seat = models.ForeignKey(SeatEntity, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(CustomerEntity, on_delete=models.DO_NOTHING)
    state = models.CharField(
        max_length=8,
        choices=CustomerMatchSeatStateType.choices,
        db_index=True,
        default=CustomerMatchSeatStateType.RESERVED,
    )

    class Meta:
        db_table = 'seas_customer_match_seat'
        app_label = 'app'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_state_valid", check=models.Q(state__in=CustomerMatchSeatStateType.values)
            )
        ]
