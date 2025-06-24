import logging
import os

def setup_logging() -> None:
    """Configure logging to file and console."""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )
