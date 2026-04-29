# dzengi-com-client

> **Disclaimer:** This is an **unofficial** Python SDK for the [dzengi.com](https://dzengi.com) cryptocurrency exchange API. It is not affiliated with or endorsed by dzengi.com.

## Installation

```bash
pip install dzengi-com-client
```

Or install from source:

```bash
git clone https://github.com/virtuz/dzengi-sdk-python.git
cd dzengi-sdk-python
pip install -e .
```

## Quick Start

```python
from dzengi_com_client import DzengiClient, OrderSide, OrderType, Interval

# Live trading
client = DzengiClient(api_key="your_api_key", api_secret="your_api_secret")

# Demo/testnet mode
demo_client = DzengiClient(api_key="your_api_key", api_secret="your_api_secret", testnet=True)

# Public endpoints (no auth required)
server_time = client.get_server_time()
exchange_info = client.get_exchange_info()
order_book = client.get_order_book("BTC/USD", limit=10)
klines = client.get_klines("BTC/USD", Interval.H1, limit=100)
ticker = client.get_ticker_24hr("BTC/USD")

# Private endpoints (auth required)
account = client.get_account()
trades = client.get_my_trades("BTC/USD")
open_orders = client.get_open_orders()

# Create a limit order
order = client.create_order(
    symbol="BTC/USD",
    side=OrderSide.BUY,
    order_type=OrderType.LIMIT,
    quantity=0.001,
    price=50000.0,
)

# Cancel an order
client.cancel_order("BTC/USD", order_id=order["orderId"])

# Leverage positions
positions = client.get_trading_positions()
client.close_trading_position(positions[0]["positionId"])
```

## API Reference

### Market Endpoints (Public)

| Method | Description |
|--------|-------------|
| `get_server_time()` | Get server time |
| `get_exchange_info()` | Get exchange info |
| `get_order_book(symbol, limit=100)` | Get order book |
| `get_agg_trades(symbol, limit=500, ...)` | Get aggregated trades |
| `get_klines(symbol, interval, limit=500, ...)` | Get candlestick data |
| `get_ticker_24hr(symbol=None)` | Get 24hr ticker |

### Account Endpoints (Private)

| Method | Description |
|--------|-------------|
| `get_account()` | Get account info |
| `get_my_trades(symbol, ...)` | Get trade history |
| `get_funding_limits()` | Get funding limits |
| `get_ledger(...)` | Get ledger entries |
| `get_trading_fees()` | Get trading fees |
| `get_trading_limits()` | Get trading limits |
| `get_currencies()` | Get currencies list |
| `get_deposit_address(coin)` | Get deposit address |
| `get_deposits(...)` | Get deposits list |
| `get_withdrawals(...)` | Get withdrawals list |
| `get_transactions(...)` | Get transactions list |

### Order Endpoints (Private)

| Method | Description |
|--------|-------------|
| `get_open_orders(symbol=None)` | Get open orders |
| `get_order(symbol, order_id=None, ...)` | Get a specific order |
| `create_order(symbol, side, order_type, quantity, ...)` | Create a new order |
| `edit_order(symbol, order_id, ...)` | Edit an existing order |
| `cancel_order(symbol, order_id=None, ...)` | Cancel an order |

### Leverage Endpoints (Private)

| Method | Description |
|--------|-------------|
| `get_trading_positions()` | Get open leverage positions |
| `get_trading_positions_history(...)` | Get positions history |
| `get_leverage_settings(symbol)` | Get leverage settings |
| `close_trading_position(position_id)` | Close a position |
| `update_trading_order(order_id, ...)` | Update trading order SL/TP |
| `update_trading_position(position_id, ...)` | Update position SL/TP |

## Enums

```python
from dzengi_com_client import OrderSide, OrderType, Interval
from dzengi_com_client.enums import OrderStatus, DepositStatus, WithdrawStatus, PositionType, MarketType

OrderSide.BUY     # "BUY"
OrderSide.SELL    # "SELL"

OrderType.LIMIT        # "LIMIT"
OrderType.MARKET       # "MARKET"
OrderType.STOP         # "STOP"
OrderType.STOP_MARKET  # "STOP_MARKET"

Interval.M1   # "1m"
Interval.M5   # "5m"
Interval.H1   # "1h"
Interval.D1   # "1d"
```

## Official Documentation

- [dzengi.com API Docs](https://currency.com/api)
