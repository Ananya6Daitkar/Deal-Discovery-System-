"""
Quick test of the scanner agent
"""
import sys
sys.path.insert(0, '/Users/nalinee/Documents/week8-multi-agent-system')

from agents.scanner_agent import ScannerAgent

print("Testing Scanner Agent...")
print("=" * 60)

scanner = ScannerAgent()

print("\n1. Fetching deals from RSS feeds...")
try:
    result = scanner.scan(memory=[])
    
    if result and result.deals:
        print(f"\nSuccess! Found {len(result.deals)} deals")
        for i, deal in enumerate(result.deals[:3], 1):
            print(f"\n{i}. ${deal.price:.2f} - {deal.product_description[:80]}...")
    else:
        print("\nNo deals found or filtered by GPT")
        
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
