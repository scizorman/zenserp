from pathlib import Path

from zenserp.exceptions import InvalidRequestException

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
