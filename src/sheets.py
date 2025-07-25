"""
Google Sheets integration for the Money Tracker Bot
"""

import asyncio
import logging
from typing import Union, Dict, Any
import httpx
from datetime import datetime

from .models import Expense, Income, Transfer
from .config import SHEETS_API_URL

# Set up logging
logger = logging.getLogger(__name__)


class SheetsIntegration:
    """Handle Google Sheets API integration for financial data."""
    
    def __init__(self):
        self.api_url = SHEETS_API_URL
        self.timeout = 10.0  # 10 seconds timeout
    
    def _prepare_payload(self, transaction: Union[Expense, Income, Transfer]) -> Dict[str, Any]:
        """Prepare payload for Google Sheets API based on transaction type."""
        
        # Common fields
        base_payload = {
            'timestamp': datetime.now().isoformat(),
            'date': transaction.date,
            'amount': transaction.amount
        }
        
        if isinstance(transaction, Expense):
            return {
                **base_payload,
                'type': 'expense',
                'category': transaction.category,
                'account': transaction.account,
                'description': transaction.name
            }
        
        elif isinstance(transaction, Income):
            return {
                **base_payload,
                'type': 'income',
                'category': transaction.category,
                'account': transaction.account,
                'description': transaction.name
            }
        
        elif isinstance(transaction, Transfer):
            return {
                **base_payload,
                'type': 'transfer',
                'from_account': transaction.from_account,
                'to_account': transaction.to_account,
                'description': transaction.description
            }
        
        else:
            raise ValueError(f"Unknown transaction type: {type(transaction)}")
    
    async def send_to_sheets(self, transaction: Union[Expense, Income, Transfer]) -> bool:
        """Send transaction data to Google Sheets API."""
        try:
            payload = self._prepare_payload(transaction)
            
            logger.info(f"Sending to Google Sheets: {payload}")
            
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,  # Follow redirects for Google Apps Script
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'MoneyTrackerBot/1.0'
                }
            ) as client:
                response = await client.post(
                    self.api_url,
                    json=payload
                )
                
                response.raise_for_status()  # Raises exception for 4xx/5xx status codes
                
                # Check if the response contains success indicators
                response_text = response.text
                logger.info(f"Google Sheets response: {response_text}")
                
                # Consider it successful if we get a 200 response
                # You may need to adjust this based on your Google Apps Script response format
                logger.info(f"Successfully sent to Google Sheets. Status: {response.status_code}")
                return True
                
        except httpx.TimeoutException:
            logger.error("Timeout while sending data to Google Sheets")
            return False
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while sending to Google Sheets: {e.response.status_code} - {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while sending to Google Sheets: {str(e)}")
            return False
    
    def send_to_sheets_sync(self, transaction: Union[Expense, Income, Transfer]) -> bool:
        """Synchronous wrapper for sending to Google Sheets (for testing)."""
        try:
            return asyncio.run(self.send_to_sheets(transaction))
        except Exception as e:
            logger.error(f"Error in sync sheets operation: {str(e)}")
            return False


# Global instance
sheets_integration = SheetsIntegration()
