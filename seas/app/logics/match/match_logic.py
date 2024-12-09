from django.db.models import QuerySet

from seas.app.helpers.error_handling.match.match_logic_error_handling import match_logic_error_handling
from seas.app.helpers.singleton import Singleton
from seas.app.logics.stadium.seat_logic import SeatLogic
from seas.app.models import MatchEntity, SeatEntity
from seas.app.repositories.match.match_repository import MatchRepository


class MatchLogic(metaclass=Singleton):

    def __init__(self):
        self.match_repository = MatchRepository()
        self.seat_logic = SeatLogic()

    def get_matches(self) -> QuerySet[MatchEntity]:
        return self.match_repository.get_matches()

    @match_logic_error_handling
    def get_match_by_id(self, match_id: str) -> MatchEntity:
        return self.match_repository.get_match_by_id(match_id=match_id)

    def get_match_seats(self, match: MatchEntity) -> QuerySet[SeatEntity]:
        return self.seat_logic.get_match_stadium_seats(match=match)
