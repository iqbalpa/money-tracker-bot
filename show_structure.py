#!/usr/bin/env python3
"""
Display the modular structure and dependencies of the Money Tracker Bot
"""

def show_structure():
    structure = """
🏗️  Money Tracker Bot - Modular Architecture

📁 Project Structure:
├── main.py              # 🎯 Entry point - Application bootstrap
├── config.py            # ⚙️  Configuration - Environment & settings
├── models.py            # 📊 Data Models - Expense, Income, Transfer
├── parser.py            # 🔍 Parser Logic - Message parsing & validation  
├── formatters.py        # 🎨 Formatters - Response formatting & templates
├── handlers.py          # 🎮 Bot Handlers - Command & message handling
├── test_parser.py       # 🧪 Tests - Parser functionality validation
├── requirements.txt     # 📦 Dependencies
├── .env                 # 🔐 Environment Variables (BOT_TOKEN)
├── .gitignore          # 🚫 Git ignore rules
└── README.md           # 📖 Documentation

🔗 Module Dependencies:

main.py
├── config.py (BOT_TOKEN)
└── handlers.py (start_command, help_command, handle_message)

handlers.py  
├── parser.py (FinanceParser)
└── formatters.py (format_transaction_response, get_*_message)

parser.py
└── models.py (Expense, Income, Transfer)

formatters.py
└── models.py (Expense, Income, Transfer)

test_parser.py
├── parser.py (FinanceParser) 
└── formatters.py (format_transaction_response)

🎯 Benefits of Modular Design:
✅ Separation of Concerns - Each module has a single responsibility
✅ Maintainability - Easy to modify individual components
✅ Testability - Components can be tested in isolation
✅ Reusability - Modules can be reused in other projects
✅ Readability - Clean, organized codebase
✅ Scalability - Easy to add new features without affecting existing code
"""
    print(structure)

if __name__ == "__main__":
    show_structure()
