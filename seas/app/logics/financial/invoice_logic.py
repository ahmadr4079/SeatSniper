from seas.app.enums.financial.invoice_enums import InvoiceStatusType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity, DepositEntity, InvoiceEntity
from seas.app.repositories.financial.invoice_repository import InvoiceRepository


class InvoiceLogic(metaclass=Singleton):

    def __init__(self):
        self.invoice_repository = InvoiceRepository()

    def create(self, status: InvoiceStatusType, customer: CustomerEntity, deposit: DepositEntity) -> InvoiceEntity:
        return self.invoice_repository.create(status=status, customer=customer, deposit=deposit)

    def update_status(self, invoice: InvoiceEntity, status: InvoiceStatusType) -> InvoiceEntity:
        return self.invoice_repository.update_status(invoice=invoice, status=status)

    def update_status_by_deposit(self, deposit: DepositEntity, status: InvoiceStatusType):
        self.invoice_repository.update_status_by_deposit(deposit=deposit, status=status)
