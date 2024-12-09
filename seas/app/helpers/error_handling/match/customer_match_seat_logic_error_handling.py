from functools import wraps

from seas.app.helpers.exceptions.logic_exceptions.match.customer_match_seat_logic_exceptions import SeatNotAvailable
from seas.app.helpers.exceptions.rest_exceptions.match.match_rest_exceptions import MatchSeatNotAvailableRestBadRequest


def customer_match_seat_logic_error_handling(function):
    @wraps(function)
    def check_exceptions(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except SeatNotAvailable:
            raise MatchSeatNotAvailableRestBadRequest

    return check_exceptions
