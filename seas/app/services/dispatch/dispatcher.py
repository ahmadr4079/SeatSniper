from django.urls import path

from seas.app.services.controllers.customer.login_controller import LoginController
from seas.app.services.controllers.customer.otp_controller import OtpController
from seas.app.services.controllers.match.matches_controller import MatchesController

urlpatterns = [
    path('login/', LoginController.as_view(), name="login_controller"),
    path("otp/", OtpController.as_view(), name="otp_controller"),
    path("matches/", MatchesController.as_view(), name="matches_controller"),
]
