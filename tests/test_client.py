import io
import logging

import pytest
import responses as responses_lib

from dzengi_com_client import DzengiClient, DzengiAPIException


@pytest.fixture
def client():
    return DzengiClient(api_key="test_key", api_secret="test_secret")


@pytest.fixture
def demo_client():
    return DzengiClient(api_key="test_key", api_secret="test_secret", testnet=True)


def make_test_logger():
    stream = io.StringIO()
    logger = logging.Logger("dzengi-test-logger", level=logging.DEBUG)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger, stream


def test_client_init(client):
    assert client._api_key == "test_key"
    assert client._api_secret == "test_secret"


def test_client_live_url(client):
    assert client._market._base_url == DzengiClient.LIVE_URL


def test_client_demo_url(demo_client):
    assert demo_client._market._base_url == DzengiClient.DEMO_URL


@responses_lib.activate
def test_api_exception_on_error():
    responses_lib.add(
        responses_lib.GET,
        DzengiClient.LIVE_URL + "time",
        json={"code": -1121, "msg": "Invalid symbol."},
        status=400,
    )
    client = DzengiClient(api_key="test_key", api_secret="test_secret")
    with pytest.raises(DzengiAPIException) as exc_info:
        client.get_server_time()
    assert exc_info.value.status_code == 400
    assert exc_info.value.code == -1121
    assert "Invalid symbol" in exc_info.value.message


@responses_lib.activate
def test_debug_logging_includes_redacted_request_and_response_details():
    responses_lib.add(
        responses_lib.GET,
        DzengiClient.LIVE_URL + "account",
        json={"balances": [], "accountType": "SPOT"},
    )
    logger, stream = make_test_logger()

    client = DzengiClient(api_key="test_key", api_secret="test_secret", logger=logger, debug=True)
    client.get_account()

    output = stream.getvalue()
    assert "Request: GET https://api-adapter.dzengi.com/api/v2/account" in output
    assert '"signature": "<redacted>"' in output
    assert "test_secret" not in output
    assert "test_key" not in output
    assert "Response: GET https://api-adapter.dzengi.com/api/v2/account status=200" in output
    assert '"balances": []' in output


@responses_lib.activate
def test_debug_logging_is_disabled_by_default():
    responses_lib.add(
        responses_lib.GET,
        DzengiClient.LIVE_URL + "time",
        json={"serverTime": 1699900000000},
    )
    logger, stream = make_test_logger()

    client = DzengiClient(api_key="test_key", api_secret="test_secret", logger=logger)
    client.get_server_time()

    assert stream.getvalue() == ""


@responses_lib.activate
def test_timestamp_mismatch_auto_retries_and_succeeds():
    """On a -1021 timestamp error the client syncs server time and retries."""
    LIVE_URL = DzengiClient.LIVE_URL

    # First call to /account returns -1021
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "account",
        json={"code": -1021, "msg": "Timestamp for this request was 1000 ms ahead of the server's time."},
        status=400,
    )
    # Time-sync call to /time
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "time",
        json={"serverTime": 1777654574394},
    )
    # Retry call to /account succeeds
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "account",
        json={"balances": [], "accountType": "SPOT"},
    )

    client = DzengiClient(api_key="test_key", api_secret="test_secret")
    result = client.get_account()
    assert "balances" in result


@responses_lib.activate
def test_timestamp_mismatch_raises_if_retry_also_fails():
    """If the retry after time-sync also fails, the exception is raised."""
    LIVE_URL = DzengiClient.LIVE_URL

    # First call returns -1021
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "account",
        json={"code": -1021, "msg": "Timestamp mismatch."},
        status=400,
    )
    # Time-sync
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "time",
        json={"serverTime": 1777654574394},
    )
    # Retry also fails with -1021
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "account",
        json={"code": -1021, "msg": "Timestamp mismatch."},
        status=400,
    )

    client = DzengiClient(api_key="test_key", api_secret="test_secret")
    with pytest.raises(DzengiAPIException) as exc_info:
        client.get_account()
    assert exc_info.value.code == -1021
