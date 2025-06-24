# from binance.client import Client
# from binance.exceptions import BinanceAPIException
# from .logger import logger

# class TradingBot:
#     def __init__(self, api_key, api_secret, testnet=True):
#         self.logger = logger
#         self.client = Client(api_key, api_secret)
#         if testnet:
#             self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
#         self.logger.info("Binance client initialized")

#     def validate_symbol(self, symbol):
#         try:
#             info = self.client.futures_exchange_info()
#             for s in info["symbols"]:
#                 if s["symbol"] == symbol:
#                     return s  # Return the full symbol info dict
#             raise ValueError(f"Invalid symbol: {symbol}")
#         except BinanceAPIException as e:
#             self.logger.error("Error validating symbol: %s", e)
#             raise


#     def get_balance(self):
#         try:
#             balances = self.client.futures_account_balance()
#             return next(b for b in balances if b["asset"] == "USDT")
#         except BinanceAPIException as e:
#             self.logger.error("Error fetching balance: %s", e)
#             raise

#     def place_market_order(self, symbol, side, quantity):
#         self.validate_symbol(symbol)
#         try:
#             return self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type="MARKET",
#                 quantity=quantity
#             )
#         except BinanceAPIException as e:
#             self.logger.error("Market order failed: %s", e)
#             raise

#     def place_limit_order(self, symbol, side, quantity, price):
#         self.validate_symbol(symbol)
#         try:
#             return self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type="LIMIT",
#                 quantity=quantity,
#                 price=price,
#                 timeInForce="GTC"
#             )
#         except BinanceAPIException as e:
#             self.logger.error("Limit order failed: %s", e)
#             raise

#     def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price, reduce_only):
#         self.validate_symbol(symbol)
#         try:
#             return self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type="STOP",
#                 quantity=quantity,
#                 stopPrice=stop_price,
#                 price=limit_price,
#                 timeInForce="GTC",
#                 reduceOnly=reduce_only
#             )
#         except BinanceAPIException as e:
#             self.logger.error("Stop-limit order failed: %s", e)
#             raise

#     def get_open_orders(self, symbol):
#         self.validate_symbol(symbol)
#         try:
#             return self.client.futures_get_open_orders(symbol=symbol)
#         except BinanceAPIException as e:
#             self.logger.error("Fetching open orders failed: %s", e)
#             raise

#     def cancel_order(self, symbol, order_id):
#         try:
#             return self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
#         except BinanceAPIException as e:
#             self.logger.error("Cancel order failed: %s", e)
#             raise


from binance.client import Client
from binance.exceptions import BinanceAPIException
from .logger import logger

class TradingBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = logger
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.logger.info("Binance Futures client initialized (Testnet=%s)", testnet)

    def validate_symbol(self, symbol):
        try:
            info = self.client.futures_exchange_info()
            for s in info["symbols"]:
                if s["symbol"] == symbol:
                    self.logger.debug("Validated trading symbol: %s", symbol)
                    return s
            self.logger.warning("Symbol validation failed: %s", symbol)
            raise ValueError(f"Invalid symbol: {symbol}")
        except BinanceAPIException as e:
            self.logger.error("Error validating symbol %s: %s", symbol, e)
            raise

    def get_balance(self):
        try:
            balances = self.client.futures_account_balance()
            usdt_balance = next(b for b in balances if b["asset"] == "USDT")
            self.logger.info("Fetched USDT balance: %s", usdt_balance["balance"])
            return usdt_balance
        except BinanceAPIException as e:
            self.logger.error("Error fetching balance: %s", e)
            raise

    def place_market_order(self, symbol, side, quantity):
        self.validate_symbol(symbol)
        try:
            self.logger.info("Placing MARKET order — Symbol: %s | Side: %s | Qty: %s", symbol, side, quantity)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            self.logger.debug("Market order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Market order failed: %s", e)
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        self.validate_symbol(symbol)
        try:
            self.logger.info("Placing LIMIT order — Symbol: %s | Side: %s | Qty: %s | Price: %s", symbol, side, quantity, price)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )
            self.logger.debug("Limit order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Limit order failed: %s", e)
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price, reduce_only):
        self.validate_symbol(symbol)
        try:
            self.logger.info(
                "Placing STOP-LIMIT order — Symbol: %s | Side: %s | Qty: %s | Stop: %s | Limit: %s | ReduceOnly: %s",
                symbol, side, quantity, stop_price, limit_price, reduce_only
            )
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce="GTC",
                reduceOnly=reduce_only
            )
            self.logger.debug("Stop-limit order response: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Stop-limit order failed: %s", e)
            raise

    def get_open_orders(self, symbol):
        self.validate_symbol(symbol)
        try:
            self.logger.info("Fetching open orders for symbol: %s", symbol)
            orders = self.client.futures_get_open_orders(symbol=symbol)
            self.logger.debug("Open orders response: %s", orders)
            return orders
        except BinanceAPIException as e:
            self.logger.error("Fetching open orders failed: %s", e)
            raise

    def cancel_order(self, symbol, order_id):
        try:
            self.logger.info("Cancelling order — Symbol: %s | Order ID: %s", symbol, order_id)
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.debug("Cancel order response: %s", result)
            return result
        except BinanceAPIException as e:
            self.logger.error("Cancel order failed: %s", e)
            raise
