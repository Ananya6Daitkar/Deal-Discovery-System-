import re
import requests
from agents.agent import Agent


class SpecialistAgent(Agent):
    """Local Ollama model for pricing"""

    name = "Specialist Agent"
    MODEL = "gemma:2b"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    PRICE_PATTERN = r"[-+]?\d*\.\d+|\d+"

    def _call_ollama(self, prompt: str) -> str:
        """Make HTTP call to Ollama"""
        payload = {"model": self.MODEL, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            self.log(f"Error: {e}")
            return "100"

    def _extract_number(self, text: str) -> float:
        """Extract first number from text"""
        text = text.replace("$", "").replace(",", "")
        match = re.search(self.PRICE_PATTERN, text)
        return float(match.group()) if match else 100.0

    def _create_prompt(self, description: str) -> str:
        """Build pricing prompt"""
        return f"""Estimate the price of this product in USD. Respond with ONLY a number.

Product: {description}

Price estimate:"""

    def price(self, description: str) -> float:
        """Get price estimate from Ollama"""
        prompt = self._create_prompt(description)
        response = self._call_ollama(prompt)
        result = self._extract_number(response)
        self.log(f"Specialist: ${result:.2f}")
        return result
