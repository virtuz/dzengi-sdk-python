import pytest
import responses as responses_lib

from dzengi_com_client import DzengiClient, Interval

LIVE_URL = DzengiClient.LIVE_URL


@pytest.fixture
def client():
    return DzengiClient(api_key="test_key", api_secret="test_secret")


@responses_lib.activate
def test_get_server_time(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "time",
        json={"serverTime": 1699900000000},
    )
    result = client.get_server_time()
    assert result["serverTime"] == 1699900000000


@responses_lib.activate
def test_get_exchange_info(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "exchangeInfo",
        json={"symbols": [], "timezone": "UTC"},
    )
    result = client.get_exchange_info()
    assert "symbols" in result


@responses_lib.activate
def test_get_order_book(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "depth",
        json={"bids": [], "asks": []},
    )
    result = client.get_order_book("BTC/USD")
    assert "bids" in result
    assert "asks" in result


@responses_lib.activate
def test_get_agg_trades(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "aggTrades",
        json=[{"a": 1, "p": "50000", "q": "0.1"}],
    )
    result = client.get_agg_trades("BTC/USD")
    assert len(result) == 1


@responses_lib.activate
def test_get_klines(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "klines",
        json=[[1699900000000, "50000", "51000", "49000", "50500", "100"]],
    )
    result = client.get_klines("BTC/USD", Interval.H1)
    assert len(result) == 1


@responses_lib.activate
def test_get_ticker_24hr(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "ticker/24hr",
        json={"symbol": "BTC/USD", "priceChange": "100"},
    )
    result = client.get_ticker_24hr("BTC/USD")
    assert result["symbol"] == "BTC/USD"
