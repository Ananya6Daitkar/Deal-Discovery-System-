from agents.agent import Agent
from agents.specialist_agent import SpecialistAgent


class EnsembleAgent(Agent):
    """Combines multiple pricing models with weighted average"""
    
    name = "Ensemble Agent"
    
    # Using only specialist for now (Gemma 2B)
    # Frontier agent removed due to ChromaDB Python 3.14 incompatibility

    def __init__(self):
        self.specialist = SpecialistAgent()

    def price(self, description: str) -> float:
        """Get price estimate from specialist model"""
        description = description.strip()
        
        specialist_price = self.specialist.price(description)
        
        self.log(f"Price: ${specialist_price:.2f} (Gemma 2B)")
        return specialist_price
