#!/usr/bin/env python3
"""
Display the modular structure and dependencies of the Money Tracker Bot
"""

def show_structure():
    structure = """
🏗️  Money Tracker Bot - Modular Architecture

📁 Project Structure:
├── src/                 # 💼 Source Code
│   ├── main.py         # 🎯 Entry point - Application bootstrap
│   ├── config.py       # ⚙️  Configuration - Environment & settings
│   ├── models.py       # 📊 Data Models - Expense, Income, Transfer
│   ├── parser.py       # 🔍 Parser Logic - Message parsing & validation  
│   ├── formatters.py   # 🎨 Formatters - Response formatting & templates
│   ├── handlers.py     # 🎮 Bot Handlers - Command & message handling
│   └── sheets.py       # 📊 Google Sheets - API integration for data storage
├── tests/              # 🧪 Test Suite
│   ├── test_parser.py  # 🧪 Tests - Parser functionality validation
│   ├── test_sheets.py  # 🧪 Tests - Google Sheets integration testing
│   └── test_version.py # 🧪 Tests - Version checking
├── docs/               # 📚 Documentation
│   ├── README.md       # 📖 Main documentation
│   ├── GOOGLE_APPS_SCRIPT_SETUP.md  # 📋 Setup guide
│   └── data-format-reference.html   # 📊 Data format reference
├── scripts/            # 🛠️  Utility Scripts
│   ├── google-apps-script.js        # 📜 Google Apps Script code
│   └── show_structure.py           # 📋 This script
├── run.py              # 🚀 Main entry point
├── requirements.txt    # 📦 Dependencies
├── .env               # 🔐 Environment Variables (BOT_TOKEN, SHEETS_API)
├── .gitignore         # 🚫 Git ignore rules
└── README.md -> docs/README.md  # 📖 Documentation link

🔗 Module Dependencies:

src/main.py
├── src/config.py (BOT_TOKEN)
└── src/handlers.py (start_command, help_command, handle_message)

src/handlers.py  
├── src/parser.py (FinanceParser)
├── src/formatters.py (format_transaction_response, get_*_message)
└── src/sheets.py (sheets_integration)

src/sheets.py
└── src/models.py (Expense, Income, Transfer)

src/parser.py
└── src/models.py (Expense, Income, Transfer)

src/formatters.py
└── src/models.py (Expense, Income, Transfer)

tests/test_parser.py
├── src/parser.py (FinanceParser) 
└── src/formatters.py (format_transaction_response)

tests/test_sheets.py
├── src/models.py (Expense, Income, Transfer)
└── src/sheets.py (sheets_integration)

🎯 Benefits of Modular Design:
✅ Separation of Concerns - Each module has a single responsibility
✅ Maintainability - Easy to modify individual components
✅ Testability - Components can be tested in isolation
✅ Reusability - Modules can be reused in other projects
✅ Readability - Clean, organized codebase
✅ Scalability - Easy to add new features without affecting existing code
✅ Google Sheets Integration - Automatic data persistence with error handling
✅ Async Support - Non-blocking HTTP requests for better performance
"""
    print(structure)

if __name__ == "__main__":
    show_structure()
