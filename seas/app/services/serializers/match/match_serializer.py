from rest_framework import serializers

from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.models import MatchEntity, SeatEntity


class MatchSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchEntity
        exclude = ["creation_time", "last_update_time", "is_deleted"]


class MatchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = MatchSerializerSerializer(many=True)


class MatchSeatStadiumSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(allow_null=True)
    state = serializers.ChoiceField(choices=CustomerMatchSeatStateType.choices)

    class Meta:
        model = SeatEntity
        exclude = ["creation_time", "last_update_time", "is_deleted"]


class MatchSeatsResponseSerializer(serializers.Serializer):
    seats = MatchSeatStadiumSerializer(many=True)


class MatchSeatsReservationRequestSerializer(serializers.Serializer):
    seat_ids = serializers.ListSerializer(child=serializers.UUIDField())
