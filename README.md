@YogeshSoni2305 ➜ /workspaces/binance-bot (main) $ poetry run python -m src.binance_bot.cli --help
Usage: python -m src.binance_bot.cli [OPTIONS] COMMAND [ARGS]...

  Binance Futures Trading Bot CLI.

Options:
  --help  Show this message and exit.

Commands:
  balance       Check futures account balance.
  cancel_order  Cancel an open order by ID.
  limit         Place a limit order.
  market        Place a market order.
  open_orders   List open orders for a symbol.
  stop_limit    Place a stop-limit order.





  poetry run python -m src.binance_bot.cli balance

  Futures Testnet URL: https://testnet.binancefuture.com.
Relevant endpoints:
/fapi/v1/exchangeInfo for symbol info (handled by get_exchange_info()).
/fapi/v2/balance for account balance (handled by futures_account_balance()).
/fapi/v1/order for placing orders (handled by futures_create_order()).
/fapi/v1/openOrders for open orders (handled by get_open_orders()).





















# Binance Futures Trading Bot

A Python-based command-line interface (CLI) trading bot for interacting with the Binance Futures Testnet. This bot allows users to place market, limit, and stop-limit orders, check account balances, manage open orders, and cancel orders on the Binance Futures Testnet.

## Features

- **Market Orders**: Place buy or sell market orders for specified trading pairs (e.g., BTCUSDT).
- **Limit Orders**: Place buy or sell limit orders with custom price and quantity.
- **Stop-Limit Orders**: Place stop-limit orders with stop price and limit price for risk management.
- **Balance Checking**: Retrieve USDT balance and available balance from the Futures account.
- **Open Orders Management**: List all open orders for a specific trading pair.
- **Order Cancellation**: Cancel open orders by order ID.
- **Symbol Validation**: Validate trading pairs and retrieve precision details (e.g., quantity precision, minimum quantity).
- **Logging**: Detailed logging of all operations to `logs/bot.log` for debugging and monitoring.
- **Testnet Support**: Operates on Binance Futures Testnet (`https://testnet.binancefuture.com`) for safe testing.
- **Configuration Management**: Securely load API keys from a `.env` file.
- **Poetry Dependency Management**: Uses Poetry for reproducible Python environments.

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Poetry**: Dependency manager for Python projects.
- **Binance Futures Testnet Account**: Obtain API key and secret from [https://testnet.binancefuture.com](https://testnet.binancefuture.com).
- **Git**: For cloning the repository.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/binance-bot.git
cd binance-bot

2. Install Poetry
If Poetry is not installed, follow these steps:

Linux/macOS:
curl -sSL https://install.python-poetry.org | python3 -


Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -



Add Poetry to your PATH if needed (see Poetry documentation).
Verify installation:
poetry --version

3. Install Dependencies
Install project dependencies using Poetry:
poetry install

This creates a virtual environment and installs dependencies listed in pyproject.toml, including python-binance>=1.0.19.
4. Configure Environment
Create a .env file in the project root with your Binance Futures Testnet API credentials:
touch .env

Edit .env with your API key and secret:
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here

Ensure the .env file is not committed to version control (it’s included in .gitignore).
Starting the Bot
Activate the Poetry virtual environment:
poetry shell

Alternatively, prefix commands with poetry run without activating the shell:
poetry run python -m src.binance_bot.cli --help

Available CLI Commands
Run the following to see all available commands:
poetry run python -m src.binance_bot.cli --help

Output:
Usage: python -m src.binance_bot.cli [OPTIONS] COMMAND [ARGS]...

  Binance Futures Trading Bot CLI.

Options:
  --help  Show this message and exit.

Commands:
  balance       Check futures account balance.
  cancel_order  Cancel an open order by ID.
  limit         Place a limit order.
  market        Place a market order.
  open_orders   List open orders for a symbol.
  stop_limit    Place a stop-limit order.

Workflow

Initialization:

The bot loads API credentials from .env using config.py.
It initializes the Binance client with testnet=True and sets the Futures API URL (https://testnet.binancefuture.com/fapi).
Logging is configured via logger.py to write to logs/bot.log.


Symbol Validation:

Before placing orders or fetching open orders, the bot validates the trading pair (e.g., BTCUSDT) using get_exchange_info().
Ensures the symbol exists and retrieves precision details (e.g., quantityPrecision, minQty).


Order Placement:

Market Orders: Executed instantly at the current market price.
Limit Orders: Placed at a specified price, waiting for a match.
Stop-Limit Orders: Triggered when the market hits the stop price, then placed as a limit order at the specified price.
Orders are sent via futures_create_order with parameters like symbol, side, quantity, price, stopPrice, and positionSide='BOTH'.


Balance and Order Management:

Fetch account balance using futures_account_balance.
List open orders with get_open_orders.
Cancel orders using cancel_order by order ID.


Error Handling:

The bot catches BinanceAPIException and logs errors.
CLI commands display user-friendly error messages.


Logging:

All operations (initialization, validation, order placement, errors) are logged to logs/bot.log for debugging.



Test Commands
Test the bot’s functionality using the following commands in the project root (/workspaces/binance-bot).
1. Check CLI Help
poetry run python -m src.binance_bot.cli --help

Expected Output:
Usage: python -m src.binance_bot.cli [OPTIONS] COMMAND [ARGS]...

  Binance Futures Trading Bot CLI.

Options:
  --help  Show this message and exit.

Commands:
  balance       Check futures account balance.
  cancel_order  Cancel an open order by ID.
  limit         Place a limit order.
  market        Place a market order.
  open_orders   List open orders for a symbol.
  stop_limit    Place a stop-limit order.

2. Check Account Balance
poetry run python -m src.binance_bot.cli balance

Expected Output (sample):
USDT Balance: 15004.90647239 (Available: 15002.25672572)

3. Place a Market Order
poetry run python -m src.binance_bot.cli market --symbol BTCUSDT --side BUY --quantity 0.001

Expected Output (sample):
Order Placed:
- Type: MARKET
- Symbol: BTCUSDT
- Side: BUY
- Quantity: 0.001
- Status: FILLED
- Order ID: <order_id>

4. Place a Limit Order
poetry run python -m src.binance_bot.cli limit --symbol BTCUSDT --side BUY --quantity 0.001 --price 59000

Expected Output (sample):
Order Placed:
- Type: LIMIT
- Symbol: BTCUSDT
- Side: BUY
- Quantity: 0.001
- Status: NEW
- Order ID: <order_id>

5. Place a Stop-Limit Order
poetry run python -m src.binance_bot.cli stop_limit --symbol BTCUSDT --side SELL --quantity 0.001 --stop-price 60000 --limit-price 59900

Expected Output (sample):
Order Placed:
- Type: STOP
- Symbol: BTCUSDT
- Side: SELL
- Quantity: 0.001
- Status: NEW
- Order ID: <order_id>

6. List Open Orders
poetry run python -m src.binance_bot.cli open_orders --symbol BTCUSDT

Expected Output (sample):
Open Order:
- Symbol: BTCUSDT
- Type: STOP
- Side: SELL
- Quantity: 0.001
- Price: 59900
- Stop Price: 60000
- Order ID: <order_id>

If no orders exist:
No open orders for BTCUSDT

7. Cancel an Order
Replace <order_id> with the actual order ID from open_orders:
poetry run python -m src.binance_bot.cli cancel_order --symbol BTCUSDT --order-id <order_id>

Expected Output (sample):
Order <order_id> canceled for BTCUSDT

8. Check Symbol Precision
poetry run python -c "from src.binance_bot.bot import TradingBot; from src.binance_bot.config import load_config; config = load_config(); bot = TradingBot(config['api_key'], config['api_secret'], testnet=True); info = bot.validate_symbol('BTCUSDT'); print(f'Quantity Precision: {info.get(\"quantityPrecision\", \"N/A\")}'); print(f'Min Quantity: {next((f for f in info.get(\"filters\", []) if f.get(\"filterType\") == \"LOT_SIZE\"), {}).get(\"minQty\", \"N/A\")}')"

Expected Output (sample):
Quantity Precision: 3
Min Quantity: 0.001

9. View Logs
Check the log file for debugging:
cat logs/bot.log

Sample Log:
2025-06-24 06:37:17,545 - src.binance_bot.bot - INFO - Binance client initialized for testnet=True
2025-06-24 06:37:17,970 - src.binance_bot.bot - DEBUG - Validated symbol: BTCUSDT
2025-06-24 06:37:17,972 - src.binance_bot.bot - DEBUG - Placing stop-limit order: symbol=BTCUSDT, side=SELL, quantity=0.001, stopPrice=60000.0, limitPrice=59900.0

Troubleshooting

API Errors:

Ensure API keys are valid and have Futures Trading permissions at https://testnet.binancefuture.com.
Check IP restrictions (use curl ifconfig.me to get your IP).


Command Not Found:

Verify cli.py is in src/binance_bot/ and uses setup_logging.
Run poetry install to ensure dependencies are installed.


Invalid Symbol or Parameters:

Check symbol precision using the symbol precision command.
Ensure quantity and price align with minQty and quantityPrecision.


Logs:

Check logs/bot.log for detailed error messages.


Library Version:
poetry show python-binance

Expected: version: 1.0.19 or later. Update if needed:
poetry add python-binance@latest
poetry install


Project Structure:
tree

Expected:
/workspaces/binance-bot
├── .env
├── README.md
├── pyproject.toml
├── poetry.lock
├── logs
│   └── bot.log
├── src
│   └── binance_bot
│       ├── __init__.py
│       ├── bot.py
│       ├── cli.py
│       ├── config.py
│       └── logger.py
└── tests
    └── __init__.py



Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Binance Futures Testnet for providing a safe testing environment.
python-binance for the API client.
Poetry for dependency management.


