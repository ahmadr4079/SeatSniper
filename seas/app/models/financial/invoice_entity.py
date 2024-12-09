from django.db import models

from seas.app.enums.financial.invoice_enums import InvoiceStatusType
from seas.app.models import CustomerEntity
from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.financial.deposit_entity import DepositEntity


class InvoiceEntity(EditableEntity, DeletableEntity):
    status = models.CharField(max_length=7, choices=InvoiceStatusType.choices, db_index=True)
    customer = models.ForeignKey(CustomerEntity, on_delete=models.DO_NOTHING)
    deposit = models.ForeignKey(DepositEntity, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'seas_invoice'
        app_label = 'app'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=InvoiceStatusType.values),
            ),
        ]
