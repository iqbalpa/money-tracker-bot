"""
Parser for finance messages in the Money Tracker Bot
"""

import re
from datetime import datetime
from typing import Optional, Union

from models import Expense, Income, Transfer


class FinanceParser:
    """Parser for finance messages."""
    
    def __init__(self):
        # Regex patterns for different transaction types
        self.expense_pattern = r'^-\s*(\d+(?:\.\d{2})?)\s+(\S+)\s+(\S+)\s+(.+?)(?:\s+@(\d{4}-\d{2}-\d{2}))?$'
        self.income_pattern = r'^\+\s*(\d+(?:\.\d{2})?)\s+(\S+)\s+(\S+)\s+(.+?)(?:\s+@(\d{4}-\d{2}-\d{2}))?$'
        self.transfer_pattern = r'^t\s*(\d+(?:\.\d{2})?)\s+(\S+)\s*>\s*(\S+)(?:\s+(.+?))?(?:\s+@(\d{4}-\d{2}-\d{2}))?$'
    
    def get_today_date(self) -> str:
        """Get today's date in YYYY-MM-DD format."""
        return datetime.now().strftime('%Y-%m-%d')
    
    def parse_expense(self, text: str) -> Optional[Expense]:
        """Parse expense message format: - <amount> <category> <account> <name> [@YYYY-MM-DD]"""
        match = re.match(self.expense_pattern, text.strip())
        if match:
            amount, category, account, name, date = match.groups()
            return Expense(
                amount=float(amount),
                category=category,
                account=account,
                name=name.strip(),
                date=date if date else self.get_today_date()
            )
        return None
    
    def parse_income(self, text: str) -> Optional[Income]:
        """Parse income message format: + <amount> <category> <account> <name> [@YYYY-MM-DD]"""
        match = re.match(self.income_pattern, text.strip())
        if match:
            amount, category, account, name, date = match.groups()
            return Income(
                amount=float(amount),
                category=category,
                account=account,
                name=name.strip(),
                date=date if date else self.get_today_date()
            )
        return None
    
    def parse_transfer(self, text: str) -> Optional[Transfer]:
        """Parse transfer message format: t <amount> <from_account> > <to_account> [description] [@YYYY-MM-DD]"""
        match = re.match(self.transfer_pattern, text.strip())
        if match:
            amount, from_account, to_account, description, date = match.groups()
            return Transfer(
                amount=float(amount),
                from_account=from_account,
                to_account=to_account,
                description=description.strip() if description else "",
                date=date if date else self.get_today_date()
            )
        return None
    
    def parse_message(self, text: str) -> Optional[Union[Expense, Income, Transfer]]:
        """Parse any supported message format."""
        # Try to parse as expense
        if text.strip().startswith('-'):
            return self.parse_expense(text)
        
        # Try to parse as income
        elif text.strip().startswith('+'):
            return self.parse_income(text)
        
        # Try to parse as transfer
        elif text.strip().startswith('t '):
            return self.parse_transfer(text)
        
        return None
