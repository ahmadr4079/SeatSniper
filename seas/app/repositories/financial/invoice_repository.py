from seas.app.enums.financial.invoice_enums import InvoiceStatusType
from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity
from seas.app.models.financial.deposit_entity import DepositEntity
from seas.app.models.financial.invoice_entity import InvoiceEntity


class InvoiceRepository(metaclass=Singleton):
    entity_class = InvoiceEntity

    def create(self, status: InvoiceStatusType, customer: CustomerEntity, deposit: DepositEntity) -> InvoiceEntity:
        return self.entity_class.objects.create(status=status, customer=customer, deposit=deposit)

    def update_status(self, invoice: InvoiceEntity, status: InvoiceStatusType) -> InvoiceEntity:
        invoice.status = status
        invoice.save()
        return invoice

    def update_status_by_deposit(self, deposit: DepositEntity, status: InvoiceStatusType):
        self.entity_class.objects.filter(deposit=deposit).update(status=status)
