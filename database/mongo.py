from datetime import datetime
from hashlib import sha256

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from config import MONGO_URI
from utils.logger import LOGGER


class MongoDatabase:

    def __init__(self):
        self.client = None
        self.db = None

        self.posts = None
        self.settings = None
        self.stats = None

    async def connect(self):

        self.client = AsyncIOMotorClient(MONGO_URI)

        self.db = self.client["AnimeNewsBot"]

        self.posts = self.db["posted_articles"]
        self.settings = self.db["settings"]
        self.stats = self.db["statistics"]

        await self.posts.create_index(
            [("hash", ASCENDING)],
            unique=True
        )

        await self.posts.create_index(
            [("url", ASCENDING)],
            unique=True
        )

        LOGGER.info("✓ MongoDB Connected")

    @staticmethod
    def generate_hash(url: str):

        return sha256(url.encode()).hexdigest()

    async def article_exists(self, url: str):

        article_hash = self.generate_hash(url)

        article = await self.posts.find_one(
            {
                "hash": article_hash
            }
        )

        return article is not None

    async def save_article(self, article: dict):

        document = {
            "hash": self.generate_hash(article["url"]),
            "url": article["url"],
            "title": article["title"],
            "description": article["description"],
            "image": article["image"],
            "source": article["source"],
            "published": article["published"],
            "posted_at": datetime.utcnow()
        }

        await self.posts.insert_one(document)

        await self.increment_post_counter()

    async def increment_post_counter(self):

        await self.stats.update_one(
            {
                "_id": "statistics"
            },
            {
                "$inc": {
                    "total_posts": 1
                }
            },
            upsert=True
        )

    async def get_total_posts(self):

        stats = await self.stats.find_one(
            {
                "_id": "statistics"
            }
        )

        if not stats:
            return 0

        return stats.get("total_posts", 0)

    async def save_last_sync(self):

        await self.settings.update_one(
            {
                "_id": "sync"
            },
            {
                "$set": {
                    "last_sync": datetime.utcnow()
                }
            },
            upsert=True
        )

    async def get_last_sync(self):

        data = await self.settings.find_one(
            {
                "_id": "sync"
            }
        )

        if not data:
            return None

        return data.get("last_sync")

    async def get_database_stats(self):

        return {
            "articles": await self.posts.count_documents({}),
            "posts": await self.get_total_posts(),
            "last_sync": await self.get_last_sync()
        }

    async def close(self):

        if self.client:
            self.client.close()
            LOGGER.info("MongoDB Connection Closed")


mongo = MongoDatabase()
