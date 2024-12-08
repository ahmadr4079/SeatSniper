from django.db import models
from django.utils import timezone

from seas.app.enums.customer.session_enums import SessionTokenType
from seas.app.models import CustomerEntity
from seas.app.models.base_entity import EditableEntity


class SessionEntity(EditableEntity):
    jti = models.CharField(max_length=120, db_index=True)
    customer = models.ForeignKey(CustomerEntity, on_delete=models.DO_NOTHING, related_name="jwt_tokens")
    expires_datetime = models.DateTimeField(default=timezone.now, db_index=True)
    is_revoked = models.BooleanField(db_index=True)
    type = models.CharField(max_length=7, choices=SessionTokenType.choices, null=True, blank=True, db_index=True)

    class Meta:
        db_table = "seas_session"
        app_label = "app"
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid", check=models.Q(type__in=SessionTokenType.values)
            )
        ]
