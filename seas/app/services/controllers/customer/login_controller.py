from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from seas.app.logics.customer.otp_logic import OtpLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.serializers.customer.login_serializer import LoginRequestSerializer, LoginResponseSerializer
from seas.app.vos.common_vo import CommonVo


class LoginController(BaseApiView):

    def __init__(self):
        super().__init__()
        self.otp_logic = OtpLogic()

    @extend_schema(
        request=LoginRequestSerializer,
        responses={200: LoginResponseSerializer, 400: OpenApiTypes.OBJECT},
    )
    def post(self, request: Request):
        request_serializer = LoginRequestSerializer(data=request.data)
        if request_serializer.is_valid(raise_exception=True):
            phone_number = request_serializer.validated_data.get(CommonVo.phone_number)
            response = self.otp_logic.set_otp(phone_number=phone_number)
            response_serializer = LoginResponseSerializer(response)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
