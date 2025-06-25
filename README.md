# Binance Futures Trading Bot

A Python-based command-line trading bot for the Binance **Futures Testnet**. Designed for safe testing, this bot supports placing market, limit, and stop-limit orders, managing balances and open orders, and canceling orders via a clean CLI.

---

## 🚀 Features

* **Market / Limit / Stop-Limit Orders**
* **Account Balance Check** (USDT)
* **Open Order Management & Cancellation**
* **Symbol Precision Validation**
* **Secure Config via `.env`**
* **Detailed Logging to `logs/bot.log`**
* **Runs on Binance Futures Testnet**
* **Clean CLI Interface with Poetry**

---

## 📦 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/YogeshSoni2305/binance-bot.git
cd binance-bot
```

### 2. Install Poetry

Follow [Poetry installation guide](https://python-poetry.org/docs/#installation):

```bash
curl -sSL https://install.python-poetry.org | python3
# Or for Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 3. Install Dependencies

```bash
poetry install
```

### 4. Configure API Credentials

```bash
touch .env
```

Add your Binance Testnet credentials:

```env
API_KEY=your_key_here
API_SECRET=your_secret_here
```

> ✅ `.env` is ignored in `.gitignore`

---

## ⚙️ Usage

### Show All Commands

```bash
poetry run python -m src.binance_bot.cli --help
```

### Available Commands

```
Usage: python -m src.binance_bot.cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  balance       Check futures account balance
  cancel-order  Cancel an open order by ID
  limit         Place a limit order
  market        Place a market order
  open-orders   List open orders for a symbol
  stop-limit    Place a stop-limit order
```

---

## 🧪 Example Commands

### 1. Check Balance

```bash
poetry run python -m src.binance_bot.cli balance
```

### 2. Place Market Order

```bash
poetry run python -m src.binance_bot.cli market --symbol BTCUSDT --side BUY --quantity 0.001

```

### 3. Place Limit Order

```bash
poetry run python -m src.binance_bot.cli limit --symbol BTCUSDT --side BUY --quantity 0.002 --price 59000

```

### 4. Place Stop-Limit Order

```bash
poetry run python -m src.binance_bot.cli stop-limit \
  --symbol BTCUSDT \
  --side SELL \
  --quantity 0.001 \
  --price 59900 \
  --stop-price 60000 \
  --reduce-only

```

### 5. List Open Orders

```bash
poetry run python -m src.binance_bot.cli open-orders --symbol BTCUSDT
```

### 6. Cancel an Order

```bash
poetry run python -m src.binance_bot.cli cancel-order --symbol BTCUSDT --order-id <order_id>
```

### 7. Check Symbol Precision

```bash
poetry run python -c "from src.binance_bot.bot import TradingBot; bot = TradingBot(); info = bot.validate_symbol('BTCUSDT'); print(f\"Precision: {info.get('quantityPrecision')} | Min Qty: {next((f for f in info['filters'] if f['filterType']=='LOT_SIZE'), {}).get('minQty')}\")"


```

---

## 📂 Project Structure

```
/workspaces/binance-bot
├── .env                # API keys
├── README.md           # You're here
├── pyproject.toml      # Poetry config
├── poetry.lock         # Locked dependencies
├── logs
│   └── bot.log         # Operation logs
├── src
│   └── binance_bot
│       ├── cli.py      # CLI entry
│       ├── bot.py      # Binance logic
│       ├── config.py   # API config
│       ├── logger.py   # Logging setup
├── tests
│   └── __init__.py     # Test suite
```

---

## 🛠 Troubleshooting

### ❌ API Errors

* Ensure your API keys are correct.
* Confirm they have **Futures Trading** permissions.
* Check IP restrictions if you're using whitelisted IPs.

### ❌ Command Not Found

* Check `cli.py` is under `src/binance_bot/`
* Run `poetry install` again

### ❌ Invalid Symbol

* Use `BTCUSDT`, `ETHUSDT`, etc.
* Check precision & min quantity using the symbol precision command above.

### 📝 View Logs

```bash
cat logs/bot.log
```

---

##  Contributing

1. Fork the repo
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Submit a PR

---



---

##  Acknowledgments

* [Binance Futures Testnet](https://testnet.binancefuture.com)
* [python-binance](https://github.com/sammchardy/python-binance)
* [Poetry](https://python-poetry.org)
