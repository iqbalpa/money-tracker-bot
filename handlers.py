"""
Bot command handlers for the Money Tracker Bot
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from parser import FinanceParser
from formatters import (
    format_transaction_response,
    get_welcome_message,
    get_help_message,
    get_error_message
)

# Set up logging
logger = logging.getLogger(__name__)

# Initialize parser
finance_parser = FinanceParser()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = get_welcome_message()
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    help_message = get_help_message()
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
            error_message = get_error_message()
            await update.message.reply_text(error_message, parse_mode='Markdown')
            
    except ValueError as e:
        error_msg = f"❌ Error parsing amount: {str(e)}\nPlease use valid decimal format (e.g., 25.50)"
        await update.message.reply_text(error_msg)
        logger.error(f"Value error: {e}")
    except Exception as e:
        error_msg = "❌ An error occurred while processing your message. Please try again."
        await update.message.reply_text(error_msg)
        logger.error(f"Unexpected error: {e}")
