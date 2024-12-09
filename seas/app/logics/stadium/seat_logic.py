from typing import List

from django.db.models import QuerySet

from seas.app.helpers.singleton import Singleton
from seas.app.models import MatchEntity, SeatEntity
from seas.app.repositories.stadium.seat_repository import SeatRepository


class SeatLogic(metaclass=Singleton):

    def __init__(self):
        self.seat_repository = SeatRepository()

    def get_match_stadium_seats(self, match: MatchEntity) -> QuerySet[SeatEntity]:
        return self.seat_repository.get_match_stadium_seats(match=match)

    def get_sum_price(self, seat_ids: List[str], match: MatchEntity) -> int:
        return self.seat_repository.get_sum_price(seat_ids=seat_ids, match=match)
