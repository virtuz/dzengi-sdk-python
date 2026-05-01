from .base import BaseAPI


class LeverageAPI(BaseAPI):
    def get_trading_positions(self, recv_window=None):
        params = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("tradingPositions", params=params, signed=True)

    def get_trading_positions_history(self, start_time=None, end_time=None, limit: int = 500, recv_window=None):
        params = {"startTime": start_time, "endTime": end_time, "limit": limit}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("tradingPositionsHistory", params=params, signed=True)

    def get_leverage_settings(self, symbol: str, recv_window=None):
        params = {"symbol": symbol}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("leverageSettings", params=params, signed=True)

    def close_trading_position(self, position_id, recv_window=None):
        data = {"positionId": position_id}
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._post("closeTradingPosition", data=data, signed=True)

    def update_trading_order(self, order_id, stop_loss=None, take_profit=None, recv_window=None):
        data = {
            "orderId": order_id,
            "stopLoss": stop_loss,
            "takeProfit": take_profit,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._post("updateTradingOrder", data=data, signed=True)

    def update_trading_position(self, position_id, stop_loss=None, take_profit=None, recv_window=None):
        data = {
            "positionId": position_id,
            "stopLoss": stop_loss,
            "takeProfit": take_profit,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._post("updateTradingPosition", data=data, signed=True)
