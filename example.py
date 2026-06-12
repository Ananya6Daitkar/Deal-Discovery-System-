"""
Simple example showing how to use the deal discovery system
"""

from deal_agent_framework import DealAgentFramework


def main():
    print("Multi-Agent Deal Discovery System\n")
    
    framework = DealAgentFramework()
    opportunities = framework.run()
    
    print(f"\n Found {len(opportunities)} opportunities")
    
    if opportunities:
        print("\n Recent Opportunities:")
        for i, opp in enumerate(opportunities[-3:], 1):  # Show last 3
            print(f"\n{i}. ${opp.discount:.2f} discount")
            print(f"   {opp.deal.product_description[:80]}...")
            print(f"   ${opp.deal.price:.2f} (Est: ${opp.estimate:.2f})")


if __name__ == "__main__":
    main()
