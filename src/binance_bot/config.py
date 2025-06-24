import os

def load_config():
    return {
        "api_key": os.getenv("BINANCE_API_KEY"),
        "api_secret": os.getenv("BINANCE_API_SECRET")
    }
