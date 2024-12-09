from django.core.validators import MinValueValidator
from django.db import models

from seas.app.enums.financial.deposit_enums import DepositStatusType
from seas.app.models import CustomerEntity
from seas.app.models.base_entity import DeletableEntity, EditableEntity


class DepositEntity(EditableEntity, DeletableEntity):
    amount = models.BigIntegerField(validators=[MinValueValidator(0)])
    payment_code = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    status = models.CharField(max_length=11, choices=DepositStatusType.choices, db_index=True)
    customer = models.ForeignKey(CustomerEntity, on_delete=models.DO_NOTHING)
    tracking_code = models.CharField(max_length=15, db_index=True)

    class Meta:
        db_table = 'seas_deposit'
        app_label = 'app'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=DepositStatusType.values),
            ),
        ]
