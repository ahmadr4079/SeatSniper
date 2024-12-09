from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import pagination, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from seas.app.helpers.exceptions.rest_exceptions.match.match_rest_exceptions import MatchRestNotFound
from seas.app.logics.match.match_logic import MatchLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.serializers.match.match_serializer import MatchSeatsResponseSerializer
from seas.app.vos.common_vo import CommonVo


class MatchSeatsController(BaseApiView, pagination.LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()
        self.match_logic = MatchLogic()

    @extend_schema(
        responses={200: MatchSeatsResponseSerializer, 404: OpenApiTypes.OBJECT},
        examples=[MatchRestNotFound().openapi_example],
    )
    def get(self, request: Request, *args, **kwargs):
        match_id = kwargs.get(CommonVo.match_id)
        match = self.match_logic.get_match_by_id(match_id=match_id)
        seats = self.match_logic.get_match_seats(match=match)
        response_serializer = MatchSeatsResponseSerializer({CommonVo.seats: seats})
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
