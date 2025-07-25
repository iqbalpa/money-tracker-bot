# Google Apps Script Setup Guide

This guide will help you set up the Google Apps Script to receive data from your Money Tracker Bot.

## 📋 Prerequisites

- Google account
- Access to Google Sheets and Google Apps Script

## 🚀 Setup Instructions

### Step 1: Create New Google Apps Script

1. Go to [script.google.com](https://script.google.com)
2. Click **"New project"**
3. Delete the default `myFunction()` code
4. Copy the entire contents of `google-apps-script.js` and paste it into the editor
5. Rename the project to "Money Tracker Bot API"

### Step 2: Test the Script

1. In the Apps Script editor, select the `testScript` function from the dropdown
2. Click the **Run** button (▶️)
3. Grant necessary permissions when prompted
4. Check the execution log to ensure it runs without errors
5. A new Google Sheet called "Money Tracker Data" should be created with test data

### Step 3: Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Choose **Web app** as the type
3. Configure the deployment:
   - **Description**: "Money Tracker Bot API v1"
   - **Execute as**: "Me"
   - **Who has access**: "Anyone"
4. Click **Deploy**
5. **Copy the Web app URL** - you'll need this for your bot

### Step 4: Update Your Bot Configuration

1. Open your `.env` file in the bot project
2. Add or update the `SHEETS_API` line with your web app URL:
   ```
   SHEETS_API=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
   ```

### Step 5: Test the Integration

1. Run the bot's test script:
   ```bash
   python tests/test_sheets.py
   ```
2. Check your Google Sheet to verify data is being saved correctly

## 📊 Spreadsheet Structure

The script creates a sheet with the following columns:

| Column | Field | Description |
|--------|-------|-------------|
| A | Timestamp | ISO timestamp when transaction was processed |
| B | Date | Transaction date (YYYY-MM-DD) |
| C | Type | "expense", "income", or "transfer" |
| D | Amount | Transaction amount |
| E | Category | Category (for expenses/income only) |
| F | Account | Account (for expenses/income only) |
| G | Description | Transaction description |
| H | From Account | Source account (for transfers only) |
| I | To Account | Destination account (for transfers only) |

## 🔧 Customization Options

### Using Existing Spreadsheet

If you want to use an existing spreadsheet:

1. Get your spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
2. In the script, uncomment and modify this line:
   ```javascript
   spreadsheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID_HERE');
   ```

### Changing Sheet Name

To use a different sheet name, modify this line:
```javascript
const SHEET_NAME = 'Your Custom Name';
```

### Adding Data Validation

You can add data validation, formulas, or formatting by modifying the `getOrCreateSheet()` function.

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure the script is deployed with "Execute as: Me"
   - Re-deploy if you change permissions

2. **404 Not Found**
   - Verify the web app URL is correct
   - Check that the deployment is active

3. **Data Not Appearing**
   - Check the Apps Script execution log for errors
   - Verify the JSON format matches what the script expects

### Testing the Web App

You can test the web app directly by visiting the URL in a browser. You should see:
```
Money Tracker Bot Google Apps Script is running!
```

### Viewing Execution Logs

1. In Apps Script editor, click **Executions** in the left sidebar
2. View recent executions to debug any issues

## 🔒 Security Notes

- The web app is set to "Anyone" access for simplicity
- Consider setting up authentication if you need more security
- The script only accepts POST requests with valid JSON data
- All execution logs are available in your Google Apps Script dashboard

## 📈 Advanced Features

### Adding Charts and Analysis

You can extend the script to automatically create charts or summary data:

```javascript
function createMonthlySummary() {
  // Add code to create pivot tables, charts, etc.
}
```

### Email Notifications

Add email notifications for large transactions:

```javascript
function checkLargeTransaction(amount) {
  if (amount > 1000) {
    MailApp.sendEmail({
      to: 'your-email@gmail.com',
      subject: 'Large Transaction Alert',
      body: `Transaction of $${amount} recorded`
    });
  }
}
```

## ✅ Verification

After setup, your integration should:

1. ✅ Receive POST requests from the bot
2. ✅ Parse JSON transaction data
3. ✅ Save data to Google Sheets with proper formatting
4. ✅ Return "Success" response to the bot
5. ✅ Handle different transaction types (expense, income, transfer)
6. ✅ Create headers and format the sheet automatically

Your Money Tracker Bot is now fully integrated with Google Sheets! 🎉
