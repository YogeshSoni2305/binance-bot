import click
from dotenv import load_dotenv
import os

from .bot import TradingBot
from .config import load_config

load_dotenv()
config = load_config()

@click.group()
def cli():
    """Binance Futures CLI Trading Bot"""
    pass

@cli.command(help="Check futures account balance")
def balance():
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    balance = bot.get_balance()
    click.echo(f"USDT Balance: {balance['balance']} USDT")

@cli.command(name="market", help="Place a market order")
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"]))
@click.option("--quantity", required=True, type=float)
def market(symbol, side, quantity):
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    order = bot.place_market_order(symbol, side, quantity)
    click.echo(order)

@cli.command(name="limit", help="Place a limit order")
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"]))
@click.option("--quantity", required=True, type=float)
@click.option("--price", required=True, type=float)
def limit(symbol, side, quantity, price):
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    order = bot.place_limit_order(symbol, side, quantity, price)
    click.echo(order)

@cli.command(name="stop-limit", help="Place a stop-limit order")
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"]))
@click.option("--quantity", required=True, type=float)
@click.option("--stop-price", required=True, type=float)
@click.option("--limit-price", required=True, type=float)
@click.option("--reduce-only", is_flag=True)
def stop_limit(symbol, side, quantity, stop_price, limit_price, reduce_only):
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price, reduce_only)
    click.echo(order)

@cli.command(name="open-orders", help="List open orders for a symbol")
@click.option("--symbol", required=True)
def open_orders(symbol):
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    orders = bot.get_open_orders(symbol)
    click.echo(orders)

@cli.command(name="cancel-order", help="Cancel an order by ID")
@click.option("--symbol", required=True)
@click.option("--order-id", required=True, type=int)
def cancel_order(symbol, order_id):
    bot = TradingBot(config["api_key"], config["api_secret"], testnet=True)
    result = bot.cancel_order(symbol, order_id)
    click.echo(result)

if __name__ == "__main__":
    cli()
