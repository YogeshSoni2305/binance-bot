import typer
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import (
    SIDE_BUY, SIDE_SELL,
    ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC
)
from .config import load_config
from .logger import logger

cfg = load_config()

class TradingBot:
    def __init__(self):
        self.client = Client(cfg["API_KEY"], cfg["API_SECRET"])
        self.logger = logger
        self.client.FUTURES_URL = cfg["BASE_URL"]
        logger.info("✅ Binance Futures client initialized (Testnet=True)")

    def validate_symbol(self, symbol: str):
        info = self.client.futures_exchange_info()
        for s in info.get("symbols", []):
            if s["symbol"] == symbol:
                logger.debug("Validated symbol: %s", symbol)
                return s
        logger.error("Invalid symbol: %s", symbol)
        raise ValueError(f"Invalid symbol: {symbol}")

    def get_balance(self):
        try:
            data = self.client.futures_account_balance()
            usdt = {b["asset"]: b["balance"] for b in data if float(b["balance"]) > 0}
            logger.info("Fetched balance: %s", usdt)
            return usdt
        except BinanceAPIException as e:
            logger.error("Balance error: %s", e)
            raise

    def place_market_order(self, symbol, side, quantity):
        self.validate_symbol(symbol)
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logger.info("✅ Market order: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Market order failed: %s", e)
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        self.validate_symbol(symbol)
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(price)
            )
            logger.info("✅ Limit order: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Limit order failed: %s", e)
            raise

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price, reduce_only=False):
        self.logger.info(f"🛑 Placing stop-limit order: {side} {quantity} @ {price} (stop {stop_price})")
        try:
            order_params = {
                "symbol": symbol,
                "side": SIDE_BUY if side == "BUY" else SIDE_SELL,
                "type": "STOP",
                "quantity": quantity,
                "price": str(price),
                "stopPrice": str(stop_price),
                "timeInForce": "GTC",
            }
            if reduce_only:
                order_params["reduceOnly"] = True

            order = self.client.futures_create_order(**order_params)
            self.logger.info(f"✅ Stop-limit order placed: {order['orderId']}")
            return order
        except BinanceAPIException as e:
            self.logger.error(f"❌ Stop-limit order error: {e}")
            raise typer.Exit(code=1)

    def get_open_orders(self, symbol):
        self.validate_symbol(symbol)
        try:
            orders = self.client.futures_get_open_orders(symbol=symbol)
            logger.info("Open orders for %s: %s", symbol, orders)
            return orders
        except BinanceAPIException as e:
            logger.error("Open orders error: %s", e)
            raise

    def cancel_order(self, symbol, order_id):
        self.validate_symbol(symbol)
        try:
            res = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logger.info("✅ Order cancelled: %s", res)
            return res
        except BinanceAPIException as e:
            logger.error("Cancel order failed: %s", e)
            raise
