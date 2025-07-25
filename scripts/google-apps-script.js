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
 * Save transaction data to the appropriate Google Sheets spreadsheet
 */
function saveToSpreadsheet(data) {
  try {
    // Get or create the appropriate sheet based on transaction type
    const sheet = getOrCreateSheetByType(data.type);
    
    // Prepare row data based on transaction type
    let rowData;
    
    if (data.type === 'expense' || data.type === 'income') {
      rowData = [
        data.timestamp,           // A: Timestamp
        data.date,               // B: Date
        data.amount,             // C: Amount
        data.category || '',     // D: Category
        data.account || '',      // E: Account
        data.description || ''   // F: Description
      ];
    } else if (data.type === 'transfer') {
      rowData = [
        data.timestamp,              // A: Timestamp
        data.date,                   // B: Date
        data.amount,                 // C: Amount
        data.from_account || '',     // D: From Account
        data.to_account || '',       // E: To Account
        data.description || ''       // F: Description
      ];
    } else {
      throw new Error('Unknown transaction type: ' + data.type);
    }
    
    // Add the row to the appropriate sheet
    sheet.appendRow(rowData);
    
    console.log('Successfully saved transaction:', data.type, data.amount, 'to', sheet.getName());
    return true;
    
  } catch (error) {
    console.error('Error saving to spreadsheet:', error);
    throw error;
  }
}

/**
 * Get existing sheet or create new one with headers based on transaction type
 */
function getOrCreateSheetByType(transactionType) {
  // Define sheet configurations for each transaction type
  const sheetConfigs = {
    'expense': {
      name: 'Expenses',
      headers: ['Timestamp', 'Date', 'Amount', 'Category', 'Account', 'Description'],
      color: '#dc3545' // Red
    },
    'income': {
      name: 'Income',
      headers: ['Timestamp', 'Date', 'Amount', 'Category', 'Account', 'Description'],
      color: '#28a745' // Green
    },
    'transfer': {
      name: 'Transfers',
      headers: ['Timestamp', 'Date', 'Amount', 'From Account', 'To Account', 'Description'],
      color: '#17a2b8' // Blue
    }
  };
  
  const config = sheetConfigs[transactionType];
  if (!config) {
    throw new Error('Unknown transaction type: ' + transactionType);
  }
  
  // Get the active spreadsheet (the one bound to this script)
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    throw new Error('No active spreadsheet found. Please bind this script to a Google Sheets document.');
  }
  
  // Get or create the specific sheet
  let sheet = spreadsheet.getSheetByName(config.name);
  
  if (!sheet) {
    // Create new sheet with headers
    sheet = spreadsheet.insertSheet(config.name);
    
    // Add headers
    sheet.getRange(1, 1, 1, config.headers.length).setValues([config.headers]);
    
    // Format headers
    const headerRange = sheet.getRange(1, 1, 1, config.headers.length);
    headerRange.setFontWeight('bold');
    headerRange.setBackground(config.color);
    headerRange.setFontColor('white');
    
    // Set column widths based on transaction type
    if (transactionType === 'expense' || transactionType === 'income') {
      sheet.setColumnWidth(1, 180); // Timestamp
      sheet.setColumnWidth(2, 100); // Date
      sheet.setColumnWidth(3, 100); // Amount
      sheet.setColumnWidth(4, 120); // Category
      sheet.setColumnWidth(5, 120); // Account
      sheet.setColumnWidth(6, 200); // Description
    } else if (transactionType === 'transfer') {
      sheet.setColumnWidth(1, 180); // Timestamp
      sheet.setColumnWidth(2, 100); // Date
      sheet.setColumnWidth(3, 100); // Amount
      sheet.setColumnWidth(4, 120); // From Account
      sheet.setColumnWidth(5, 120); // To Account
      sheet.setColumnWidth(6, 200); // Description
    }
    
    // Freeze header row
    sheet.setFrozenRows(1);
    
    console.log('Created new sheet:', config.name, 'with headers');
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
  console.log('This will create 3 separate sheets: Expenses, Income, Transfers');
  
  for (const testData of testTransactions) {
    try {
      saveToSpreadsheet(testData);
      console.log('✅ Successfully saved:', testData.type, 'to', testData.type.charAt(0).toUpperCase() + testData.type.slice(1), 'sheet');
    } catch (error) {
      console.error('❌ Failed to save:', testData.type, error);
    }
  }
  
  console.log('Test completed! Check your spreadsheet for 3 new sheets.');
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
