from typing import List, Optional

from django.db import transaction

from seas.app.adapters.payment_adapter import PaymentAdapter
from seas.app.dtos.financial.deposit_dto import ShaparakRedirectDto
from seas.app.enums.financial.deposit_enums import DepositStatusType
from seas.app.enums.financial.invoice_enums import InvoiceStatusType
from seas.app.enums.financial.invoice_item_enums import InvoiceItemStatusType
from seas.app.enums.match.match_enums import CustomerMatchSeatStateType
from seas.app.helpers.singleton import Singleton
from seas.app.helpers.utils import Utils
from seas.app.logics.financial.invoice_item_logic import InvoiceItemLogic
from seas.app.logics.financial.invoice_logic import InvoiceLogic
from seas.app.logics.match.customer_match_seat_logic import CustomerMatchSeatLogic
from seas.app.logics.stadium.seat_logic import SeatLogic
from seas.app.models import CustomerEntity, DepositEntity, MatchEntity
from seas.app.repositories.financial.deposit_repository import DepositRepository
from seas.project.config import RunEnvType, seas_config


class DepositLogic(metaclass=Singleton):

    def __init__(self):
        self.deposit_repository = DepositRepository()
        self.invoice_logic = InvoiceLogic()
        self.invoice_item_logic = InvoiceItemLogic()
        self.customer_match_seat_logic = CustomerMatchSeatLogic()
        self.seat_logic = SeatLogic()
        self.payment_adapter = PaymentAdapter()

    def get_deposit_by_payment_code(self, payment_code: str, status: DepositStatusType) -> Optional[DepositEntity]:
        return self.deposit_repository.get_deposit_by_payment_code(payment_code=payment_code, status=status)

    def update_payment_code(self, deposit: DepositEntity, payment_code: str) -> DepositEntity:
        return self.deposit_repository.update_payment_code(deposit=deposit, payment_code=payment_code)

    def update_status(self, deposit: DepositEntity, status: DepositStatusType) -> DepositEntity:
        return self.deposit_repository.update_status(deposit=deposit, status=status)

    @transaction.atomic
    def deposit(self, seat_ids: List[str], match: MatchEntity, customer: CustomerEntity) -> ShaparakRedirectDto:
        self.customer_match_seat_logic.check_exists_customer_by_ids_and_state(
            seat_ids=seat_ids, match=match, customer=customer, states=[CustomerMatchSeatStateType.RESERVED]
        )
        seats_sum_price = self.seat_logic.get_sum_price(seat_ids=seat_ids, match=match)
        deposit = self.deposit_repository.create(
            customer=customer, amount=seats_sum_price, status=DepositStatusType.IN_PROGRESS
        )
        invoice = self.invoice_logic.create(status=InvoiceStatusType.PENDING, customer=customer, deposit=deposit)
        for seat_id in seat_ids:
            customer_match_seat = self.customer_match_seat_logic.get_by_seat_id(
                customer=customer, match=match, seat_id=seat_id, state=CustomerMatchSeatStateType.RESERVED
            )
            self.invoice_item_logic.create(
                status=InvoiceItemStatusType.PENDING,
                customer=customer,
                customer_match_seat=customer_match_seat,
                invoice=invoice,
            )
        if seas_config.run_env_type == RunEnvType.development:
            deposit = self.update_payment_code(deposit=deposit, payment_code=Utils.generate_payment_code())
        shaparak_redirect_dto = self.payment_adapter.deposit(deposit=deposit)
        return shaparak_redirect_dto

    def success_deposit(self, deposit: DepositEntity):
        self.update_status(deposit=deposit, status=DepositStatusType.SUCCESS)
        self.invoice_logic.update_status_by_deposit(deposit=deposit, status=InvoiceStatusType.SUCCESS)
        self.invoice_item_logic.update_status_by_deposit(deposit=deposit, status=InvoiceItemStatusType.SUCCESS)
        invoice_items = self.invoice_item_logic.get_invoice_items_by_deposit(deposit=deposit)
        for invoice_item in invoice_items:
            self.customer_match_seat_logic.update_state(
                customer_match_seat=invoice_item.customer_match_seat, state=CustomerMatchSeatStateType.SOLD
            )

    def failed_deposit(self, deposit: DepositEntity):
        self.update_status(deposit=deposit, status=DepositStatusType.FAILED)
        self.invoice_logic.update_status_by_deposit(deposit=deposit, status=InvoiceStatusType.FAILED)
        self.invoice_item_logic.update_status_by_deposit(deposit=deposit, status=InvoiceItemStatusType.FAILED)
        invoice_items = self.invoice_item_logic.get_invoice_items_by_deposit(deposit=deposit)
        for invoice_item in invoice_items:
            self.customer_match_seat_logic.update_state(
                customer_match_seat=invoice_item.customer_match_seat, state=CustomerMatchSeatStateType.CANCELED
            )

    def deposit_inquiry(self, deposit: DepositEntity, is_success: bool):
        self.success_deposit(deposit=deposit) if is_success else self.failed_deposit(deposit=deposit)
