from pathlib import Path
from uuid import uuid4

import pytest
from requests import HTTPError, Request, Response

from zenserp.exceptions import (
    APILimitException,
    InvalidRequestException,
    NoAPIKeyException,
    NotFoundException,
    WrongAPIKeyException,
    status_handler,
)

ERROR_RESPONSES_DIR = Path(__file__).parent / "data/errors"
NO_API_KEY_RESPONSE_JSON = ERROR_RESPONSES_DIR / "no_api_key.json"
NOT_ENOUGH_REQUESTS_JSON = ERROR_RESPONSES_DIR / "not_enough_requests.json"
INVALID_REQUEST_JSON = ERROR_RESPONSES_DIR / "invalid_request.json"


def test_invalid_request_exception():
    errors = {
        "location": "location not found.",
        "search_engine": "search engine not found.",
    }
    actual = InvalidRequestException(errors).__str__()
    expect = "invalid request: (location: location not found, search_engine: search engine not found)"
    assert actual == expect


class TestStatusHandler:
    def test_ok(self):
        @status_handler
        def return_ok():
            resp = Response()
            resp.status_code = 200
            return resp

        return_ok()

    def test_no_api_key(self):
        @status_handler
        def return_no_api_key_response():
            resp = Response()
            resp.status_code = 403
            with NO_API_KEY_RESPONSE_JSON.open("rb") as f:
                resp._content = f.read()
            return resp

        with pytest.raises(NoAPIKeyException):
            return_no_api_key_response()

    def test_wrong_api_key(self):
        @status_handler
        def return_wrong_api_key_response():
            resp = Response()
            resp.status_code = 403
            resp.request = Request(
                "GET",
                "https://app.zenserp.com/api/v2/status",
                headers={"apikey": "WRONG_API_KEY"},
            ).prepare()
            with NOT_ENOUGH_REQUESTS_JSON.open("rb") as f:
                resp._content = f.read()
            return resp

        with pytest.raises(WrongAPIKeyException):
            return_wrong_api_key_response()

    def test_api_limit(self):
        @status_handler
        def return_api_limit_response():
            resp = Response()
            resp.status_code = 403
            resp.request = Request(
                "GET",
                "https://app.zenserp.com/api/v2/status",
                headers={"apikey": uuid4().hex},
            ).prepare()
            with NOT_ENOUGH_REQUESTS_JSON.open("rb") as f:
                resp._content = f.read()
            return resp

        with pytest.raises(APILimitException):
            return_api_limit_response()

    def test_not_found(self):
        @status_handler
        def return_not_found_response():
            resp = Response()
            resp.status_code = 404
            return resp

        with pytest.raises(NotFoundException):
            return_not_found_response()

    def test_invalid_request(self):
        @status_handler
        def return_invalid_request_response():
            resp = Response()
            resp.status_code = 500
            with INVALID_REQUEST_JSON.open("rb") as f:
                resp._content = f.read()
            return resp

        with pytest.raises(InvalidRequestException):
            return_invalid_request_response()

    def test_unknown(self):
        @status_handler
        def return_unknown_response():
            resp = Response()
            resp.status_code = 429
            return resp

        with pytest.raises(HTTPError):
            return_unknown_response()
