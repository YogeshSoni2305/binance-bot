
import logging
from typing import Dict, List
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT
from binance.exceptions import BinanceAPIException

class TradingBot:
    """A trading bot for interacting with Binance Futures Testnet."""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.logger.info("Binance client initialized for testnet=%s", testnet)
            self.logger.debug("Futures API URL: %s", self.client.FUTURES_URL)
        except BinanceAPIException as e:
            self.logger.error("Failed to initialize Binance client: %s", e)
            raise

    def validate_symbol(self, symbol: str) -> Dict:
        try:
            exchange_info = self.client.get_exchange_info()
            symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)
            if not symbol_info:
                raise ValueError(f"Invalid symbol: {symbol}")
            self.logger.debug("Validated symbol: %s", symbol)
            return symbol_info
        except BinanceAPIException as e:
            self.logger.error("Failed to validate symbol %s: %s", symbol, e)
            raise ValueError(f"Failed to validate symbol: {e}")

    def place_market_order(self, symbol: str, side: str, quantity: float, reduce_only: bool = False) -> Dict:
        self.validate_symbol(symbol)
        side = side.upper()
        if side not in [SIDE_BUY, SIDE_SELL]:
            raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")

        try:
            price = float(self.client.futures_mark_price(symbol=symbol)['markPrice'])
            notional = quantity * price
            if notional < 100 and not reduce_only:
                raise ValueError(f"Order notional (${notional:.2f}) must be ≥ $100 or use reduce_only=True")

            self.logger.debug("Placing market order: symbol=%s, side=%s, quantity=%s", symbol, side, quantity)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity,
                positionSide='BOTH',
                reduceOnly=reduce_only
            )
            self.logger.info("Placed market order: orderId=%s", order['orderId'])
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place market order: %s", e)
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float, reduce_only: bool = False) -> Dict:
        self.validate_symbol(symbol)
        side = side.upper()
        if side not in [SIDE_BUY, SIDE_SELL]:
            raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")

        notional = quantity * price
        if notional < 100 and not reduce_only:
            raise ValueError(f"Order notional (${notional:.2f}) must be ≥ $100 or use reduce_only=True")

        try:
            self.logger.debug("Placing limit order: symbol=%s, side=%s, quantity=%s, price=%s", symbol, side, quantity, price)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce="GTC",
                quantity=quantity,
                price=price,
                positionSide='BOTH',
                reduceOnly=reduce_only
            )
            self.logger.info("Placed limit order: orderId=%s", order['orderId'])
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place limit order: %s", e)
            raise

    def place_stop_limit(self, symbol: str, side: str, quantity: float, stop_price: float, limit_price: float, reduce_only: bool = False) -> Dict:
        self.validate_symbol(symbol)
        side = side.upper()
        if side not in [SIDE_BUY, SIDE_SELL]:
            raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")

        notional = quantity * limit_price
        if notional < 100 and not reduce_only:
            raise ValueError(f"Order notional (${notional:.2f}) must be ≥ $100 or use reduce_only=True")

        try:
            self.logger.debug("Placing stop-limit order: symbol=%s, side=%s, quantity=%s, stopPrice=%s, limitPrice=%s", symbol, side, quantity, stop_price, limit_price)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce="GTC",
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                positionSide='BOTH',
                reduceOnly=reduce_only
            )
            self.logger.info("Placed stop-limit order: orderId=%s", order['orderId'])
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place stop-limit order: %s", e)
            raise

    def get_account_balance(self) -> List[Dict]:
        try:
            self.logger.debug("Fetching futures account balance")
            balance = self.client.futures_account_balance()
            self.logger.debug("Fetched balance: %s", balance)
            return balance
        except BinanceAPIException as e:
            self.logger.error("Failed to fetch futures account balance: %s", e)
            raise

    def get_open_orders(self, symbol: str) -> List[Dict]:
        self.validate_symbol(symbol)
        try:
            self.logger.debug("Fetching open orders for symbol=%s", symbol)
            orders = self.client.futures_get_open_orders(symbol=symbol)
            self.logger.debug("Fetched %d open orders", len(orders))
            return orders
        except BinanceAPIException as e:
            self.logger.error("Failed to fetch open orders for %s: %s", symbol, e)
            raise

    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        self.validate_symbol(symbol)
        try:
            self.logger.debug("Canceling order: symbol=%s, orderId=%s", symbol, order_id)
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info("Canceled order: orderId=%s", order_id)
            return result
        except BinanceAPIException as e:
            self.logger.error("Failed to cancel order %s for %s: %s", order_id, symbol, e)
            raise
