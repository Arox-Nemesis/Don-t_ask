from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_ID, API_HASH, BOT_TOKEN
from utils.logger import LOGGER


class AnimeNewsBot(Client):

    def __init__(self):

        super().__init__(
            name="AnimeNewsBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            workers=50
        )

    async def start(self):

        await super().start()

        me = await self.get_me()

        LOGGER.info("=" * 50)
        LOGGER.info(f"Bot Started Successfully")
        LOGGER.info(f"Bot Name : {me.first_name}")
        LOGGER.info(f"Username : @{me.username}")
        LOGGER.info("=" * 50)

    async def stop(self, *args):

        LOGGER.info("Stopping Bot...")

        await super().stop()

        LOGGER.info("Bot Stopped Successfully")


app = AnimeNewsBot()
