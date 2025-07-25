"""
Configuration settings for the Money Tracker Bot
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
SHEETS_API_URL = os.getenv('SHEETS_API')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables. Please check your .env file.")

if not SHEETS_API_URL:
    raise ValueError("SHEETS_API not found in environment variables. Please check your .env file.")

# Other configuration constants can be added here
DEFAULT_CURRENCY = "$"
DATE_FORMAT = "%Y-%m-%d"
