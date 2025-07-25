#!/usr/bin/env python3
"""
Test script for Google Sheets integration
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Expense, Income, Transfer
from sheets import sheets_integration

async def test_sheets_integration():
    """Test the Google Sheets integration with sample data."""
    
    print("🧪 Testing Google Sheets Integration\n")
    
    # Test cases
    test_transactions = [
        Expense(
            amount=50.00,
            category="food",
            account="cash",
            name="Test lunch",
            date="2025-07-25"
        ),
        Income(
            amount=1000.00,
            category="salary",
            account="bank",
            name="Test salary",
            date="2025-07-25"
        ),
        Transfer(
            amount=200.00,
            from_account="cash",
            to_account="bank",
            description="Test transfer",
            date="2025-07-25"
        )
    ]
    
    for i, transaction in enumerate(test_transactions, 1):
        print(f"Test {i}: Sending {type(transaction).__name__} to Google Sheets")
        print(f"   Data: {transaction}")
        
        try:
            success = await sheets_integration.send_to_sheets(transaction)
            if success:
                print("   ✅ Successfully sent to Google Sheets")
            else:
                print("   ❌ Failed to send to Google Sheets")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 50)

def test_sheets_sync():
    """Synchronous test wrapper."""
    asyncio.run(test_sheets_integration())

if __name__ == "__main__":
    test_sheets_sync()
