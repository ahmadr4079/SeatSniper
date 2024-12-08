import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class OtpRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    nounce_code = serializers.CharField(max_length=32)
    otp_code = serializers.IntegerField(min_value=0, max_value=99999)

    def validate_phone_number(self, phone_number: str):
        if not re.search("^(9\d{9})$", phone_number):
            raise ValidationError("phone number not valid")
        return phone_number


class OtpResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField(allow_null=True)
    expires_in = serializers.FloatField()
