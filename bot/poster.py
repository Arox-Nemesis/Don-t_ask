from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNEL_ID, FALLBACK_IMAGE
from utils.formatter import formatter
from utils.logger import LOGGER


class NewsPoster:

    def __init__(self, app: Client):
        self.app = app

    @staticmethod
    def keyboard(article: dict):

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 Read More",
                        url=article["url"]
                    )
                ]
            ]
        )

    async def send(self, article: dict) -> bool:

        caption = formatter.format_caption(article)

        keyboard = self.keyboard(article)

        photo = article.get("image") or FALLBACK_IMAGE

        # First try article image
        try:

            await self.app.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )

            LOGGER.info(
                f"Posted: {article['title']}"
            )

            return True

        except RPCError as err:

            LOGGER.warning(
                f"Article image failed: {err}"
            )

        # Fallback image
        try:

            await self.app.send_photo(
                chat_id=CHANNEL_ID,
                photo=FALLBACK_IMAGE,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )

            LOGGER.info(
                f"Posted using fallback image: {article['title']}"
            )

            return True

        except RPCError as err:

            LOGGER.warning(
                f"Fallback image failed: {err}"
            )

        # Text-only fallback
        try:

            await self.app.send_message(
                chat_id=CHANNEL_ID,
                text=caption,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
                reply_markup=keyboard
            )

            LOGGER.info(
                f"Posted text message: {article['title']}"
            )

            return True

        except Exception as err:

            LOGGER.exception(err)

            return False
