from agents.agent import Agent
from agents.deals import Opportunity


class MessagingAgent(Agent):
    """Sends notifications about deals"""

    name = "Messaging Agent"

    def alert(self, opportunity: Opportunity):
        """Print alert for a great deal"""
        print(f"""
🔔 Great Deal Found!

Product: {opportunity.deal.product_description[:100]}...
Price: ${opportunity.deal.price:.2f}
Estimated Value: ${opportunity.estimate:.2f}
Discount: ${opportunity.discount:.2f}

URL: {opportunity.deal.url}
""")
        self.log(f"Alert sent: ${opportunity.discount:.2f} discount")
