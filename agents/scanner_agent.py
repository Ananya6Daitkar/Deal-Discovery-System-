from typing import Optional, List
import re
from agents.deals import ScrapedDeal, DealSelection, Deal
from agents.agent import Agent


class ScannerAgent(Agent):
    """Scans RSS feeds and extracts deals"""
    
    name = "Scanner Agent"
    PRICE_PATTERN = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'

    def _get_new_deals(self, memory) -> List[ScrapedDeal]:
        """Fetch deals not in memory"""
        existing_urls = {opp.deal.url for opp in memory}
        all_deals = ScrapedDeal.fetch()
        new_deals = [d for d in all_deals if d.url not in existing_urls]
        self.log(f"Found {len(new_deals)} new deals")
        return new_deals

    def _extract_price(self, text: str) -> float:
        """Extract price from text using regex"""
        match = re.search(self.PRICE_PATTERN, text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 100.0

    def _create_deal(self, scraped: ScrapedDeal) -> Deal:
        """Convert ScrapedDeal to Deal"""
        text = f"{scraped.title} {scraped.details}"
        price = self._extract_price(text)
        description = scraped.details if scraped.details else scraped.title
        return Deal(product_description=description, price=price, url=scraped.url)

    def scan(self, memory: List[str] = []) -> Optional[DealSelection]:
        """Scan feeds and return filtered deals"""
        deals = self._get_new_deals(memory)
        if not deals:
            self.log("No new deals")
            return None
        
        self.log(f"Processing {len(deals)} deals")
        result_deals = [self._create_deal(d) for d in deals[:5]]
        
        if result_deals:
            self.log(f"Selected {len(result_deals)} deals")
            return DealSelection(deals=result_deals)
        
        return None
