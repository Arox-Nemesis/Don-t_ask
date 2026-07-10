from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import RPCError

from config import CHANNEL_ID, FALLBACK_IMAGE
from utils.logger import LOGGER
from utils.formatter import formatter
from database.mongo import mongo


class NewsPoster:

    def __init__(self, app: Client):
        self.app = app

    def build_keyboard(self, article: dict):
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🔗 Read More",
                        url=article["url"]
                    )
                ]
            ]
        )

    async def post_article(self, article: dict):

        if await mongo.article_exists(article["url"]):
            LOGGER.info(
                f"Skipped: {article['title']}"
            )
            return False

        caption = formatter.format_caption(article)

        keyboard = self.build_keyboard(article)

        photo = article.get("image") or FALLBACK_IMAGE

        try:

            await self.app.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo,
                caption=caption,
                reply_markup=keyboard,
            )

            LOGGER.info(
                f"Posted: {article['title']}"
            )

        except RPCError as err:

            LOGGER.warning(
                f"Photo failed ({err}). Using fallback."
            )

            try:

                await self.app.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=FALLBACK_IMAGE,
                    caption=caption,
                    reply_markup=keyboard,
                )

            except Exception:

                await self.app.send_message(
                    chat_id=CHANNEL_ID,
                    text=caption,
                    reply_markup=keyboard,
                    disable_web_page_preview=False,
                )

        except Exception as err:

            LOGGER.error(err)

            return False

        await mongo.save_article(article)

        return True


poster = None
