from rest_framework import serializers


class DepositRequestSerializer(serializers.Serializer):
    seat_ids = serializers.ListSerializer(child=serializers.UUIDField())
    match_id = serializers.UUIDField()


class DepositResponseSerializer(serializers.Serializer):
    redirect_url = serializers.CharField()
