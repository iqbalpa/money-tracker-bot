import logging
import os
import re
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Union
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables. Please check your .env file.")

# Data classes for different transaction types
@dataclass
class Expense:
    amount: float
    category: str
    account: str
    name: str
    date: str
    
@dataclass
class Income:
    amount: float
    category: str
    account: str
    name: str
    date: str
    
@dataclass
class Transfer:
    amount: float
    from_account: str
    to_account: str
    description: str
    date: str

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

# Initialize parser
finance_parser = FinanceParser()

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
🤖 **Welcome to Money Tracker Bot!**

I can help you track your personal finances. Here are the supported formats:

**💸 Expense:**
`- <amount> <category> <account> <description> [@YYYY-MM-DD]`
*Example:* `- 50.00 food cash Lunch at restaurant`

**💵 Income:**
`+ <amount> <category> <account> <description> [@YYYY-MM-DD]`
*Example:* `+ 1000.00 salary bank Monthly salary`

**🔄 Transfer:**
`t <amount> <from_account> > <to_account> [@YYYY-MM-DD]`
*Example:* `t 200.00 cash > bank ATM deposit`

**📅 Date is optional** - if not specified, today's date will be used.

Just send me a message in any of these formats and I'll log it for you!
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    help_message = """
📖 **Money Tracker Bot Help**

**Supported Formats:**

1️⃣ **Expense** (spending money):
   `- <amount> <category> <account> <description> [@date]`
   
2️⃣ **Income** (earning money):
   `+ <amount> <category> <account> <description> [@date]`
   
3️⃣ **Transfer** (moving money):
   `t <amount> <from_account> > <to_account> [@date]`

**Examples:**
• `- 25.50 groceries cash Weekly shopping @2024-01-15`
• `+ 3000.00 freelance paypal Web design project`
• `t 500.00 savings > checking Emergency fund`

**Notes:**
- Date format: YYYY-MM-DD (optional, defaults to today)
- Amount: Use decimal format (e.g., 25.50)
- No spaces in category/account names (use underscores if needed)
"""
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and parse finance data."""
    message_text = update.message.text
    logger.info(f"Received message: {message_text}")
    
    try:
        # Parse the message
        transaction = finance_parser.parse_message(message_text)
        
        if transaction:
            # Format and send success response
            response = format_transaction_response(transaction)
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Log the transaction
            logger.info(f"Parsed transaction: {transaction}")
        else:
            # Send error message with examples
            error_message = """
❌ **Invalid format!** 

Please use one of these formats:

**Expense:** `- 50.00 food cash Lunch`
**Income:** `+ 1000.00 salary bank Monthly pay`
**Transfer:** `t 200.00 cash > bank Deposit`

Send /help for more details and examples.
"""
            await update.message.reply_text(error_message, parse_mode='Markdown')
            
    except ValueError as e:
        error_msg = f"❌ Error parsing amount: {str(e)}\nPlease use valid decimal format (e.g., 25.50)"
        await update.message.reply_text(error_msg)
        logger.error(f"Value error: {e}")
    except Exception as e:
        error_msg = "❌ An error occurred while processing your message. Please try again."
        await update.message.reply_text(error_msg)
        logger.error(f"Unexpected error: {e}")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting Money Tracker Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()