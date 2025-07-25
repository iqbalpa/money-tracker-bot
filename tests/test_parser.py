#!/usr/bin/env python3
"""
Test script for the Money Tracker Bot parser
"""

import sys
import os
# Add parent directory and src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.parser import FinanceParser
from src.formatters import format_transaction_response

def test_parser():
    """Test the finance parser with sample inputs."""
    
    print("🧪 Testing Money Tracker Bot Parser\n")
    
    # Initialize parser
    finance_parser = FinanceParser()
    
    # Test cases
    test_cases = [
        # Expenses
        "- 50.00 food cash Lunch at restaurant",
        "- 25.50 groceries card Weekly shopping @2024-01-15",
        "- 120.00 gas cash Gas station fill-up",
        
        # Income
        "+ 1000.00 salary bank Monthly salary",
        "+ 500.00 freelance paypal Web design project @2024-01-20",
        "+ 50.00 gift cash Birthday money",
        
        # Transfers
        "t 200.00 cash > bank ATM deposit",
        "t 1000.00 checking > savings Monthly savings @2024-01-10",
        "t 50.00 paypal > bank Transfer to bank",
        
        # Invalid cases
        "invalid message",
        "- invalid amount food cash Test",
        "+ 100 missing info",
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: '{test_case}'")
        
        try:
            result = finance_parser.parse_message(test_case)
            if result:
                print("✅ Parsed successfully:")
                print(f"   {result}")
                print("\n📱 Bot Response:")
                response = format_transaction_response(result)
                print(f"   {response.replace('**', '').replace('*', '')}")
            else:
                print("❌ Failed to parse")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_parser()
