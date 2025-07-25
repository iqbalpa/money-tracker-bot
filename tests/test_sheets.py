#!/usr/bin/env python3
"""
Test script for Google Sheets integration
"""

import sys
import os
import asyncio
# Add parent directory and src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models import Expense, Income, Transfer
from src.sheets import sheets_integration

async def test_sheets_integration():
    """Test the Google Sheets integration with sample data."""
    
    print("🧪 Testing Google Sheets Integration\n")
    
    # Test cases with Indonesian accounts and proper dropdown categories
    test_transactions = [
        Expense(
            amount=50.00,
            category="Food & Dining",
            account="Cash",
            name="Test lunch expense",
            date="2025-07-25"
        ),
        Income(
            amount=1000.00,
            category="Salary",
            account="BRI",
            name="Test monthly salary",
            date="2025-07-25"
        ),
        Transfer(
            amount=200.00,
            from_account="Gopay",
            to_account="Mandiri",
            description="Test transfer from e-wallet to bank",
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
