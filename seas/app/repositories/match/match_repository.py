from django.db.models import QuerySet

from seas.app.enums.match.match_enums import MatchStateType
from seas.app.helpers.singleton import Singleton
from seas.app.models import MatchEntity


class MatchRepository(metaclass=Singleton):
    entity_class = MatchEntity

    def get_matches(self) -> QuerySet[MatchEntity]:
        return self.entity_class.objects.all()
