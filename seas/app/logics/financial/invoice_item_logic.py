from django.db.models import QuerySet

from seas.app.enums.financial.invoice_item_enums import InvoiceItemStatusType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, CustomerMatchSeatEntity, DepositEntity, InvoiceEntity, InvoiceItemEntity
from seas.app.repositories.financial.invoice_item_repository import InvoiceItemRepository


class InvoiceItemLogic(metaclass=Singleton):

    def __init__(self):
        self.invoice_item_repository = InvoiceItemRepository()

    def create(
        self,
        status: InvoiceItemStatusType,
        customer: CustomerEntity,
        customer_match_seat: CustomerMatchSeatEntity,
        invoice: InvoiceEntity,
    ) -> InvoiceItemEntity:
        return self.invoice_item_repository.create(
            status=status, customer=customer, customer_match_seat=customer_match_seat, invoice=invoice
        )

    def update_status_by_deposit(self, deposit: DepositEntity, status: InvoiceItemStatusType):
        self.invoice_item_repository.update_status_by_deposit(deposit=deposit, status=status)

    def get_invoice_items_by_deposit(self, deposit: DepositEntity) -> QuerySet[InvoiceItemEntity]:
        return self.invoice_item_repository.get_invoice_items_by_deposit(deposit=deposit)
