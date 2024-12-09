from django.db import models

from seas.app.enums.financial.invoice_item_enums import InvoiceItemStatusType
from seas.app.models import CustomerEntity, InvoiceEntity
from seas.app.models.base_entity import DeletableEntity, EditableEntity
from seas.app.models.match.customer_match_seat_entity import CustomerMatchSeatEntity


class InvoiceItemEntity(EditableEntity, DeletableEntity):
    status = models.CharField(max_length=7, choices=InvoiceItemStatusType.choices, db_index=True)
    customer = models.ForeignKey(CustomerEntity, on_delete=models.DO_NOTHING)
    invoice = models.ForeignKey(InvoiceEntity, on_delete=models.DO_NOTHING)
    customer_match_seat = models.ForeignKey(CustomerMatchSeatEntity, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'seas_invoice_item'
        app_label = 'app'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=InvoiceItemStatusType.values),
            ),
        ]
