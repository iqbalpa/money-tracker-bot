/**
 * Money Tracker Bot - Google Apps Script
 * 
 * This script receives POST requests from the Money Tracker Telegram Bot
 * and saves transaction data to a Google Sheets spreadsheet.
 * 
 * Deploy this as a web app with:
 * - Execute as: Me
 * - Who has access: Anyone
 */

/**
 * Main function that handles POST requests from the bot
 */
function doPost(e) {
  try {
    // Log the incoming request for debugging
    console.log('Received POST request:', e.postData.contents);
    
    // Parse the JSON payload
    const data = JSON.parse(e.postData.contents);
    
    // Validate required fields
    if (!data.type || !data.amount || !data.date) {
      throw new Error('Missing required fields: type, amount, or date');
    }
    
    // Save data to spreadsheet
    const result = saveToSpreadsheet(data);
    
    // Return success response
    return ContentService
      .createTextOutput('Success')
      .setMimeType(ContentService.MimeType.TEXT);
      
  } catch (error) {
    console.error('Error processing request:', error);
    
    // Return error response
    return ContentService
      .createTextOutput('Error: ' + error.message)
      .setMimeType(ContentService.MimeType.TEXT);
  }
}

/**
 * Save transaction data to the Google Sheets spreadsheet
 */
function saveToSpreadsheet(data) {
  try {
    // Get or create the spreadsheet
    const sheet = getOrCreateSheet();
    
    // Prepare row data based on transaction type
    let rowData;
    
    if (data.type === 'expense' || data.type === 'income') {
      rowData = [
        data.timestamp,           // A: Timestamp
        data.date,               // B: Date
        data.type,               // C: Type
        data.amount,             // D: Amount
        data.category || '',     // E: Category
        data.account || '',      // F: Account
        data.description || '',  // G: Description
        '',                      // H: From Account (empty for expense/income)
        ''                       // I: To Account (empty for expense/income)
      ];
    } else if (data.type === 'transfer') {
      rowData = [
        data.timestamp,              // A: Timestamp
        data.date,                   // B: Date
        data.type,                   // C: Type
        data.amount,                 // D: Amount
        '',                          // E: Category (empty for transfer)
        '',                          // F: Account (empty for transfer)
        data.description || '',      // G: Description
        data.from_account || '',     // H: From Account
        data.to_account || ''        // I: To Account
      ];
    } else {
      throw new Error('Unknown transaction type: ' + data.type);
    }
    
    // Add the row to the sheet
    sheet.appendRow(rowData);
    
    console.log('Successfully saved transaction:', data.type, data.amount);
    return true;
    
  } catch (error) {
    console.error('Error saving to spreadsheet:', error);
    throw error;
  }
}

/**
 * Get existing sheet or create new one with headers
 */
function getOrCreateSheet() {
  const SHEET_NAME = 'Money Tracker';
  
  // Try to get existing spreadsheet (replace with your spreadsheet ID if you have one)
  let spreadsheet;
  try {
    // Option 1: Use existing spreadsheet by ID (uncomment and add your ID)
    // spreadsheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID_HERE');
    
    // Option 2: Create new spreadsheet (comment out if using existing)
    spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (!spreadsheet) {
      spreadsheet = SpreadsheetApp.create('Money Tracker Data');
    }
  } catch (error) {
    // Create new spreadsheet if none exists
    spreadsheet = SpreadsheetApp.create('Money Tracker Data');
  }
  
  // Get or create the sheet
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    // Create new sheet with headers
    sheet = spreadsheet.insertSheet(SHEET_NAME);
    
    // Add headers
    const headers = [
      'Timestamp',      // A
      'Date',          // B
      'Type',          // C
      'Amount',        // D
      'Category',      // E
      'Account',       // F
      'Description',   // G
      'From Account',  // H
      'To Account'     // I
    ];
    
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    
    // Format headers
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#4285f4');
    headerRange.setFontColor('white');
    
    // Set column widths
    sheet.setColumnWidth(1, 180); // Timestamp
    sheet.setColumnWidth(2, 100); // Date
    sheet.setColumnWidth(3, 80);  // Type
    sheet.setColumnWidth(4, 100); // Amount
    sheet.setColumnWidth(5, 120); // Category
    sheet.setColumnWidth(6, 120); // Account
    sheet.setColumnWidth(7, 200); // Description
    sheet.setColumnWidth(8, 120); // From Account
    sheet.setColumnWidth(9, 120); // To Account
    
    // Freeze header row
    sheet.setFrozenRows(1);
    
    console.log('Created new sheet with headers');
  }
  
  return sheet;
}

/**
 * Test function to verify the script works
 * Run this function manually to test
 */
function testScript() {
  // Test data for each transaction type
  const testTransactions = [
    {
      timestamp: new Date().toISOString(),
      date: '2025-07-25',
      type: 'expense',
      amount: 25.50,
      category: 'food',
      account: 'cash',
      description: 'Test lunch expense'
    },
    {
      timestamp: new Date().toISOString(),
      date: '2025-07-25',
      type: 'income',
      amount: 1000.00,
      category: 'salary',
      account: 'bank',
      description: 'Test monthly salary'
    },
    {
      timestamp: new Date().toISOString(),
      date: '2025-07-25',
      type: 'transfer',
      amount: 200.00,
      from_account: 'cash',
      to_account: 'bank',
      description: 'Test transfer'
    }
  ];
  
  console.log('Testing script with sample data...');
  
  for (const testData of testTransactions) {
    try {
      saveToSpreadsheet(testData);
      console.log('✅ Successfully saved:', testData.type);
    } catch (error) {
      console.error('❌ Failed to save:', testData.type, error);
    }
  }
  
  console.log('Test completed!');
}

/**
 * Function to get the web app URL after deployment
 * Run this after deploying to get your URL for the .env file
 */
function getWebAppUrl() {
  // This will be available after you deploy the script as a web app
  console.log('After deploying as web app, your URL will be:');
  console.log('https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec');
  console.log('Add this URL to your .env file as SHEETS_API=<url>');
}

/**
 * Function to handle GET requests (optional, for testing)
 */
function doGet(e) {
  return ContentService
    .createTextOutput('Money Tracker Bot Google Apps Script is running!')
    .setMimeType(ContentService.MimeType.TEXT);
}
