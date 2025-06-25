import typer
from rich.console import Console
from rich.table import Table
from binance_bot.bot import TradingBot
from binance.exceptions import BinanceAPIException

app = typer.Typer()
console = Console()

bot = TradingBot()

@app.command("balance")
def check_balance():
    """Check futures account balance"""
    balances = bot.get_balance()
    for asset, balance in balances.items():
        console.print(f"[cyan]{asset}[/cyan]: {balance}")

@app.command("market")
def place_market_order(
    symbol: str = typer.Option(..., "--symbol"),
    side: str = typer.Option(..., "--side"),
    quantity: float = typer.Option(..., "--quantity"),
):
    """Place a market order"""
    try:
        bot.place_market_order(symbol, side.upper(), quantity)
    except BinanceAPIException as e:
        console.print(f"[red]Error:[/red] {e}")

@app.command("limit")
def place_limit_order(
    symbol: str = typer.Option(..., "--symbol"),
    side: str = typer.Option(..., "--side"),
    quantity: float = typer.Option(..., "--quantity"),
    price: float = typer.Option(..., "--price"),
):
    """Place a limit order"""
    try:
        bot.place_limit_order(symbol, side.upper(), quantity, price)
    except BinanceAPIException as e:
        console.print(f"[red]Error:[/red] {e}")

@app.command("stop-limit")
def place_stop_limit_order(
    symbol: str = typer.Option(..., "--symbol"),
    side: str = typer.Option(..., "--side"),
    quantity: float = typer.Option(..., "--quantity"),
    price: float = typer.Option(..., "--price", help="Limit price"),
    stop_price: float = typer.Option(..., "--stop-price", help="Trigger price"),
    reduce_only: bool = typer.Option(False, "--reduce-only", help="Reduce-only order"),
):
    """Place a stop-limit order"""
    try:
        bot.place_stop_limit_order(symbol, side.upper(), quantity, price, stop_price, reduce_only=reduce_only)
    except typer.Exit:
        pass  # Already logged
    except BinanceAPIException as e:
        console.print(f"[red]Error:[/red] {e}")

@app.command("open-orders")
def list_open_orders(symbol: str = typer.Option(..., "--symbol")):
    """List open orders for a symbol"""
    try:
        orders = bot.get_open_orders(symbol)
        table = Table(title=f"Open Orders for {symbol}")
        table.add_column("Order ID")
        table.add_column("Side")
        table.add_column("Price")
        table.add_column("Qty")
        for order in orders:
            table.add_row(str(order["orderId"]), order["side"], order["price"], order["origQty"])
        console.print(table)
    except BinanceAPIException as e:
        console.print(f"[red]Error:[/red] {e}")

@app.command("cancel-order")
def cancel_order(
    symbol: str = typer.Option(..., "--symbol"),
    order_id: int = typer.Option(..., "--order-id"),
):
    """Cancel a specific order by ID"""
    try:
        bot.cancel_order(symbol, order_id)
    except BinanceAPIException as e:
        console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    app()
