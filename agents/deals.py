from pydantic import BaseModel, Field
from typing import List, Self
from bs4 import BeautifulSoup
import re
import feedparser
import requests
import time

# RSS feeds to scrape (multiple sources for reliability)
FEEDS = [
    # Primary feeds
    "https://www.dealnews.com/c142/Electronics/?rss=1",
    "https://www.dealnews.com/c39/Computers/?rss=1",
    "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
    # Backup feeds
    "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
    "https://www.techbargains.com/rss/deals",
]

# Demo data for when RSS feeds are unavailable
DEMO_DEALS = [
    {
        "title": "Apple AirPods Pro 2 with USB-C - $199",
        "summary": "Apple AirPods Pro 2nd Generation with USB-C charging case. Features active noise cancellation, transparency mode, and adaptive audio.",
        "url": "https://example.com/deal/airpods-pro-2",
    },
    {
        "title": "Sony WH-1000XM5 Wireless Headphones - $329",
        "summary": "Premium noise-cancelling wireless headphones with 30-hour battery life and superior sound quality.",
        "url": "https://example.com/deal/sony-wh1000xm5",
    },
    {
        "title": "Samsung Galaxy Watch 6 - $249",
        "summary": "Latest smartwatch with health tracking, GPS, and sleep monitoring. Compatible with Android devices.",
        "url": "https://example.com/deal/galaxy-watch-6",
    },
    {
        "title": "Logitech MX Master 3S Mouse - $79",
        "summary": "Ergonomic wireless mouse with precision tracking and customizable buttons for productivity.",
        "url": "https://example.com/deal/mx-master-3s",
    },
    {
        "title": "iPad Air 5th Gen 64GB - $499",
        "summary": "Apple iPad Air with M1 chip, 10.9-inch Liquid Retina display, and support for Apple Pencil 2.",
        "url": "https://example.com/deal/ipad-air-5",
    },
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
        """Scrape deals from all RSS feeds with fallback to demo data"""
        deals = []
        successful_feeds = 0
        
        for feed_url in FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                if feed.entries:
                    successful_feeds += 1
                    for entry in feed.entries[:10]:
                        deals.append(cls(entry))
                        time.sleep(0.05)
            except Exception as e:
                print(f"Failed to fetch {feed_url}: {e}")
                continue
        
        # Fallback to demo data if no feeds worked
        if not deals:
            print("All RSS feeds failed. Using demo data...")
            for demo in DEMO_DEALS:
                # Create a mock entry that matches RSS feed structure
                mock_entry = {
                    "title": demo["title"],
                    "summary": demo["summary"],
                    "links": [{"href": demo["url"]}]
                }
                deals.append(cls(mock_entry))
        
        print(f"Fetched {len(deals)} deals from {successful_feeds} feeds")
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
