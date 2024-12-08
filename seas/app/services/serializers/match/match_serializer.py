from rest_framework import serializers

from seas.app.models import MatchEntity


class MatchSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchEntity
        exclude = ["creation_time", "last_update_time", "is_deleted"]


class MatchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = MatchSerializerSerializer(many=True)
