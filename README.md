# Money Tracker Bot

A Telegram bot for tracking personal finances with support for expenses, income, and transfers.

## Features

- **Expenses**: Track money spent with categorization
- **Income**: Record money earned from various sources  
- **Transfers**: Log money moved between accounts
- **Date Support**: Optional date specification or auto-default to today
- **Error Handling**: Clear error messages for invalid formats

## Supported Message Formats

### 💸 Expense
```
- <amount> <category> <account> <description> [@YYYY-MM-DD]
```
**Example:** `- 50.00 food cash Lunch at restaurant`

### 💵 Income  
```
+ <amount> <category> <account> <description> [@YYYY-MM-DD]
```
**Example:** `+ 1000.00 salary bank Monthly salary`

### 🔄 Transfer
```
t <amount> <from_account> > <to_account> [description] [@YYYY-MM-DD]
```
**Example:** `t 200.00 cash > bank ATM deposit`

## Project Structure

```
money-tracker-bot/
├── main.py              # Main application entry point
├── config.py            # Configuration and environment setup
├── models.py            # Data models (Expense, Income, Transfer)
├── parser.py            # Message parsing logic
├── formatters.py        # Response formatting utilities
├── handlers.py          # Telegram bot command handlers
├── test_parser.py       # Test script for parser functionality
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (BOT_TOKEN)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd money-tracker-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Create a `.env` file in the project root
   - Add your Telegram bot token:
     ```
     BOT_TOKEN=your_bot_token_here
     ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## Testing

Run the test script to verify parser functionality:
```bash
python test_parser.py
```

## Bot Commands

- `/start` - Welcome message and usage instructions
- `/help` - Detailed help with examples and format specifications

## Architecture

### Modular Design

The bot is designed with separation of concerns:

- **`config.py`**: Centralized configuration management
- **`models.py`**: Data structures for different transaction types
- **`parser.py`**: Core parsing logic with regex patterns
- **`formatters.py`**: Response formatting and message templates
- **`handlers.py`**: Telegram bot event handlers
- **`main.py`**: Application entry point and bot setup

### Error Handling

- **Input Validation**: Regex patterns ensure proper format
- **Amount Parsing**: Validates decimal numbers
- **Date Validation**: Ensures YYYY-MM-DD format when specified
- **Graceful Failures**: Clear error messages for invalid inputs

## Development

### Adding New Transaction Types

1. Add new data model in `models.py`
2. Create parsing method in `parser.py`
3. Add formatting logic in `formatters.py`
4. Update `parse_message()` method to handle new type
5. Add test cases in `test_parser.py`

### Customization

- **Currency Symbol**: Modify `DEFAULT_CURRENCY` in `config.py`
- **Date Format**: Adjust `DATE_FORMAT` in `config.py`
- **Response Messages**: Update templates in `formatters.py`
