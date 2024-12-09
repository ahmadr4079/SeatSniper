from typing import List

from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.helpers.error_handling.match.customer_match_seat_logic_error_handling import (
    customer_match_seat_logic_error_handling,
)
from seas.app.helpers.exceptions.logic_exceptions.match.customer_match_seat_logic_exceptions import SeatNotAvailable
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, MatchEntity
from seas.app.models.match.customer_match_seat_entity import CustomerMatchSeatEntity
from seas.app.repositories.match.customer_match_seat_repository import CustomerMatchSeatRepository


class CustomerMatchSeatLogic(metaclass=Singleton):

    def __init__(self):
        self.customer_match_seat_repository = CustomerMatchSeatRepository()

    def create(
        self, customer: CustomerEntity, seat_id: str, match: MatchEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        return self.customer_match_seat_repository.create(customer=customer, seat_id=seat_id, match=match, state=state)

    @customer_match_seat_logic_error_handling
    def reservation_by_seat_ids(self, customer: CustomerEntity, seat_ids: List[str], match: MatchEntity):
        if self.customer_match_seat_repository.check_exists_by_ids_and_states(
            seat_ids=seat_ids,
            states=[CustomerMatchSeatStateType.SOLD.value, CustomerMatchSeatStateType.RESERVED.value],
            match=match,
        ):
            raise SeatNotAvailable
        for seat_id in seat_ids:
            self.create(customer=customer, seat_id=seat_id, match=match, state=CustomerMatchSeatStateType.RESERVED)
