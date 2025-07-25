# Money Tracker Bot

A Telegram bot for tracking personal finances with Google Sheets integration.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   - Copy `.env.example` to `.env` (if available)
   - Add your `BOT_TOKEN` and `SHEETS_API` URL

3. **Run the bot**
   ```bash
   python run.py
   ```

## Documentation

For complete documentation, setup instructions, and usage examples, see:
- **[📖 Full Documentation](docs/README.md)**
- **[🔧 Google Apps Script Setup](docs/GOOGLE_APPS_SCRIPT_SETUP.md)**

## Project Structure

```
├── src/           # Source code
├── tests/         # Test files  
├── docs/          # Documentation
├── scripts/       # Utility scripts
└── run.py         # Entry point
```

## Testing

```bash
python tests/test_parser.py    # Test message parsing
python tests/test_sheets.py    # Test Google Sheets integration
```
