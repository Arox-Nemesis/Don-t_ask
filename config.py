from dotenv import load_dotenv
import os

load_dotenv()

# Telegram

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

OWNER_ID = int(os.getenv("OWNER_ID"))

# MongoDB

MONGO_URI = os.getenv("MONGO_URI")

# AniNewsAPI

NEWS_API_URL = os.getenv("NEWS_API_URL")

CHECK_INTERVAL = int(
    os.getenv("CHECK_INTERVAL", 300)
)

# Branding

CHANNEL_BRAND = os.getenv(
    "CHANNEL_BRAND",
    "𝗔𝗻𝗶𝗳𝗹𝗶𝘅 𝗡𝗲𝘄𝘀 𝗡𝗲𝘁𝘄𝗼𝗿𝗸"
)

FALLBACK_IMAGE = os.getenv(
    "FALLBACK_IMAGE",
    "https://i.ibb.co/yLBQXvW/IMG-20260710-135314.png"
)
