import asyncio
import signal

from bot.client import app
from bot.scheduler import NewsScheduler
from bot.commands import register_commands

from database.mongo import mongo
from utils.logger import LOGGER


async def startup():

    LOGGER.info("=" * 60)
    LOGGER.info("Starting Anime News Bot...")
    LOGGER.info("=" * 60)

    # Connect MongoDB
    await mongo.connect()

    # Start Telegram Bot
    await app.start()

    # Create Scheduler
    scheduler = NewsScheduler(app)

    # Register Commands
    register_commands(app, scheduler)

    # Start Scheduler
    scheduler.start()

    # Run one check immediately
    LOGGER.info("Running Initial News Check...")
    await scheduler.check_news()

    LOGGER.info("=" * 60)
    LOGGER.info("Anime News Bot Started Successfully")
    LOGGER.info("=" * 60)

    return scheduler


async def shutdown(scheduler):

    LOGGER.info("=" * 60)
    LOGGER.info("Stopping Anime News Bot...")
    LOGGER.info("=" * 60)

    try:
        await scheduler.stop()
    except Exception:
        pass

    try:
        await mongo.close()
    except Exception:
        pass

    try:
        await app.stop()
    except Exception:
        pass

    LOGGER.info("Shutdown Complete")


async def main():

    scheduler = await startup()

    stop_event = asyncio.Event()

    def stop_signal(*args):
        stop_event.set()

    loop = asyncio.get_running_loop()

    for sig in (
        signal.SIGINT,
        signal.SIGTERM,
    ):
        try:
            loop.add_signal_handler(
                sig,
                stop_signal
            )
        except NotImplementedError:
            pass

    await stop_event.wait()

    await shutdown(scheduler)


if __name__ == "__main__":
    asyncio.run(main())
