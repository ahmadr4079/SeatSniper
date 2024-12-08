from typing import Union

import pytz
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from seas.app.dtos.customer.token_dto import TokenDto
from seas.app.enums.customer.session_enums import SessionTokenType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity
from seas.app.repositories.customer.session_repository import SessionRepository
from seas.app.vos.common_vo import CommonVo


class SecurityLogic(metaclass=Singleton):

    def __init__(self):
        self.session_repository = SessionRepository()

    @transaction.atomic
    def get_refresh_and_access_token(self, customer: CustomerEntity) -> TokenDto:
        refresh_token = RefreshToken.for_user(user=customer)
        access_token = refresh_token.access_token
        self.session_repository.create(
            jti=refresh_token.get(CommonVo.jti),
            customer=customer,
            type=SessionTokenType.REFRESH,
            expires_datetime=timezone.datetime.fromtimestamp(refresh_token.get(CommonVo.exp), tz=pytz.UTC),
        )
        self.session_repository.create(
            jti=access_token.get(CommonVo.jti),
            customer=customer,
            type=SessionTokenType.ACCESS,
            expires_datetime=timezone.datetime.fromtimestamp(access_token.get(CommonVo.exp), tz=pytz.UTC),
        )
        return TokenDto(
            access_token=str(access_token), refresh_token=str(refresh_token), expires_in=access_token.get(CommonVo.exp)
        )

    def is_customer_jti_revoked(self, token: Union[AccessToken, RefreshToken], customer: CustomerEntity) -> bool:
        jti = token.get(CommonVo.jti)
        session = self.session_repository.get_session_by_jti(jti=jti, customer=customer)
        if session:
            return session.is_revoked
        return False
