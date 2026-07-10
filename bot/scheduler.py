from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.client import api
from database.mongo import mongo
from bot.poster import NewsPoster
from utils.logger import LOGGER
from config import CHECK_INTERVAL


class NewsScheduler:

    def __init__(self, app):
        self.app = app
        self.poster = NewsPoster(app)
        self.scheduler = AsyncIOScheduler()

    async def check_news(self):
        """
        Fetch latest news and post only new articles.
        """

        LOGGER.info("Checking AniNewsAPI...")

        try:

            articles = await api.fetch_news()

            if not articles:
                LOGGER.info("No articles received.")
                return

            posted = 0

            for article in articles:

                if await mongo.article_exists(article["url"]):
                    continue

                success = await self.poster.post_article(article)

                if success:
                    posted += 1

            await mongo.save_last_sync()

            LOGGER.info(
                f"News Check Complete | "
                f"Fetched: {len(articles)} | "
                f"Posted: {posted}"
            )

        except Exception as err:

            LOGGER.exception(err)

    def start(self):

        self.scheduler.add_job(
            self.check_news,
            "interval",
            seconds=CHECK_INTERVAL,
            max_instances=1,
            coalesce=True,
        )

        self.scheduler.start()

        LOGGER.info(
            f"Scheduler Started "
            f"({CHECK_INTERVAL}s)"
        )


scheduler = NewsScheduler
