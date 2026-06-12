import logging

class Agent:
    """Base class for agents with simple logging"""
    
    name: str = "Agent"

    def log(self, message):
        """Log a message with the agent name"""
        logging.info(f"[{self.name}] {message}")
