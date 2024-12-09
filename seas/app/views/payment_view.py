from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from rest_framework import serializers

from seas.app.enums.financial.deposit_enums import DepositStatusType
from seas.app.logics.financial.deposit_logic import DepositLogic
from seas.app.vos.common_vo import CommonVo


class PaymentSerializer(serializers.Serializer):
    is_success = serializers.BooleanField()
    payment_code = serializers.IntegerField(min_value=0)


class PaymentView(View):

    def __init__(self):
        super().__init__()
        self.deposit_logic = DepositLogic()

    def get(self, request, *args, **kwargs):
        request_serializer = PaymentSerializer(data=request.GET)
        if request_serializer.is_valid(raise_exception=True):
            data = request_serializer.validated_data
            is_success = data.get(CommonVo.is_success)
            payment_code = data.get(CommonVo.payment_code)
            deposit = self.deposit_logic.get_deposit_by_payment_code(
                payment_code=str(payment_code), status=DepositStatusType.IN_PROGRESS
            )
            if deposit is None:
                return HttpResponseForbidden()
            self.deposit_logic.deposit_inquiry(deposit=deposit, is_success=is_success)
            return HttpResponse("process done")
