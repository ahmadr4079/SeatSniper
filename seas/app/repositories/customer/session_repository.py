from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from seas.app.enums.customer.session_enums import SessionTokenType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, SessionEntity


class SessionRepository(metaclass=Singleton):
    entity_class = SessionEntity

    def create(
        self,
        jti: str,
        customer: CustomerEntity,
        expires_datetime: datetime,
        type: SessionTokenType,
        is_revoked: bool = False,
    ) -> SessionEntity:
        return self.entity_class.objects.create(
            jti=jti, customer=customer, expires_datetime=expires_datetime, type=type, is_revoked=is_revoked
        )

    def get_session_by_jti(self, jti: str, customer: CustomerEntity):
        try:
            return self.entity_class.objects.get(jti=jti, customer=customer)
        except ObjectDoesNotExist:
            return None
