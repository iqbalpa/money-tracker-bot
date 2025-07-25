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
    console.log('=== doPost called ===');
    console.log('Received POST request:', e.postData.contents);
    
    // Parse the JSON payload
    const data = JSON.parse(e.postData.contents);
    console.log('Parsed data:', JSON.stringify(data));
    
    // Validate required fields
    if (!data.type || !data.amount || !data.date) {
      throw new Error('Missing required fields: type, amount, or date');
    }
    
    // Save data to spreadsheet
    const result = saveToSpreadsheet(data);
    console.log('saveToSpreadsheet result:', result);
    
    // Return success response
    return ContentService
      .createTextOutput('Success')
      .setMimeType(ContentService.MimeType.TEXT);
      
  } catch (error) {
    console.error('=== Error in doPost ===');
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
    console.log('=== saveToSpreadsheet called ===');
    console.log('Data type:', data.type);
    
    // Get or create the appropriate sheet based on transaction type
    const sheet = getOrCreateSheetByType(data.type);
    console.log('Sheet obtained:', sheet.getName());
    
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
    
    console.log('Row data prepared:', JSON.stringify(rowData));
    
    // Add the row to the appropriate sheet
    sheet.appendRow(rowData);
    console.log('Row appended to sheet');
    
    // Get the new row index and setup dropdowns
    const newRowIndex = sheet.getLastRow();
    console.log('=== DROPDOWN SETUP START ===');
    console.log('Setting up dropdowns for new row:', newRowIndex, 'type:', data.type);
    
    // Call dropdown setup
    setupDropdownsForNewRow(sheet, newRowIndex, data.type);
    
    console.log('=== DROPDOWN SETUP END ===');
    console.log('Dropdown setup completed for row:', newRowIndex);
    
    console.log('Successfully saved transaction:', data.type, data.amount, 'to', sheet.getName());
    return true;
    
  } catch (error) {
    console.error('=== Error in saveToSpreadsheet ===');
    console.error('Error saving to spreadsheet:', error);
    console.error('Stack trace:', error.stack);
    throw error;
  }
}

/**
 * Get dropdown options for categories and accounts
 */
function getDropdownOptions() {
  return {
    categories: [
      'Food & Dining',
      'Transportation',
      'Shopping',
      'Entertainment',
      'Bills & Utilities',
      'Healthcare',
      'Education',
      'Travel',
      'Personal Care',
      'Gifts & Donations',
      'Investment',
      'Salary',
      'Business',
      'Other'
    ],
    accounts: [
      'Cash',
      'BRI',
      'Mandiri',
      'Bank Jago',
      'Gopay',
      'OVO',
      'ShopeePay',
      'PayPal',
    ]
  };
}

/**
 * Setup dropdown data validation for a specific range
 */
function setupDropdownValidation(range, options, helpText) {
  console.log('setupDropdownValidation called with options count:', options.length);
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(options, true)
    .setAllowInvalid(false)
    .setHelpText(helpText)
    .build();
  range.setDataValidation(rule);
  console.log('Dropdown validation rule applied successfully');
}

/**
 * Setup dropdowns for existing data in a sheet
 */
function setupDropdownsForSheet(sheet, transactionType) {
  const lastRow = sheet.getLastRow();
  const dropdownOptions = getDropdownOptions();
  
  if (lastRow > 1) { // Only if there's data beyond headers
    if (transactionType === 'expense' || transactionType === 'income') {
      // Category dropdown (column D)
      const categoryRange = sheet.getRange(2, 4, lastRow - 1, 1);
      setupDropdownValidation(categoryRange, dropdownOptions.categories, 'Select a category from the dropdown');
      
      // Account dropdown (column E)
      const accountRange = sheet.getRange(2, 5, lastRow - 1, 1);
      setupDropdownValidation(accountRange, dropdownOptions.accounts, 'Select an account from the dropdown');
    } else if (transactionType === 'transfer') {
      // From Account dropdown (column D)
      const fromAccountRange = sheet.getRange(2, 4, lastRow - 1, 1);
      setupDropdownValidation(fromAccountRange, dropdownOptions.accounts, 'Select the source account');
      
      // To Account dropdown (column E)
      const toAccountRange = sheet.getRange(2, 5, lastRow - 1, 1);
      setupDropdownValidation(toAccountRange, dropdownOptions.accounts, 'Select the destination account');
    }
  }
}

/**
 * Setup dropdowns for a new row
 */
