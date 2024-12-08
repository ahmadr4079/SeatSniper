from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class BaseApiView(APIView, JWTAuthentication):
    def __init__(self):
        super().__init__()
