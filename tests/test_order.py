import pytest
import responses as responses_lib

from dzengi_com_client import DzengiClient, OrderSide, OrderType

LIVE_URL = DzengiClient.LIVE_URL


@pytest.fixture
def client():
    return DzengiClient(api_key="test_key", api_secret="test_secret")


@responses_lib.activate
def test_get_open_orders(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "openOrders",
        json=[{"orderId": "123", "symbol": "BTC/USD"}],
    )
    result = client.get_open_orders()
    assert len(result) == 1


@responses_lib.activate
def test_get_order(client):
    responses_lib.add(
        responses_lib.GET,
        LIVE_URL + "fetchOrder",
        json={"orderId": "123", "symbol": "BTC/USD", "status": "NEW"},
    )
    result = client.get_order("BTC/USD", order_id="123")
    assert result["orderId"] == "123"


@responses_lib.activate
def test_create_order(client):
    responses_lib.add(
        responses_lib.POST,
        LIVE_URL + "order",
        json={"orderId": "456", "symbol": "BTC/USD", "status": "NEW"},
    )
    result = client.create_order(
        symbol="BTC/USD",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        quantity=0.1,
        price=50000,
    )
    assert result["orderId"] == "456"


@responses_lib.activate
def test_create_order_leverage(client):
    responses_lib.add(
        responses_lib.POST,
        LIVE_URL + "order",
        json={"orderId": "789", "symbol": "BTC/USD_LEVERAGE", "status": "NEW"},
    )
    result = client.create_order(
        symbol="BTC/USD_LEVERAGE",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=0.1,
        account_id="acc123",
        leverage=10,
        stop_loss=45000.0,
        take_profit=55000.0,
        guaranteed_stop_loss=False,
        trailing_stop_loss=False,
    )
    assert result["orderId"] == "789"


@responses_lib.activate
def test_edit_order(client):
    responses_lib.add(
        responses_lib.PUT,
        LIVE_URL + "order",
        json=[{"orderId": "00a0c503-0079-54c4-0000-0000803400c0"}],
    )
    result = client.edit_order(order_id="00a0c503-0079-54c4-0000-0000803400c0", price=51000.0)
    assert result[0]["orderId"] == "00a0c503-0079-54c4-0000-0000803400c0"


@responses_lib.activate
def test_cancel_order(client):
    responses_lib.add(
        responses_lib.DELETE,
        LIVE_URL + "order",
        json={"orderId": "123", "status": "CANCELED"},
    )
    result = client.cancel_order("BTC/USD", order_id="123")
    assert result["status"] == "CANCELED"
