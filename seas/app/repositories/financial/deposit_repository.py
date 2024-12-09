from typing import Optional

from seas.app.enums.financial.deposit_enums import DepositStatusType
from seas.app.helpers.singleton import Singleton
from seas.app.helpers.utils import Utils
from seas.app.models import CustomerEntity
from seas.app.models.financial.deposit_entity import DepositEntity


class DepositRepository(metaclass=Singleton):
    entity_class = DepositEntity

    def create(self, amount: int, status: DepositStatusType, customer: CustomerEntity) -> DepositEntity:
        return self.entity_class.objects.create(
            amount=amount, status=status, customer=customer, tracking_code=Utils.generate_tracking_code()
        )

    def update_payment_code(self, deposit: DepositEntity, payment_code: str) -> DepositEntity:
        deposit.payment_code = payment_code
        deposit.save()
        return deposit

    def get_deposit_by_payment_code(self, payment_code: str, status: DepositStatusType) -> Optional[DepositEntity]:
        return self.entity_class.objects.filter(payment_code=payment_code, status=status).first()

    def update_status(self, deposit: DepositEntity, status: DepositStatusType) -> DepositEntity:
        deposit.status = status
        deposit.save()
        return deposit
