from __future__ import annotations

from types import TracebackType
from typing import Any, Optional, Type
from urllib.parse import urljoin

from requests import Response, Session


class Client:
    _base_url = "https://app.zenserp.com"

    def __init__(self, api_key: str):
        if api_key == "":
            raise ValueError("no API key provided")
        self._session = Session()
        self._session.headers["apikey"] = api_key

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        return self.close()

    def close(self) -> None:
        """Closes this client."""
        return self._session.close()

    def handle_error(self, response: Response) -> None:
        status_code = response.status_code
        if status_code == 200:
            return None
        elif status_code == 403:
            # TODO: Raise a custom exception about the HTTP status 403.
            message = response.json()["error"]
            raise Exception(message)
        elif status_code == 404:
            # TODO: Raise a custom exception about the HTTP status 404.
            raise response.raise_for_status()
        elif status_code == 500:
            # TODO: Raise a custom exception about the HTTP status 500.
            messages = response.json()["errors"].values()
            raise Exception(messages)
        else:
            raise response.raise_for_status()

    def status(self) -> int:
        """Checks the remaining requests of your API key.

        Returns:
            int: The remaining requests of your API key.
        """
        url = urljoin(self._base_url, "api/v2/status")
        with self._session.get(url) as resp:
            resp.encoding = resp.apparent_encoding
            self.handle_error(resp)
            return resp.json()["remaining_requests"]
