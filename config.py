import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUPPORT_GROUP_ID = os.getenv("SUPPORT_GROUP_ID")
OWNER_ID = os.getenv("OWNER_ID")
