from .base import BaseAPI


class MarketAPI(BaseAPI):
    def get_server_time(self):
        return self._get("time")

    def get_exchange_info(self):
        return self._get("exchangeInfo")

    def get_order_book(self, symbol: str, limit: int = 100):
        params = {"symbol": symbol, "limit": limit}
        return self._get("depth", params=params)

    def get_agg_trades(self, symbol: str, limit: int = 500, from_id=None, start_time=None, end_time=None):
        params = {
            "symbol": symbol,
            "limit": limit,
            "fromId": from_id,
            "startTime": start_time,
            "endTime": end_time,
        }
        return self._get("aggTrades", params=params)

    def get_klines(self, symbol: str, interval, limit: int = 500, start_time=None, end_time=None):
        params = {
            "symbol": symbol,
            "interval": str(interval),
            "limit": limit,
            "startTime": start_time,
            "endTime": end_time,
        }
        return self._get("klines", params=params)

    def get_ticker_24hr(self, symbol=None):
        params = {"symbol": symbol}
        return self._get("ticker/24hr", params=params)
