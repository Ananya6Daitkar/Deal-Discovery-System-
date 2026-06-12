from pydantic import BaseModel, Field
from typing import List, Self
from bs4 import BeautifulSoup
import re
import feedparser
import requests
import time

# RSS feeds to scrape
FEEDS = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
    "https://www.dealnews.com/c39/Computers/?rss=1",
    "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
]


def _extract_text(html: str) -> str:
    """Extract clean text from HTML snippet"""
    soup = BeautifulSoup(html, "html.parser")
    snippet = soup.find("div", class_="snippet summary")
    text = snippet.get_text(strip=True) if snippet else html
    return re.sub(r"<[^<]+?>", "", text).replace("\n", " ").strip()


class ScrapedDeal:
    """Deal retrieved from RSS feed"""

    def __init__(self, entry: dict):
        self.title = entry["title"][:100]
        self.summary = _extract_text(entry["summary"])
        self.url = entry["links"][0]["href"]
        
        # Use summary only (skip slow web scraping)
        self.details = self.summary[:500]
        self.features = ""

    def describe(self) -> str:
        """Format for LLM consumption"""
        return f"Title: {self.title}\nSummary: {self.details.strip()}\nURL: {self.url}"

    @classmethod
    def fetch(cls) -> List[Self]:
        """Scrape deals from all RSS feeds"""
        deals = []
        for feed_url in FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                deals.append(cls(entry))
                time.sleep(0.05)
        return deals


class Deal(BaseModel):
    """Structured deal with product description and price"""
    
    product_description: str = Field(
        description="3-4 sentence product summary focusing on features, not deal terms"
    )
    price: float = Field(description="Actual price of the product")
    url: str = Field(description="Deal URL")


class DealSelection(BaseModel):
    """Collection of selected deals"""
    
    deals: List[Deal] = Field(
        description="5 deals with most detailed descriptions and clear prices"
    )


class Opportunity(BaseModel):
    """Deal opportunity with pricing analysis"""
    
    deal: Deal
    estimate: float
    discount: float
