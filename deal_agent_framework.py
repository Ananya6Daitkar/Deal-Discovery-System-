import os
import sys
import logging
import json
from typing import List
from dotenv import load_dotenv
from agents.planning_agent import PlanningAgent
from agents.deals import Opportunity

load_dotenv(override=True)


def init_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


class DealAgentFramework:
    """Main framework that coordinates the multi-agent system with Ollama"""
    
    MEMORY_FILE = "memory.json"

    def __init__(self):
        init_logging()
        logging.info("Using Ollama with Gemma 2B")
        self.memory = self._load_memory()
        self.planner = None

    def _load_memory(self) -> List[Opportunity]:
        """Load previously seen opportunities from file"""
        if os.path.exists(self.MEMORY_FILE):
            with open(self.MEMORY_FILE, "r") as f:
                data = json.load(f)
            return [Opportunity(**item) for item in data]
        return []

    def _save_memory(self) -> None:
        """Save opportunities to file"""
        with open(self.MEMORY_FILE, "w") as f:
            data = [opp.model_dump() for opp in self.memory]
            json.dump(data, f, indent=2)

    def run(self) -> List[Opportunity]:
        """Execute the deal discovery workflow"""
        # Initialize agents lazily
        if not self.planner:
            self.planner = PlanningAgent()
        
        logging.info("Starting deal discovery")
        result = self.planner.plan(memory=self.memory)
        
        if result:
            self.memory.append(result)
            self._save_memory()
            
        logging.info(f"Complete: {len(self.memory)} total opportunities")
        return self.memory


if __name__ == "__main__":
    DealAgentFramework().run()
