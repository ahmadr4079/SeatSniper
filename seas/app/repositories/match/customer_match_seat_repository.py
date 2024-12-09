from typing import List

from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, MatchEntity
from seas.app.models.match.customer_match_seat_entity import CustomerMatchSeatEntity


class CustomerMatchSeatRepository(metaclass=Singleton):
    entity_class = CustomerMatchSeatEntity

    def create(
        self, customer: CustomerEntity, seat_id: str, match: MatchEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        return self.entity_class.objects.create(customer=customer, seat_id=seat_id, match=match, state=state)

    def check_exists_by_ids_and_states(self, seat_ids: List[str], states: List[str], match: MatchEntity) -> bool:
        return self.entity_class.objects.filter(seat_id__in=seat_ids, state__in=states, match=match).exists()

    def check_exists_customer_by_ids_and_state(
        self, seat_ids: List[str], states: List[str], match: MatchEntity, customer: CustomerEntity
    ) -> bool:
        return self.entity_class.objects.filter(
            seat_id__in=seat_ids, state__in=states, match=match, customer=customer
        ).exists()

    def get_by_seat_id(
        self, customer: CustomerEntity, seat_id: str, match: MatchEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        return self.entity_class.objects.get(seat_id=seat_id, customer=customer, match=match, state=state)

    def update_state(
        self, customer_match_seat: CustomerMatchSeatEntity, state: CustomerMatchSeatStateType
    ) -> CustomerMatchSeatEntity:
        customer_match_seat.state = state
        customer_match_seat.save()
        return customer_match_seat
