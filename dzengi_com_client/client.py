import requests

from .api.account import AccountAPI
from .api.leverage import LeverageAPI
from .api.market import MarketAPI
from .api.order import OrderAPI


class DzengiClient:
    LIVE_URL = "https://api-adapter.backend.currency.com/api/v2/"
    DEMO_URL = "https://demo-api-adapter.backend.currency.com/api/v2/"

    def __init__(self, api_key: str = "", api_secret: str = "", testnet: bool = False, recv_window: int = 5000):
        self._api_key = api_key
        self._api_secret = api_secret
        base_url = self.DEMO_URL if testnet else self.LIVE_URL

        session = requests.Session()
        session.headers.update({
            "X-MBX-APIKEY": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

        kwargs = dict(api_key=api_key, api_secret=api_secret, base_url=base_url, session=session, recv_window=recv_window)
        self._market = MarketAPI(**kwargs)
        self._account = AccountAPI(**kwargs)
        self._order = OrderAPI(**kwargs)
        self._leverage = LeverageAPI(**kwargs)

    # Market endpoints
    def get_server_time(self):
        return self._market.get_server_time()

    def get_exchange_info(self):
        return self._market.get_exchange_info()

    def get_order_book(self, symbol: str, limit: int = 100):
        return self._market.get_order_book(symbol, limit)

    def get_agg_trades(self, symbol: str, limit: int = 500, from_id=None, start_time=None, end_time=None):
        return self._market.get_agg_trades(symbol, limit, from_id, start_time, end_time)

    def get_klines(self, symbol: str, interval, limit: int = 500, start_time=None, end_time=None):
        return self._market.get_klines(symbol, interval, limit, start_time, end_time)

    def get_ticker_24hr(self, symbol=None):
        return self._market.get_ticker_24hr(symbol)

    # Account endpoints
    def get_account(self, recv_window=None):
        return self._account.get_account(recv_window)

    def get_my_trades(self, symbol: str, limit: int = 500, from_id=None, start_time=None, end_time=None, recv_window=None):
        return self._account.get_my_trades(symbol, limit, from_id, start_time, end_time, recv_window)

    def get_funding_limits(self, recv_window=None):
        return self._account.get_funding_limits(recv_window)

    def get_ledger(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        return self._account.get_ledger(start_time, end_time, limit, recv_window)

    def get_trading_fees(self, recv_window=None):
        return self._account.get_trading_fees(recv_window)

    def get_trading_limits(self, recv_window=None):
        return self._account.get_trading_limits(recv_window)

    def get_currencies(self, recv_window=None):
        return self._account.get_currencies(recv_window)

    def get_deposit_address(self, coin: str, recv_window=None):
        return self._account.get_deposit_address(coin, recv_window)

    def get_deposits(self, coin=None, status=None, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        return self._account.get_deposits(coin, status, start_time, end_time, limit, recv_window)

    def get_withdrawals(self, coin=None, status=None, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        return self._account.get_withdrawals(coin, status, start_time, end_time, limit, recv_window)

    def get_transactions(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        return self._account.get_transactions(start_time, end_time, limit, recv_window)

    # Order endpoints
    def get_open_orders(self, symbol=None, recv_window=None):
        return self._order.get_open_orders(symbol, recv_window)

    def get_order(self, symbol: str, order_id=None, orig_client_order_id=None, recv_window=None):
        return self._order.get_order(symbol, order_id, orig_client_order_id, recv_window)

    def create_order(self, symbol: str, side, order_type, quantity, price=None, stop_price=None, time_in_force=None, new_client_order_id=None, recv_window=None):
        return self._order.create_order(symbol, side, order_type, quantity, price, stop_price, time_in_force, new_client_order_id, recv_window)

    def edit_order(self, symbol: str, order_id, quantity=None, price=None, recv_window=None):
        return self._order.edit_order(symbol, order_id, quantity, price, recv_window)

    def cancel_order(self, symbol: str, order_id=None, orig_client_order_id=None, recv_window=None):
        return self._order.cancel_order(symbol, order_id, orig_client_order_id, recv_window)

    # Leverage endpoints
    def get_trading_positions(self, recv_window=None):
        return self._leverage.get_trading_positions(recv_window)

    def get_trading_positions_history(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        return self._leverage.get_trading_positions_history(start_time, end_time, limit, recv_window)

    def get_leverage_settings(self, symbol: str, recv_window=None):
        return self._leverage.get_leverage_settings(symbol, recv_window)

    def close_trading_position(self, position_id, recv_window=None):
        return self._leverage.close_trading_position(position_id, recv_window)

    def update_trading_order(self, order_id, stop_loss=None, take_profit=None, recv_window=None):
        return self._leverage.update_trading_order(order_id, stop_loss, take_profit, recv_window)

    def update_trading_position(self, position_id, stop_loss=None, take_profit=None, recv_window=None):
        return self._leverage.update_trading_position(position_id, stop_loss, take_profit, recv_window)
