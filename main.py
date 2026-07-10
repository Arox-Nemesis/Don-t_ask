import asyncio

from bot.client import app
from bot.commands import register_commands
from bot.scheduler import NewsScheduler
from database.mongo import mongo
from utils.logger import LOGGER


async def startup():

    LOGGER.info("Connecting to MongoDB...")

    await mongo.connect()

    LOGGER.info("Starting Telegram Bot...")

    await app.start()

    register_commands(app)

    scheduler = NewsScheduler(app)

    scheduler.start()

    # Run once immediately on startup
    await scheduler.check_news()

    LOGGER.info("Anime News Bot Started Successfully")

    await asyncio.Event().wait()


async def shutdown():

    LOGGER.info("Shutting Down...")

    await mongo.close()

    await app.stop()

    LOGGER.info("Bot Stopped")


async def main():

    try:

        await startup()

    except KeyboardInterrupt:

        pass

    finally:

        await shutdown()


if __name__ == "__main__":

    asyncio.run(main())
