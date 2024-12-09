from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import pagination, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from seas.app.helpers.utils import Utils
from seas.app.logics.match.match_logic import MatchLogic
from seas.app.services.controllers.base_api_view import BaseApiView
from seas.app.services.filters.match.matches_filter import MatchFilter
from seas.app.services.serializers.match.match_serializer import MatchResponseSerializer


class MatchesController(BaseApiView, pagination.LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()
        self.match_logic = MatchLogic()

    @extend_schema(
        responses={200: MatchResponseSerializer},
        parameters=Utils.get_openapi_parameters_by_filter(query_filter=MatchFilter)
        + [
            OpenApiParameter(name="limit", type=OpenApiTypes.INT64),
            OpenApiParameter(name="offset", type=OpenApiTypes.INT64),
        ],
        summary="get matches with filter in state",
    )
    def get(self, request: Request, *args, **kwargs):
        matches = self.match_logic.get_matches()
        matches_filter = MatchFilter(data=request.query_params, queryset=matches)
        paginate_query_set = self.paginate_queryset(queryset=matches_filter.qs, request=request)
        response = self.get_paginated_response(data=paginate_query_set)
        response_serializer = MatchResponseSerializer(response.data)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
