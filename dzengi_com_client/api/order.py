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

    def create_order(self, symbol: str, side, order_type, quantity, price=None, stop_price=None, time_in_force=None, new_client_order_id=None, recv_window=None):
        data = {
            "symbol": symbol,
            "side": str(side),
            "type": str(order_type),
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "timeInForce": time_in_force,
            "newClientOrderId": new_client_order_id,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._post("order", data=data, signed=True)

    def edit_order(self, symbol: str, order_id, quantity=None, price=None, recv_window=None):
        data = {
            "symbol": symbol,
            "orderId": order_id,
            "quantity": quantity,
            "price": price,
        }
        if recv_window is not None:
            data["recvWindow"] = recv_window
        return self._put("order", data=data, signed=True)

    def cancel_order(self, symbol: str, order_id=None, orig_client_order_id=None, recv_window=None):
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "origClientOrderId": orig_client_order_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self._delete("order", params=params, signed=True)
