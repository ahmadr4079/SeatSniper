import datetime
from typing import List

from django.utils.crypto import get_random_string
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class Utils:

    @staticmethod
    def convert_filed_class_name_to_openapi_type(class_name: str) -> OpenApiTypes:
        types = {
            "CharField": OpenApiTypes.STR,
            "DateTimeField": OpenApiTypes.DATETIME,
            "NullBooleanField": OpenApiTypes.BOOL,
        }
        return types.get(class_name, OpenApiTypes.STR)

    @staticmethod
    def get_openapi_parameters_by_filter(query_filter) -> List[OpenApiParameter]:
        parameters = []
        for field_name, field in query_filter.base_filters.items():
            if field.extra and "choices" in field.extra:
                enum = [c[0] for c in field.extra.get("choices")]
            else:
                enum = None
            parameters.append(
                OpenApiParameter(
                    name=field_name,
                    required=field.extra.get("required", True),
                    enum=enum,
                    type=Utils.convert_filed_class_name_to_openapi_type(class_name=field.field.__class__.__name__),
                )
            )
        return parameters

    @staticmethod
    def generate_tracking_code() -> str:
        now_time_stamp = str(int(datetime.datetime.timestamp(datetime.datetime.now())))
        return now_time_stamp + get_random_string(2, allowed_chars="0123456789")

    @staticmethod
    def generate_payment_code() -> str:
        now_time_stamp = str(int(datetime.datetime.timestamp(datetime.datetime.now())))
        return now_time_stamp + get_random_string(5, allowed_chars="0123456789")
