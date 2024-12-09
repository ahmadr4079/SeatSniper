from django.db.models import QuerySet

from seas.app.enums.financial.invoice_item_enums import InvoiceItemStatusType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, CustomerMatchSeatEntity, DepositEntity, InvoiceEntity
from seas.app.models.financial.invoice_item_entity import InvoiceItemEntity


class InvoiceItemRepository(metaclass=Singleton):
    entity_class = InvoiceItemEntity

    def create(
        self,
        status: InvoiceItemStatusType,
        customer: CustomerEntity,
        customer_match_seat: CustomerMatchSeatEntity,
        invoice: InvoiceEntity,
    ) -> InvoiceItemEntity:
        return self.entity_class.objects.create(
            status=status, customer=customer, customer_match_seat=customer_match_seat, invoice=invoice
        )

    def update_status_by_deposit(self, deposit: DepositEntity, status: InvoiceItemStatusType):
        self.entity_class.objects.filter(invoice__deposit=deposit).update(status=status)

    def get_invoice_items_by_deposit(self, deposit: DepositEntity) -> QuerySet[InvoiceItemEntity]:
        return self.entity_class.objects.filter(invoice__deposit=deposit)
