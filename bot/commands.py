from pyrogram import filters
from pyrogram.types import Message

from config import OWNER_ID
from database.mongo import mongo
from api.client import api


from bot.scheduler import scheduler

   @app.on_message(
      filters.command("checknews")
      & filters.user(OWNER_ID)
    )
    async def check_news_command(_, message: Message):

       await message.reply_text(
            "🔍 Checking for latest news..."
        )

        await scheduler.check_news()

        await message.reply_text(
            "✅ News check completed."
    )
    async def ping(_, message: Message):

        status = await api.health_check()

        await message.reply_text(
            f"🏓 <b>Pong!</b>\n\n"
            f"API : {'✅ Online' if status else '❌ Offline'}\n"
            f"MongoDB : ✅ Connected"
        )

    @app.on_message(
        filters.command("stats")
        & filters.user(OWNER_ID)
    )
    async def stats(_, message: Message):

        stats = await mongo.get_database_stats()

        await message.reply_text(
            "<b>📊 Bot Statistics</b>\n\n"
            f"Articles Posted : {stats['posts']}\n"
            f"Database Entries : {stats['articles']}\n"
            f"Last Sync : {stats['last_sync']}"
        )

    @app.on_message(
        filters.command("help")
        & filters.user(OWNER_ID)
    )
    async def help_command(_, message: Message):

        await message.reply_text(
            "<b>Anime News Bot</b>\n\n"
            "/checknews - Check for new articles\n"
            "/stats - View statistics\n"
            "/ping - Check bot status\n"
            "/help - Show this message"
        )
