#!/usr/bin/env python3
"""
Test to check which version of Google Apps Script is deployed
"""

import sys
import os
import asyncio
import httpx
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SHEETS_API_URL
import json

async def test_script_version():
    """Test which version of the script is deployed"""
    
    print("🔍 Testing Google Apps Script Version\n")
    
    # Test with each transaction type to see which sheets get created
    test_cases = [
        {
            "timestamp": f"2025-07-25T08:10:{str(int(time.time()) % 60).zfill(2)}",
            "date": "2025-07-25",
            "amount": 1.01,
            "type": "expense",
            "category": "version_test",
            "account": "test",
            "description": "VERSION_TEST_EXPENSE"
        },
        {
            "timestamp": f"2025-07-25T08:10:{str(int(time.time()) % 60).zfill(2)}",
            "date": "2025-07-25",
            "amount": 2.02,
            "type": "income",
            "category": "version_test",
            "account": "test",
            "description": "VERSION_TEST_INCOME"
        },
        {
            "timestamp": f"2025-07-25T08:10:{str(int(time.time()) % 60).zfill(2)}",
            "date": "2025-07-25",
            "amount": 3.03,
            "type": "transfer",
            "from_account": "test1",
            "to_account": "test2",
            "description": "VERSION_TEST_TRANSFER"
        }
    ]
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        for i, test_data in enumerate(test_cases, 1):
            print(f"Test {i}: Sending {test_data['type']} transaction...")
            
            try:
                response = await client.post(
                    SHEETS_API_URL,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200 and response.text == "Success":
                    print(f"   ✅ {test_data['type']} sent successfully")
                else:
                    print(f"   ❌ {test_data['type']} failed: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error sending {test_data['type']}: {e}")
        
        print("\n" + "="*60)
        print("🔍 CHECK YOUR GOOGLE SHEETS NOW:")
        print("If you see NEW separate sheets (Expenses, Income, Transfers):")
        print("   ✅ Updated script is deployed correctly")
        print("\nIf all data goes to 'Money Tracker' sheet:")
        print("   ❌ Old script is still deployed - need to redeploy")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(test_script_version())
