from seas.app.dtos.financial.deposit_dto import ShaparakRedirectDto
from seas.app.helpers.singleton import Singleton
from seas.app.models import DepositEntity


class PaymentAdapter(metaclass=Singleton):

    def deposit(self, deposit: DepositEntity) -> ShaparakRedirectDto:
        return ShaparakRedirectDto(
            redirect_url=f"http://localhost:8000/payment/?is_success=True&payment_code={deposit.payment_code}"
        )
