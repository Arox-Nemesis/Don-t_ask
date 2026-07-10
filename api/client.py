import asyncio
from datetime import datetime
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup

from config import NEWS_API_URL, FALLBACK_IMAGE
from utils.logger import LOGGER


class AniNewsAPI:

    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def fetch_news(self) -> List[Dict]:
        """
        Fetch latest news from AniNewsAPI.
        """

        try:
            async with aiohttp.ClientSession(
                timeout=self.timeout
            ) as session:

                async with session.get(
                    NEWS_API_URL
                ) as response:

                    response.raise_for_status()

                    data = await response.json()

                    return self.normalize(data)

        except Exception as e:

            LOGGER.error(f"API Error: {e}")

            return []

    def normalize(self, data) -> List[Dict]:

        articles = []

        if isinstance(data, dict):
            data = data.get("data", [])

        for article in data:

            title = article.get("title", "").strip()

            description = self.clean_description(
                article.get("description", "")
            )

            image = (
                article.get("image")
                or FALLBACK_IMAGE
            )

            url = (
                article.get("url")
                or article.get("link")
            )

            source = article.get(
                "source",
                "Unknown"
            )

            published = self.parse_date(
                article.get("published")
                or article.get("publishedAt")
            )

            articles.append(
                {
                    "title": title,
                    "description": description,
                    "image": image,
                    "url": url,
                    "source": source,
                    "published": published,
                }
            )

        articles.sort(
            key=lambda x: x["published"],
            reverse=True,
        )

        return articles

    @staticmethod
    def clean_description(text: str) -> str:

        if not text:
            return ""

        text = BeautifulSoup(
            text,
            "html.parser"
        ).get_text(" ")

        text = " ".join(text.split())

        if len(text) > 300:
            text = text[:297] + "..."

        return text

    @staticmethod
    def parse_date(date_string):

        if not date_string:
            return datetime.utcnow()

        formats = (
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
        )

        for fmt in formats:
            try:
                return datetime.strptime(
                    date_string,
                    fmt
                )
            except Exception:
                pass

        return datetime.utcnow()

    async def health_check(self):

        news = await self.fetch_news()

        return len(news) > 0


api = AniNewsAPI()
