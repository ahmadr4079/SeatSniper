from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from seas.app.helpers.exceptions.repository_exceptions.match.match_repository_exception import MatchRepositoryNotFound
from seas.app.helpers.singleton import Singleton
from seas.app.models import MatchEntity


class MatchRepository(metaclass=Singleton):
    entity_class = MatchEntity

    def get_matches(self) -> QuerySet[MatchEntity]:
        return self.entity_class.objects.all()

    def get_match_by_id(self, match_id: str) -> MatchEntity:
        try:
            return self.entity_class.objects.get(id=match_id)
        except ObjectDoesNotExist:
            raise MatchRepositoryNotFound
