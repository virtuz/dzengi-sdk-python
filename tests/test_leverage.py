import pytest
import responses as responses_lib

from dzengi_com_client import DzengiClient

LIVE_URL = DzengiClient.LIVE_URL


@pytest.fixture
def client():
    return DzengiClient(api_key="test_key", api_secret="test_secret")


@responses_lib.activate
def test_get_positions(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "tradingPositions",
        json=[{"positionId": "123", "symbol": "ETH/USD"}],
    )
    result = client.get_positions()
    assert len(result) == 1
    assert result[0]["positionId"] == "123"


@responses_lib.activate
def test_get_trading_positions(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "tradingPositions",
        json=[{"positionId": "789", "symbol": "BTC/USD"}],
    )
    result = client.get_trading_positions()
    assert len(result) == 1
    assert result[0]["positionId"] == "789"


@responses_lib.activate
def test_close_trading_position(client):
    responses_lib.add(
        responses_lib.POST,
        LIVE_URL + "closeTradingPosition",
        json={"positionId": "789", "status": "CLOSED"},
    )
    result = client.close_trading_position("789")
    assert result["status"] == "CLOSED"
