from functools import wraps

from seas.app.helpers.exceptions.repository_exceptions.match.match_repository_exception import MatchRepositoryNotFound
from seas.app.helpers.exceptions.rest_exceptions.match.match_rest_exceptions import MatchRestNotFound


def match_logic_error_handling(function):
    @wraps(function)
    def check_exceptions(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except MatchRepositoryNotFound:
            raise MatchRestNotFound

    return check_exceptions
