import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)

    def validate_phone_number(self, phone_number: str):
        if not re.search("^(9\d{9})$", phone_number):
            raise ValidationError("phone number not valid")
        return phone_number


class LoginResponseSerializer(serializers.Serializer):
    nounce_code = serializers.CharField()
    nounce_code_expires_in = serializers.FloatField()
    otp_code_expires_in = serializers.FloatField()
