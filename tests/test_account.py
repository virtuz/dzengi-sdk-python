import pytest
import responses as responses_lib

from dzengi_com_client import DzengiClient

LIVE_URL = DzengiClient.LIVE_URL


@pytest.fixture
def client():
    return DzengiClient(api_key="test_key", api_secret="test_secret")


@responses_lib.activate
def test_get_account(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "account",
        json={"balances": [], "accountType": "SPOT"},
    )
    result = client.get_account()
    assert "balances" in result


@responses_lib.activate
def test_get_my_trades(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "myTrades",
        json=[{"id": 1, "symbol": "BTC/USD", "price": "50000"}],
    )
    result = client.get_my_trades("BTC/USD")
    assert len(result) == 1
    assert result[0]["symbol"] == "BTC/USD"
