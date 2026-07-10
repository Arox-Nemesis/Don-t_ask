
# Anime News Bot

A Telegram bot that automatically fetches anime news from a deployed AniNewsAPI instance and posts it to a Telegram channel.

## Features

- Automatic news posting
- MongoDB duplicate prevention
- APScheduler background tasks
- Fallback image support
- HTML formatted captions
- Docker support
- Hugging Face compatible
- Koyeb / Railway / Render compatible

---

## Environment Variables

Create a `.env` file.

```env
API_ID=
API_HASH=
BOT_TOKEN=

CHANNEL_ID=
OWNER_ID=

MONGO_URI=

NEWS_API_URL=

CHECK_INTERVAL=300

CHANNEL_BRAND=𝗔𝗻𝗶𝗳𝗹𝗶𝘅 𝗡𝗲𝘄𝘀 𝗡𝗲𝘁𝘄𝗼𝗿𝗸

FALLBACK_IMAGE=https://i.ibb.co/yLBQXvW/IMG-20260710-135314.png
```

---

## Install

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Docker

```bash
docker build -t anime-news-bot .
docker run --env-file .env anime-news-bot
```
