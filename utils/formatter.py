from html import escape

from config import CHANNEL_BRAND


class Formatter:

    @staticmethod
    def format_caption(article: dict) -> str:
        """
        Create Telegram caption.
        """

        title = escape(article["title"])

        description = escape(
            article["description"]
        )

        caption = (
            "📰 <b>Anime News</b>\n\n"

            f"<b>{title}</b>\n\n"

            f"{description}\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

            f"𝗦𝗼𝘂𝗿𝗰𝗲: {CHANNEL_BRAND}"
        )

        return caption


formatter = Formatter()
