from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from seas.app.logics.customer.customer_logic import CustomerLogic
from seas.app.logics.customer.otp_logic import OtpLogic
from seas.app.logics.customer.security_logic import SecurityLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.serializers.customer.otp_serializer import OtpRequestSerializer, OtpResponseSerializer
from seas.app.vos.common_vo import CommonVo


class OtpController(BaseApiView):
    def __init__(self):
        super().__init__()
        self.otp_logic = OtpLogic()
        self.customer_logic = CustomerLogic()
        self.security_logic = SecurityLogic()

    @extend_schema(
        request=OtpRequestSerializer,
        responses={400: OpenApiTypes.OBJECT, 200: OtpResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        request_serializer = OtpRequestSerializer(data=request.data)
        if request_serializer.is_valid(raise_exception=True):
            data = request_serializer.validated_data
            nounce_code = data.get(CommonVo.nounce_code)
            otp_code = data.get(CommonVo.otp_code)
            phone_number = data.get(CommonVo.phone_number)
            self.otp_logic.check_otp(phone_number=phone_number, nounce_code=nounce_code, otp_code=otp_code)
            customer = self.customer_logic.get_or_create_customer_by_phone_number(phone_number=phone_number)
            token = self.security_logic.get_refresh_and_access_token(customer=customer)
            response_serializer = OtpResponseSerializer(token)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
