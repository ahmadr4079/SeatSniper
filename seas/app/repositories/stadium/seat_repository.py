from django.db.models import OuterRef, QuerySet, Subquery, Value
from django.db.models.functions import Coalesce

from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerMatchSeatEntity, MatchEntity, SeatEntity, SeatPriceEntity


class SeatRepository(metaclass=Singleton):
    entity_class = SeatEntity

    def get_match_stadium_seats(self, match: MatchEntity) -> QuerySet[SeatEntity]:
        return self.entity_class.objects.filter(stadium=match.stadium).annotate(
            price=Subquery(
                SeatPriceEntity.objects.filter(stadium_id=OuterRef("stadium_id"), match_id=match.id)
                .order_by("-creation_time")
                .values("amount")[:1]
            ),
            state=(
                Coalesce(
                    Subquery(
                        CustomerMatchSeatEntity.objects.filter(seat_id=OuterRef("id"), match_id=match.id)
                        .order_by("-creation_time")
                        .values("state")[:1]
                    ),
                    Value(CustomerMatchSeatStateType.AVAILABLE),
                )
            ),
        )
