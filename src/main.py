"""
Money Tracker Bot - Main application entry point

A Telegram bot for tracking personal finances with support for:
- Expenses: - <amount> <category> <account> <description> [@date]
- Income: + <amount> <category> <account> <description> [@date]  
- Transfers: t <amount> <from_account> > <to_account> [description] [@date]
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers import start_command, help_command, handle_message, accounts_command, categories_command

# Set up logging
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Money Tracker Bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("accounts", accounts_command))
    application.add_handler(CommandHandler("categories", categories_command))
    
    # Add message handler for text messages (excluding commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting Money Tracker Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
