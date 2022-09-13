from typing import Mapping

from aiohttp import ClientResponse


class ZenserpException(Exception):
    """There was an ambiguous exception that occurred while requesting to Zenserp."""

    pass


class NoAPIKeyException(ZenserpException):
    """This exception occurs when your API key is not provided."""

    pass


class WrongAPIKeyException(ZenserpException):
    """This exception occurs when your API key is wrong."""

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


async def handle_status(response: ClientResponse) -> None:
    status = response.status
    if status == 200:
        return
    elif status == 403:
        data = await response.json()
        error = data.get("error")
        if error == "No apikey provided.":
            raise NoAPIKeyException("no API key is provided")
        elif error == "Not enough requests.":
            raise APILimitException("no request remains")
        else:
            response.raise_for_status()
    elif status == 404:
        raise NotFoundException("not found")
    elif status == 500:
        data = await response.json()
        # TODO: If the response is an unexpected one, execute 'response.raise_for_status()'.
        errors = data.get("errors")[0]
        raise InvalidRequestException(errors)
    else:
        response.raise_for_status()
