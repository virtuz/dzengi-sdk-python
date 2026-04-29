from enum import Enum


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"


class Interval(str, Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"


class OrderStatus(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class DepositStatus(int, Enum):
    PENDING = 0
    CREDITED_BUT_CANNOT_WITHDRAW = 1
    SUCCESS = 6
    FAILED = 4


class WithdrawStatus(int, Enum):
    EMAIL_SENT = 0
    CANCELLED = 1
    AWAITING_APPROVAL = 2
    REJECTED = 3
    PROCESSING = 4
    FAILURE = 5
    COMPLETED = 6


class PositionType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class MarketType(str, Enum):
    SPOT = "SPOT"
    LEVERAGE = "LEVERAGE"
