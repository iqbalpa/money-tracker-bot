"""
Response formatting utilities for the Money Tracker Bot
"""

from typing import Union
from models import Expense, Income, Transfer


def format_transaction_response(transaction: Union[Expense, Income, Transfer]) -> str:
    """Format the parsed transaction into a clean response."""
    if isinstance(transaction, Expense):
        return f"💸 **Expense Recorded**\n\n" \
               f"💰 Amount: ${transaction.amount:.2f}\n" \
               f"📂 Category: {transaction.category}\n" \
               f"🏦 Account: {transaction.account}\n" \
               f"📝 Description: {transaction.name}\n" \
               f"📅 Date: {transaction.date}"
    
    elif isinstance(transaction, Income):
        return f"💵 **Income Recorded**\n\n" \
               f"💰 Amount: +${transaction.amount:.2f}\n" \
               f"📂 Category: {transaction.category}\n" \
               f"🏦 Account: {transaction.account}\n" \
               f"📝 Description: {transaction.name}\n" \
               f"📅 Date: {transaction.date}"
    
    elif isinstance(transaction, Transfer):
        response = f"🔄 **Transfer Recorded**\n\n" \
                  f"💰 Amount: ${transaction.amount:.2f}\n" \
                  f"📤 From: {transaction.from_account}\n" \
                  f"📥 To: {transaction.to_account}\n" \
                  f"📅 Date: {transaction.date}"
        
        if transaction.description:
            response += f"\n📝 Description: {transaction.description}"
        
        return response
    
    return "❌ Unknown transaction type"


def get_welcome_message() -> str:
    """Get the welcome message for the /start command."""
    return """
🤖 **Welcome to Money Tracker Bot!**

I can help you track your personal finances. Here are the supported formats:

**💸 Expense:**
`- <amount> <category> <account> <description> [@YYYY-MM-DD]`
*Example:* `- 50.00 food cash Lunch at restaurant`

**💵 Income:**
`+ <amount> <category> <account> <description> [@YYYY-MM-DD]`
*Example:* `+ 1000.00 salary bank Monthly salary`

**🔄 Transfer:**
`t <amount> <from_account> > <to_account> [description] [@YYYY-MM-DD]`
*Example:* `t 200.00 cash > bank ATM deposit`

**📅 Date is optional** - if not specified, today's date will be used.

Just send me a message in any of these formats and I'll log it for you!
"""


def get_help_message() -> str:
    """Get the help message for the /help command."""
    return """
📖 **Money Tracker Bot Help**

**Supported Formats:**

1️⃣ **Expense** (spending money):
   `- <amount> <category> <account> <description> [@date]`
   
2️⃣ **Income** (earning money):
   `+ <amount> <category> <account> <description> [@date]`
   
3️⃣ **Transfer** (moving money):
   `t <amount> <from_account> > <to_account> [description] [@date]`

**Examples:**
• `- 25.50 groceries cash Weekly shopping @2024-01-15`
• `+ 3000.00 freelance paypal Web design project`
• `t 500.00 savings > checking Emergency fund`

**Notes:**
- Date format: YYYY-MM-DD (optional, defaults to today)
- Amount: Use decimal format (e.g., 25.50)
- No spaces in category/account names (use underscores if needed)
"""


def get_error_message() -> str:
    """Get the error message for invalid formats."""
    return """
❌ **Invalid format!** 

Please use one of these formats:

**Expense:** `- 50.00 food cash Lunch`
**Income:** `+ 1000.00 salary bank Monthly pay`
**Transfer:** `t 200.00 cash > bank Deposit`

Send /help for more details and examples.
"""