function setupDropdownsForNewRow(sheet, rowIndex, transactionType) {
  console.log('setupDropdownsForNewRow called with:', rowIndex, transactionType);
  const dropdownOptions = getDropdownOptions();
  
  if (transactionType === 'expense' || transactionType === 'income') {
    console.log('Setting up expense/income dropdowns for row:', rowIndex);
    // Category dropdown (column D)
    const categoryCell = sheet.getRange(rowIndex, 4);
    setupDropdownValidation(categoryCell, dropdownOptions.categories, 'Select a category from the dropdown');
    console.log('Category dropdown set for row:', rowIndex);
    
    // Account dropdown (column E)
    const accountCell = sheet.getRange(rowIndex, 5);
    setupDropdownValidation(accountCell, dropdownOptions.accounts, 'Select an account from the dropdown');
    console.log('Account dropdown set for row:', rowIndex);
  } else if (transactionType === 'transfer') {
    console.log('Setting up transfer dropdowns for row:', rowIndex);
    // From Account dropdown (column D)
    const fromAccountCell = sheet.getRange(rowIndex, 4);
    setupDropdownValidation(fromAccountCell, dropdownOptions.accounts, 'Select the source account');
    console.log('From Account dropdown set for row:', rowIndex);
    
    // To Account dropdown (column E)
    const toAccountCell = sheet.getRange(rowIndex, 5);
    setupDropdownValidation(toAccountCell, dropdownOptions.accounts, 'Select the destination account');
    console.log('To Account dropdown set for row:', rowIndex);
  }
  console.log('setupDropdownsForNewRow completed for row:', rowIndex);
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
 * Initialize dropdowns for all existing sheets and data
 * Run this function once to add dropdowns to all existing data
 */
function initializeAllDropdowns() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (!spreadsheet) {
      throw new Error('No active spreadsheet found');
    }
    
    const sheetTypes = ['expense', 'income', 'transfer'];
    const sheetNames = ['Expenses', 'Income', 'Transfers'];
    
    for (let i = 0; i < sheetTypes.length; i++) {
      const sheet = spreadsheet.getSheetByName(sheetNames[i]);
      if (sheet) {
        console.log('Setting up dropdowns for sheet:', sheetNames[i]);
        setupDropdownsForSheet(sheet, sheetTypes[i]);
      }
    }
    
    console.log('✅ Dropdown initialization completed for all sheets');
    return 'Dropdowns initialized successfully';
    
  } catch (error) {
    console.error('Error initializing dropdowns:', error);
    throw error;
  }
}

/**
 * Add dropdown validation to a specific sheet manually
 * Useful for maintenance or when adding dropdowns to existing data
 */
function addDropdownsToSheet(sheetName) {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(sheetName);
    
    if (!sheet) {
      throw new Error('Sheet not found: ' + sheetName);
    }
    
    // Determine transaction type based on sheet name
    let transactionType;
    if (sheetName === 'Expenses') transactionType = 'expense';
    else if (sheetName === 'Income') transactionType = 'income';
    else if (sheetName === 'Transfers') transactionType = 'transfer';
    else throw new Error('Unknown sheet type: ' + sheetName);
    
    setupDropdownsForSheet(sheet, transactionType);
    console.log('✅ Dropdowns added to sheet:', sheetName);
    return 'Dropdowns added successfully to ' + sheetName;
    
  } catch (error) {
    console.error('Error adding dropdowns to sheet:', error);
    throw error;
  }
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
      category: 'Food & Dining',
      account: 'Cash',
      description: 'Test lunch expense'
    },
    {
      timestamp: new Date().toISOString(),
      date: '2025-07-25',
      type: 'income',
      amount: 1000.00,
      category: 'Salary',
      account: 'BRI',
      description: 'Test monthly salary'
    },
    {
      timestamp: new Date().toISOString(),
      date: '2025-07-25',
      type: 'transfer',
      amount: 200.00,
      from_account: 'Gopay',
      to_account: 'Mandiri',
      description: 'Test transfer from e-wallet to bank'
    }
  ];
  
  console.log('Testing script with sample data...');
  console.log('This will create 3 separate sheets: Expenses, Income, Transfers');
  console.log('Dropdowns will be automatically added to category and account fields');
  
  for (const testData of testTransactions) {
    try {
      saveToSpreadsheet(testData);
      console.log('✅ Successfully saved:', testData.type, 'to', testData.type.charAt(0).toUpperCase() + testData.type.slice(1), 'sheet');
    } catch (error) {
      console.error('❌ Failed to save:', testData.type, error);
    }
  }
  
  console.log('Test completed! Check your spreadsheet for 3 new sheets with dropdown menus.');
  console.log('Category and account fields should now have dropdown validation.');
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
  console.log('=== doGet called ===');
  console.log('GET request received');
  return ContentService
    .createTextOutput('Money Tracker Bot Google Apps Script is running!')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Simple function to test if the deployment is working with logs
 */
function testDeployment() {
  console.log('=== testDeployment called ===');
  console.log('Testing deployment...');
  
  // Test the dropdown setup with a simple case
  const testData = {
    timestamp: new Date().toISOString(),
    date: '2025-07-25',
    type: 'expense',
    amount: 1.00,
    category: 'Other',
    account: 'Cash',
    description: 'Deployment test'
  };
  
  console.log('Calling saveToSpreadsheet with test data...');
  const result = saveToSpreadsheet(testData);
  console.log('Test result:', result);
  
  return 'Deployment test completed - check logs';
}
