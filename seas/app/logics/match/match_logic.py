from django.db.models import QuerySet

from seas.app.helpers.singleton import Singleton
from seas.app.models import MatchEntity
from seas.app.repositories.match.match_repository import MatchRepository


class MatchLogic(metaclass=Singleton):

    def __init__(self):
        self.match_repository = MatchRepository()

    def get_matches(self) -> QuerySet[MatchEntity]:
        return self.match_repository.get_matches()
