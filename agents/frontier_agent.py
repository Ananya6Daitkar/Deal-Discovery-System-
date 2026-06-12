import re
import requests
from sentence_transformers import SentenceTransformer
from agents.agent import Agent


class FrontierAgent(Agent):
    """RAG-based pricing using similar products from vector database with Ollama"""
    
    name = "Frontier Agent"
    MODEL = "llama3.2"
    OLLAMA_URL = "http://localhost:11434/api/generate"

    def __init__(self, collection):
        self.collection = collection
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def _find_similar_products(self, description: str):
        """Find similar products using vector search"""
        vector = self.encoder.encode([description])
        results = self.collection.query(
            query_embeddings=vector.astype(float).tolist(), 
            n_results=5
        )
        documents = results["documents"][0]
        prices = [m["price"] for m in results["metadatas"][0]]
        return documents, prices

    def _extract_price(self, text: str) -> float:
        """Extract price from Ollama response"""
        text = text.replace("$", "").replace(",", "")
        match = re.search(r"[-+]?\d*\.\d+|\d+", text)
        return float(match.group()) if match else 0.0

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        payload = {
            "model": self.MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            self.log(f"Ollama error: {e}")
            return "100"

    def price(self, description: str) -> float:
        """Estimate price using RAG with similar products"""
        # Find similar products
        similar_products, similar_prices = self._find_similar_products(description)
        
        # Build context
        context = "Similar products for reference:\n\n"
        for product, price in zip(similar_products, similar_prices):
            context += f"- {product}\n  Price: ${price:.2f}\n\n"
        
        # Call Ollama
        prompt = f"""Based on similar products, estimate the price of this product. 
Respond with ONLY a number (no dollar sign, no explanation).

Product to estimate:
{description}

{context}

Estimated price:"""
        
        response = self._call_ollama(prompt)
        result = self._extract_price(response)
        self.log(f"Frontier: ${result:.2f}")
        return result
