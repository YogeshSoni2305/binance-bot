
import click
from typing import Dict
from .bot import TradingBot
from .config import load_config
from .logger import setup_logging

def format_order(order: Dict) -> str:
    """Format order details for CLI output.

    Args:
        order: Order response from Binance API.

    Returns:
        Formatted order details.
    """
    return (
        f"Order Placed:\n"
        f"- Type: {order.get('type', 'N/A')}\n"
        f"- Symbol: {order.get('symbol', 'N/A')}\n"
        f"- Side: {order.get('side', 'N/A')}\n"
        f"- Quantity: {order.get('origQty', order.get('quantity', 'N/A'))}\n"
        f"- Status: {order.get('status', 'N/A')}\n"
        f"- Order ID: {order.get('orderId', 'N/A')}"
    )

@click.group()
def cli():
    """Binance Futures Trading Bot CLI."""
    setup_logging()

@cli.command()
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side')
@click.option('--quantity', required=True, type=float, help='Order quantity')
def market(symbol: str, side: str, quantity: float):
    """Place a market order."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        order = bot.place_market_order(symbol, side, quantity)
        click.echo(format_order(order))
    except Exception as e:
        click.echo(f"Error placing market order: {e}", err=True)

@cli.command()
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side')
@click.option('--quantity', required=True, type=float, help='Order quantity')
@click.option('--price', required=True, type=float, help='Limit price')
def limit(symbol: str, side: str, quantity: float, price: float):
    """Place a limit order."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        order = bot.place_limit_order(symbol, side, quantity, price)
        click.echo(format_order(order))
    except Exception as e:
        click.echo(f"Error placing limit order: {e}", err=True)

@cli.command(name='stop_limit')
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side')
@click.option('--quantity', required=True, type=float, help='Order quantity')
@click.option('--stop-price', required=True, type=float, help='Stop price')
@click.option('--limit-price', required=True, type=float, help='Limit price')
def stop_limit(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    """Place a stop-limit order."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        order = bot.place_stop_limit(symbol, side, quantity, stop_price, limit_price)
        click.echo(format_order(order))
    except Exception as e:
        click.echo(f"Error placing stop-limit order: {e}", err=True)

@cli.command()
def balance():
    """Check futures account balance."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        balance = bot.get_account_balance()
        usdt = next((asset for asset in balance if asset['asset'] == 'USDT'), None)
        if usdt:
            click.echo(f"USDT Balance: {usdt['balance']} (Available: {usdt['availableBalance']})")
        else:
            click.echo("No USDT balance found")
    except Exception as e:
        click.echo(f"Error fetching balance: {e}", err=True)

@cli.command(name='open_orders')
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
def open_orders(symbol: str):
    """List open orders for a symbol."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        orders = bot.get_open_orders(symbol)
        if orders:
            for order in orders:
                click.echo(
                    f"Open Order:\n"
                    f"- Symbol: {order.get('symbol', 'N/A')}\n"
                    f"- Type: {order.get('type', 'N/A')}\n"
                    f"- Side: {order.get('side', 'N/A')}\n"
                    f"- Quantity: {order.get('origQty', 'N/A')}\n"
                    f"- Price: {order.get('price', 'N/A')}\n"
                    f"- Stop Price: {order.get('stopPrice', 'N/A')}\n"
                    f"- Order ID: {order.get('orderId', 'N/A')}"
                )
        else:
            click.echo(f"No open orders for {symbol}")
    except Exception as e:
        click.echo(f"Error fetching open orders: {e}", err=True)

@cli.command(name='cancel_order')
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--order-id', required=True, type=int, help='Order ID to cancel')
def cancel_order(symbol: str, order_id: int):
    """Cancel an open order by ID."""
    config = load_config()
    bot = TradingBot(config['api_key'], config['api_secret'], testnet=True)
    try:
        result = bot.cancel_order(symbol, order_id)
        click.echo(f"Order {order_id} canceled for {symbol}")
    except Exception as e:
        click.echo(f"Error canceling order: {e}", err=True)

if __name__ == '__main__':
    cli()
