from typing import Mapping


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
