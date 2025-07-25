"""
Response formatting utilities for the Money Tracker Bot
"""

from typing import Union
from models import Expense, Income, Transfer
from config import DEFAULT_CURRENCY


def format_transaction_response(transaction: Union[Expense, Income, Transfer]) -> str:
    """Format the parsed transaction into a clean response."""
    if isinstance(transaction, Expense):
        return f"💸 **Expense Recorded**\n\n" \
               f"💰 Amount: {DEFAULT_CURRENCY}{transaction.amount:,.2f}\n" \
               f"📂 Category: {transaction.category}\n" \
               f"🏦 Account: {transaction.account}\n" \
               f"📝 Description: {transaction.name}\n" \
               f"📅 Date: {transaction.date}"
    
    elif isinstance(transaction, Income):
        return f"💵 **Income Recorded**\n\n" \
               f"💰 Amount: +{DEFAULT_CURRENCY}{transaction.amount:,.2f}\n" \
               f"📂 Category: {transaction.category}\n" \
               f"🏦 Account: {transaction.account}\n" \
               f"📝 Description: {transaction.name}\n" \
               f"📅 Date: {transaction.date}"
    
    elif isinstance(transaction, Transfer):
        response = f"🔄 **Transfer Recorded**\n\n" \
                  f"💰 Amount: {DEFAULT_CURRENCY}{transaction.amount:,.2f}\n" \
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
*Example:* `- 50.00 Transportation Cash Bus fare to work`

**💵 Income:**
`+ <amount> <category> <account> <description> [@YYYY-MM-DD]`
*Example:* `+ 1000.00 Salary BRI Monthly salary`

**🔄 Transfer:**
`t <amount> <from_account> > <to_account> [description] [@YYYY-MM-DD]`
*Example:* `t 200.00 Cash > BRI ATM deposit`

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
• `- 25.50 Shopping Cash Weekly groceries @2024-01-15`
• `+ 3000.00 Business Mandiri Web design project`
• `t 500.00 Gopay > BRI Emergency fund transfer`

**Available Categories:**
Transportation, Shopping, Entertainment, Healthcare, Education, Travel, Investment, Salary, Business, Other

**Available Accounts:**
Cash, BRI, Mandiri, Gopay, OVO, ShopeePay, PayPal

**Notes:**
- Date format: YYYY-MM-DD (optional, defaults to today)
- Amount: Use decimal format (e.g., 25.50)
- Category/account names cannot contain spaces (use single words)
- Use "Other" category for miscellaneous expenses
"""


def get_error_message() -> str:
    """Get the error message for invalid formats."""
    return """
❌ **Invalid format!** 

Please use one of these formats:

**Expense:** `- 50.00 Transportation Cash Bus fare`
**Income:** `+ 1000.00 Salary BRI Monthly pay`
**Transfer:** `t 200.00 Cash > BRI Deposit`

Send /help for more details and examples.
"""
