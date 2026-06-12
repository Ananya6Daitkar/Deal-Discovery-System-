from agents.agent import Agent
from agents.specialist_agent import SpecialistAgent
import config


class EnsembleAgent(Agent):
    """Combines multiple pricing models with RAG-enhanced context"""
    
    name = "Ensemble Agent"
    USE_RAG = config.USE_RAG

    def __init__(self):
        self.specialist = SpecialistAgent()
        self.vector_store = None
        
        if self.USE_RAG:
            try:
                from agents.vector_store import VectorStore
                self.vector_store = VectorStore()
                self.log("RAG enabled with vector store")
            except Exception as e:
                self.log(f"RAG disabled: {e}")
                self.USE_RAG = False

    def _enhance_with_rag(self, description: str) -> str:
        """Enhance description with similar historical deals"""
        if not self.vector_store:
            return description
        
        similar = self.vector_store.similarity_search(description, k=2)
        if similar:
            context = "\n".join([
                f"Similar product: {s['text']} (${s['metadata'].get('price', 'N/A')})"
                for s in similar
            ])
            return f"{description}\n\nContext from similar deals:\n{context}"
        return description

    def price(self, description: str) -> float:
        """Get price estimate with optional RAG enhancement"""
        description = description.strip()
        
        # Enhance with RAG if enabled
        if self.USE_RAG and self.vector_store:
            enhanced_desc = self._enhance_with_rag(description)
        else:
            enhanced_desc = description
        
        specialist_price = self.specialist.price(enhanced_desc)
        
        # Store in vector store for future RAG
        if self.USE_RAG and self.vector_store:
            try:
                self.vector_store.add_document(
                    description,
                    {"price": specialist_price, "source": "specialist"}
                )
            except Exception as e:
                self.log(f"Failed to store in vector DB: {e}")
        
        self.log(f"Price: ${specialist_price:.2f} (Gemma 2B)")
        return specialist_price
