from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from seas.app.helpers.common_response import CommonResponse
from seas.app.helpers.exceptions.rest_exceptions.match.match_rest_exceptions import (
    MatchRestNotFound,
    MatchSeatNotAvailableRestBadRequest,
)
from seas.app.logics.match.customer_match_seat_logic import CustomerMatchSeatLogic
from seas.app.logics.match.match_logic import MatchLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.serializers.match.match_serializer import (
    MatchSeatsReservationRequestSerializer,
    MatchSeatsResponseSerializer,
)
from seas.app.vos.common_vo import CommonVo


class MatchSeatsReservationController(BaseApiView, pagination.LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()
        self.match_logic = MatchLogic()
        self.customer_match_seat_logic = CustomerMatchSeatLogic()

    @extend_schema(
        request=MatchSeatsReservationRequestSerializer,
        responses={200: MatchSeatsResponseSerializer, 404: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
        examples=[
            MatchRestNotFound().openapi_example,
            MatchSeatNotAvailableRestBadRequest().openapi_example,
            OpenApiExample(
                "MatchSeatsReservationResponse",
                value={"code": 200, "message": "reservation successfully"},
                response_only=True,
                status_codes=["200"],
            ),
        ],
        summary="reserve seat (start of deposit process)",
    )
    def post(self, request: Request, *args, **kwargs):
        request_serializer = MatchSeatsReservationRequestSerializer(data=request.data)
        if request_serializer.is_valid(raise_exception=True):
            match_id = kwargs.get(CommonVo.match_id)
            match = self.match_logic.get_match_by_id(match_id=match_id)
            seat_ids = request_serializer.validated_data.get(CommonVo.seat_ids)
            self.customer_match_seat_logic.reservation_by_seat_ids(
                customer=request.user, seat_ids=seat_ids, match=match
            )
            return CommonResponse(message="reservation successfully")
