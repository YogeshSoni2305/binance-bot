from dotenv import load_dotenv
from typing import Dict
import os

def load_config() -> Dict[str, str]:
    """Load configuration from .env file."""
    load_dotenv()
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')

    if not api_key or not api_secret:
        raise ValueError("API_KEY and API_SECRET must be set in .env file")

    return {
        'api_key': api_key,
        'api_secret': api_secret
    }
