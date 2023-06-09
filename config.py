import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")

TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
