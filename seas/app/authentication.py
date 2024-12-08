from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from seas.app.logics.customer.security_logic import SecurityLogic
from seas.app.models import CustomerEntity
from seas.app.vos.common_vo import CommonVo


class OpenApAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "seas.app.authentication.Authentication"
    name = "OpenApAuthenticationScheme"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Value should be formatted: `Bearer <key>`",
        }


class Authentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = CustomerEntity
        self.security_logic = SecurityLogic()

    def get_validated_token(self, raw_token) -> AccessToken:
        try:
            return super().get_validated_token(raw_token=raw_token)
        except TokenError as e:
            raise AuthenticationFailed
        except InvalidToken as e:
            raise AuthenticationFailed

    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        try:
            user = self.user_model.objects.get(**{'id': user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')
        return user

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        request.jti = validated_token.get(CommonVo.jti)
        if CommonVo.user_id in validated_token:
            customer = self.get_user(validated_token)
            jti_is_revoked = self.security_logic.is_customer_jti_revoked(token=validated_token, customer=customer)
            if jti_is_revoked:
                raise AuthenticationFailed
            return self.get_user(validated_token), validated_token
        return None
