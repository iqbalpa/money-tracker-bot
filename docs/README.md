# Money Tracker Bot

A Telegram bot for tracking personal finances with support for expenses, income, and transfers, with automatic Google Sheets integration.

## Features

- **Expenses**: Track money spent with categorization
- **Income**: Record money earned from various sources  
- **Transfers**: Log money moved between accounts
- **Date Support**: Optional date specification or auto-default to today
- **Google Sheets Integration**: Automatically saves all transactions to Google Sheets
- **Error Handling**: Clear error messages for invalid formats
- **Real-time Confirmation**: Instant feedback when data is saved to spreadsheet

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
├── src/                 # Source code
│   ├── main.py         # Main application entry point
│   ├── config.py       # Configuration and environment setup
│   ├── models.py       # Data models (Expense, Income, Transfer)
│   ├── parser.py       # Message parsing logic
│   ├── formatters.py   # Response formatting utilities
│   ├── handlers.py     # Telegram bot command handlers
│   └── sheets.py       # Google Sheets API integration
├── tests/              # Test files
│   ├── test_parser.py  # Test script for parser functionality
│   ├── test_sheets.py  # Test script for Google Sheets integration
│   └── test_version.py # Test script for version checking
├── docs/               # Documentation
│   ├── README.md       # This file
│   ├── GOOGLE_APPS_SCRIPT_SETUP.md  # Setup guide for Google Apps Script
│   └── data-format-reference.html   # Data format reference
├── scripts/            # Utility scripts
│   ├── google-apps-script.js        # Google Apps Script code
│   └── show_structure.py           # Project structure display script
├── run.py              # Entry point to run the bot
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (BOT_TOKEN, SHEETS_API)
└── .gitignore         # Git ignore rules
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
   - Add your Telegram bot token and Google Sheets API URL:
     ```
     BOT_TOKEN=your_bot_token_here
     SHEETS_API=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
     ```

5. **Run the bot**
   ```bash
   python run.py
   ```

## Google Sheets Integration

The bot automatically sends all transaction data to Google Sheets via Google Apps Script.

### Data Format Sent to Sheets

Each transaction sends the following data:
- `timestamp`: ISO format timestamp when the transaction was processed
- `date`: Transaction date (YYYY-MM-DD)
- `amount`: Transaction amount
- `type`: "expense", "income", or "transfer"

**For Expenses and Income:**
- `category`: Transaction category
- `account`: Account used
- `description`: Transaction description

**For Transfers:**
- `from_account`: Source account
- `to_account`: Destination account  
- `description`: Transfer description (optional)

### Setting up Google Sheets

1. Create a Google Apps Script that accepts POST requests
2. Deploy as a web app with execute permissions for "Anyone"
3. Add the deployment URL to your `.env` file as `SHEETS_API`

## Usage

1. **Run the bot**
   ```bash
   python run.py
   ```

2. **Start a conversation** with your bot on Telegram using `/start`

3. **Send transactions** using the supported formats shown above

## Testing

Run the test scripts to verify functionality:
```bash
# Test parser functionality
python tests/test_parser.py

# Test Google Sheets integration
python tests/test_sheets.py

# Test Google Apps Script version
python tests/test_version.py
```

## Bot Commands

- `/start` - Welcome message and usage instructions
- `/help` - Detailed help with examples and format specifications
- `/accounts` - Show list of available accounts (Cash, BRI, Mandiri, Gopay, OVO, ShopeePay, PayPal)
- `/categories` - Show list of available categories (Transportation, Shopping, Entertainment, Healthcare, Education, Travel, Investment, Salary, Business, Other)

## Architecture

### Modular Design

The bot is designed with separation of concerns:

- **`src/config.py`**: Centralized configuration management
- **`src/models.py`**: Data structures for different transaction types
- **`src/parser.py`**: Core parsing logic with regex patterns
- **`src/formatters.py`**: Response formatting and message templates
- **`src/handlers.py`**: Telegram bot event handlers
- **`src/main.py`**: Application entry point and bot setup

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
