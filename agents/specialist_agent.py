import re
import requests
from agents.agent import Agent
import config


class SpecialistAgent(Agent):
    """Hybrid pricing: Ollama (primary) + Modal.com (fallback)"""

    name = "Specialist Agent"
    MODEL = config.OLLAMA_MODEL
    OLLAMA_URL = config.OLLAMA_URL
    MODAL_URL = config.MODAL_URL
    PRICE_PATTERN = r"[-+]?\d*\.\d+|\d+"
    USE_MODAL_FALLBACK = config.USE_MODAL_FALLBACK

    def _call_modal(self, description: str) -> float:
        """Call Modal.com fine-tuned model"""
        try:
            response = requests.post(
                self.MODAL_URL,
                json={"description": description},
                timeout=30
            )
            response.raise_for_status()
            return float(response.json().get("price", 100.0))
        except Exception as e:
            self.log(f"Modal error: {e}")
            return None

    def _call_ollama(self, prompt: str) -> str:
        """Make HTTP call to Ollama"""
        payload = {"model": self.MODEL, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            self.log(f"Ollama error: {e}")
            return None

    def _extract_number(self, text: str) -> float:
        """Extract first number from text"""
        if not text:
            return None
        text = text.replace("$", "").replace(",", "")
        match = re.search(self.PRICE_PATTERN, text)
        return float(match.group()) if match else None

    def _create_prompt(self, description: str) -> str:
        """Build pricing prompt"""
        return f"""Estimate the price of this product in USD. Respond with ONLY a number.

Product: {description}

Price estimate:"""

    def price(self, description: str) -> float:
        """Get price estimate with fallback strategy"""
        # Try Ollama first
        prompt = self._create_prompt(description)
        response = self._call_ollama(prompt)
        result = self._extract_number(response)
        
        # Fallback to Modal if Ollama fails and fallback enabled
        if result is None and self.USE_MODAL_FALLBACK:
            self.log("Ollama failed, trying Modal.com...")
            result = self._call_modal(description)
        
        # Final fallback to reasonable estimate
        if result is None:
            result = 100.0
            
        self.log(f"Specialist: ${result:.2f}")
        return result
