import django_filters

from seas.app.models import MatchEntity


class MatchFilter(django_filters.FilterSet):
    class Meta:
        model = MatchEntity
        fields = ["state"]
