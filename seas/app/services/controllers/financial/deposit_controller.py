from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import pagination, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from seas.app.helpers.exceptions.rest_exceptions.match.match_rest_exceptions import (
    MatchRestNotFound,
    MatchSeatNotAvailableRestBadRequest,
)
from seas.app.logics.financial.deposit_logic import DepositLogic
from seas.app.logics.match.customer_match_seat_logic import CustomerMatchSeatLogic
from seas.app.logics.match.match_logic import MatchLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.serializers.financial.deposit_serializer import (
    DepositRequestSerializer,
    DepositResponseSerializer,
)
from seas.app.vos.common_vo import CommonVo


class DepositController(BaseApiView, pagination.LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()
        self.match_logic = MatchLogic()
        self.customer_match_seat_logic = CustomerMatchSeatLogic()
        self.deposit_logic = DepositLogic()

    @extend_schema(
        request=DepositRequestSerializer,
        responses={200: DepositResponseSerializer, 404: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
        examples=[MatchRestNotFound().openapi_example, MatchSeatNotAvailableRestBadRequest().openapi_example],
    )
    def post(self, request: Request, *args, **kwargs):
        request_serializer = DepositRequestSerializer(data=request.data)
        if request_serializer.is_valid(raise_exception=True):
            seat_ids = request_serializer.validated_data.get(CommonVo.seat_ids)
            match_id = request_serializer.validated_data.get(CommonVo.match_id)
            match = self.match_logic.get_match_by_id(match_id=match_id)
            shaparak_redirect_dto = self.deposit_logic.deposit(seat_ids=seat_ids, match=match, customer=request.user)
            response_serializer = DepositResponseSerializer(shaparak_redirect_dto)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
