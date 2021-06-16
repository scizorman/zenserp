from functools import wraps
from typing import Any, Callable, Mapping
from uuid import UUID

from requests import Response


class ZenserpException(Exception):
    """There was an ambiguous exception that occurred while requesting to Zenserp."""

    pass


class NoAPIKeyException(ZenserpException):
    """This exception occurs when your API key is not provided."""

    pass


class WrongAPIKeyException(ZenserpException):
    """This exception occurs when you API key is wrong."""

    pass


class APILimitException(ZenserpException):
    """This exception occurs when your API key has no remaining request."""

    pass


class NotFoundException(ZenserpException):
    """This exception occurs when the search results are not found."""

    pass


class InvalidRequestException(ZenserpException):
    """This exception occurs when your request is invalid."""

    def __init__(self, errors: Mapping[str, str]):
        self._errors = errors

    def __str__(self) -> str:
        error_messages = ", ".join(f"{k}: {v.replace('.', '')}" for k, v in self._errors.items())
        return f"invalid request: ({error_messages})"


def status_handler(func: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        resp = func(*args, **kwargs)
        status_code = resp.status_code
        if status_code == 200:
            pass
        elif status_code == 403:
            message = resp.json()["error"]
            if message == "No apikey provided.":
                raise NoAPIKeyException("no API key is provided")
            elif message == "Not enough requests.":
                api_key = resp.request.headers["apikey"]
                try:
                    UUID(hex=api_key)
                except ValueError:
                    raise WrongAPIKeyException("your API key is wrong")
                else:
                    raise APILimitException("no request remains")
        elif status_code == 404:
            raise NotFoundException("not found")
        elif status_code == 500:
            errors = resp.json()["errors"][0]
            raise InvalidRequestException(errors)
        else:
            resp.raise_for_status()
        return resp

    return wrapper
