from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.client import api
from bot.poster import NewsPoster
from database.mongo import mongo
from config import CHECK_INTERVAL
from utils.logger import LOGGER


class NewsScheduler:

    def __init__(self, app):

        self.poster = NewsPoster(app)

        self.scheduler = AsyncIOScheduler()

    async def check_news(self):

        LOGGER.info("=" * 60)
        LOGGER.info("Checking AniNewsAPI...")

        try:

            articles = await api.fetch_news()

            if not articles:

                LOGGER.info("No articles received.")

                return

            # Oldest first
            articles.sort(
                key=lambda article: article["published"]
            )

            fetched = len(articles)
            skipped = 0
            posted = 0

            for article in articles:

                exists = await mongo.article_exists(
                    article["url"]
                )

                if exists:

                    skipped += 1

                    continue

                success = await self.poster.send(
                    article
                )

                if success:

                    await mongo.save_article(
                        article
                    )

                    posted += 1

            await mongo.save_last_sync()

            LOGGER.info("=" * 60)
            LOGGER.info(
                f"Fetched : {fetched}"
            )
            LOGGER.info(
                f"Posted  : {posted}"
            )
            LOGGER.info(
                f"Skipped : {skipped}"
            )
            LOGGER.info("=" * 60)

        except Exception as err:

            LOGGER.exception(err)

    def start(self):

        self.scheduler.add_job(
            self.check_news,
            trigger="interval",
            seconds=CHECK_INTERVAL,
            id="anime_news",
            max_instances=1,
            coalesce=True,
            replace_existing=True,
        )

        self.scheduler.start()

        LOGGER.info(
            f"Scheduler Started "
            f"({CHECK_INTERVAL} seconds)"
        )

    async def stop(self):

        self.scheduler.shutdown(
            wait=False
        )

        LOGGER.info(
            "Scheduler Stopped"
        )
