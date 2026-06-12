from typing import Optional, List
from agents.agent import Agent
from agents.deals import Deal, Opportunity
from agents.scanner_agent import ScannerAgent
from agents.ensemble_agent import EnsembleAgent
from agents.messaging_agent import MessagingAgent
import config


class PlanningAgent(Agent):
    """Orchestrates workflow across scanner, pricing, and messaging agents"""
    
    name = "Planning Agent"
    DEAL_THRESHOLD = config.DEAL_THRESHOLD

    def __init__(self):
        self.scanner = ScannerAgent()
        self.ensemble = EnsembleAgent()
        self.messenger = MessagingAgent()

    def _calculate_opportunity(self, deal: Deal) -> Opportunity:
        """Calculate discount for a single deal"""
        estimate = self.ensemble.price(deal.product_description)
        discount = estimate - deal.price
        return Opportunity(deal=deal, estimate=estimate, discount=discount)

    def _get_best_opportunity(self, opportunities: List[Opportunity]) -> Opportunity:
        """Find opportunity with highest discount"""
        return max(opportunities, key=lambda opp: opp.discount)

    def _should_alert(self, discount: float) -> bool:
        """Check if discount meets threshold"""
        return discount > self.DEAL_THRESHOLD

    def plan(self, memory: List[str] = []) -> Optional[Opportunity]:
        """Execute main discovery workflow"""
        selection = self.scanner.scan(memory=memory)
        if not selection:
            return None
        
        opportunities = [self._calculate_opportunity(d) for d in selection.deals[:5]]
        best = self._get_best_opportunity(opportunities)
        
        self.log(f"Best deal: ${best.discount:.2f} discount")
        
        if self._should_alert(best.discount):
            self.messenger.alert(best)
            return best
        
        return None
