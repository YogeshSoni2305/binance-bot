import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        "API_KEY": os.getenv("BINANCE_API_KEY", ""),
        "API_SECRET": os.getenv("BINANCE_API_SECRET", ""),
        "BASE_URL": os.getenv("BASE_URL", "https://testnet.binancefuture.com/fapi")
    }

