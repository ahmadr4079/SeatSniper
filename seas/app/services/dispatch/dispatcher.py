from django.urls import path

from seas.app.services.controllers.customer.login_controller import LoginController
from seas.app.services.controllers.customer.otp_controller import OtpController
from seas.app.services.controllers.financial.deposit_controller import DepositController
from seas.app.services.controllers.match.match_seats_controller import MatchSeatsController
from seas.app.services.controllers.match.match_seats_reservation_controller import MatchSeatsReservationController
from seas.app.services.controllers.match.matches_controller import MatchesController

urlpatterns = [
    path('login/', LoginController.as_view(), name="login_controller"),
    path("otp/", OtpController.as_view(), name="otp_controller"),
    path("matches/", MatchesController.as_view(), name="matches_controller"),
    path("matches/<uuid:match_id>/seats/", MatchSeatsController.as_view(), name="match_seats_controller"),
    path(
        "matches/<uuid:match_id>/seats/reservation/",
        MatchSeatsReservationController.as_view(),
        name="match_seats_reservation_controller",
    ),
    path("deposit/", DepositController.as_view(), name="deposit_controller"),
]
