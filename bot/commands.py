from pyrogram import filters
from pyrogram.types import Message

from config import OWNER_ID
from database.mongo import mongo
from api.client import api
from utils.logger import LOGGER


def register_commands(app, scheduler):

    admin = filters.user(OWNER_ID)

    @app.on_message(filters.command("ping") & admin)
    async def ping(_, message: Message):

        status = await api.health_check()

        text = (
            "🏓 <b>Pong!</b>\n\n"
            f"API Status : {'🟢 Online' if status else '🔴 Offline'}\n"
            "MongoDB : 🟢 Connected"
        )

        await message.reply_text(text)

    @app.on_message(filters.command("stats") & admin)
    async def stats(_, message: Message):

        data = await mongo.get_database_stats()

        text = (
            "📊 <b>Bot Statistics</b>\n\n"
            f"📰 Total Posts : {data['posts']}\n"
            f"📂 Database Entries : {data['articles']}\n"
            f"🕒 Last Sync : {data['last_sync']}"
        )

        await message.reply_text(text)

    @app.on_message(filters.command("checknews") & admin)
    async def check_news(_, message: Message):

        progress = await message.reply_text(
            "🔍 Checking AniNewsAPI..."
        )

        try:

            await scheduler.check_news()

            await progress.edit_text(
                "✅ News check completed successfully."
            )

        except Exception as err:

            LOGGER.exception(err)

            await progress.edit_text(
                f"❌ Error\n\n<code>{err}</code>"
            )

    @app.on_message(filters.command("help") & admin)
    async def help_command(_, message: Message):

        text = (
            "<b>Anime News Bot</b>\n\n"

            "<b>Available Commands</b>\n\n"

            "/checknews - Fetch latest news\n"
            "/stats - Bot statistics\n"
            "/ping - API status\n"
            "/help - Show this message"
        )

        await message.reply_text(text)
       
