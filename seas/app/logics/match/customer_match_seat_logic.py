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

    @customer_match_seat_logic_error_handling
    def check_exists_customer_by_ids_and_state(
        self, seat_ids: List[str], states: List[str], match: MatchEntity, customer: CustomerEntity
    ) -> bool:
        if not self.customer_match_seat_repository.check_exists_customer_by_ids_and_state(
            seat_ids=seat_ids, states=states, match=match, customer=customer
        ):
            raise SeatNotAvailable

    def get_by_seat_id(
        self, customer: CustomerEntity, seat_id: str, match: MatchEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        return self.customer_match_seat_repository.get_by_seat_id(
            seat_id=seat_id, customer=customer, match=match, state=state
        )

    def update_state(
        self, customer_match_seat: CustomerMatchSeatEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        return self.customer_match_seat_repository.update_state(customer_match_seat=customer_match_seat, state=state)
