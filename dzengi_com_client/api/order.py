from .base import BaseAPI


class OrderAPI(BaseAPI):
    def get_open_orders(self, symbol=None, recv_window=None):
        params = {"symbol": symbol}
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("openOrders", params=params, signed=True)

    def get_order(self, symbol: str, order_id=None, orig_client_order_id=None, recv_window=None):
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "origClientOrderId": orig_client_order_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._get("fetchOrder", params=params, signed=True)

    def create_order(self, symbol: str, side, order_type, quantity,
                     price=None, account_id=None, expire_timestamp=None,
                     guaranteed_stop_loss=None, leverage=None, profit_distance=None,
                     stop_distance=None, stop_loss=None, take_profit=None,
                     trailing_stop_loss=None, new_order_resp_type=None, recv_window=None):
        data = {
            "symbol": symbol,
            "side": str(side),
            "type": str(order_type),
            "quantity": quantity,
            "price": price,
            "accountId": account_id,
            "expireTimestamp": expire_timestamp,
            "guaranteedStopLoss": guaranteed_stop_loss,
            "leverage": leverage,
            "profitDistance": profit_distance,
            "stopDistance": stop_distance,
            "stopLoss": stop_loss,
            "takeProfit": take_profit,
            "trailingStopLoss": trailing_stop_loss,
            "newOrderRespType": new_order_resp_type,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._post("order", data=data, signed=True)

    def edit_order(self, order_id: str, price=None, expire_timestamp=None, recv_window=None):
        data = {
            "orderId": order_id,
            "price": price,
            "expireTimestamp": expire_timestamp,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._put("order", data=data, signed=True)

    def cancel_order(self, symbol: str, order_id: str, recv_window=None):
        params = {
            "symbol": symbol,
            "orderId": order_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._delete("order", params=params, signed=True)
