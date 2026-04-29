from .base import BaseAPI


class AccountAPI(BaseAPI):
    def get_account(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("account", params=params, signed=True)

    def get_my_trades(self, symbol: str, limit: int = 500, from_id=None, start_time=None, end_time=None, recv_window=None):
        params = {
            "symbol": symbol,
            "limit": limit,
            "fromId": from_id,
            "startTime": start_time,
            "endTime": end_time,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("myTrades", params=params, signed=True)

    def get_funding_limits(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("fundingLimits", params=params, signed=True)

    def get_ledger(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        params = {"startTime": start_time, "endTime": end_time, "limit": limit}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("ledger", params=params, signed=True)

    def get_trading_fees(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("tradingFees", params=params, signed=True)

    def get_trading_limits(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("tradingLimits", params=params, signed=True)

    def get_currencies(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("currencies", params=params, signed=True)

    def get_deposit_address(self, coin: str, recv_window=None):
        params = {"coin": coin}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("depositAddress", params=params, signed=True)

    def get_deposits(self, coin=None, status=None, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        params = {
            "coin": coin,
            "status": status,
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("deposits", params=params, signed=True)

    def get_withdrawals(self, coin=None, status=None, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        params = {
            "coin": coin,
            "status": status,
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("withdrawals", params=params, signed=True)

    def get_transactions(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        params = {"startTime": start_time, "endTime": end_time, "limit": limit}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("transactions", params=params, signed=True)
