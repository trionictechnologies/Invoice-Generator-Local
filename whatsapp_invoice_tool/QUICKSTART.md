# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Prerequisites

**Required:**
1. **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
2. **wkhtmltopdf** - [Download here](https://wkhtmltopdf.org/downloads.html)

### Step 2: Setup

Run the automated setup:

```bash
python setup.py
```

This will:
- ✓ Install all Python dependencies
- ✓ Install Playwright browser
- ✓ Create necessary directories
- ✓ Generate a sample Excel file

### Step 3: Configure Your Details

Edit `config.json` and update:

```json
{
  "company_info": {
    "CompanyName": "Your Company Name",      ← Change this
    "CompanyAddress": "Your Address",        ← Change this
    "CompanyPhone": "+91 XXXXXXXXXX",        ← Change this
    "CompanyEmail": "your@email.com",        ← Change this
    "BankName": "Your Bank",                 ← Change this
    "AccountNumber": "XXXXXXXXXXXX",         ← Change this
    "IFSCCode": "XXXXXX",                   ← Change this
    "UPIID": "yourupi@bank"                 ← Change this
  }
}
```

### Step 4: Prepare Your Excel File

Use `sample_invoices.xlsx` as a template or create your own with these columns:

| InvoiceNo | CustomerName | PhoneNumber | Amount | InvoiceDate | Status | PaymentReceived |
|-----------|--------------|-------------|--------|-------------|--------|-----------------|
| INV-001   | John Doe     | 919876543210| 5000   | 2024-01-15  | Pending|                 |

**Important:** Phone numbers must include country code (91 for India)

### Step 5: Run the Application

**Windows:** Double-click `run.bat`

**Or use command line:**
```bash
python app.py
```

### Step 6: Use the Application

1. **Login to WhatsApp**
   - Click "1. Login to WhatsApp"
   - Scan QR code with your phone
   - Wait for confirmation

2. **Send Invoices**
   - Select your Excel file
   - Click "2. Generate & Send Pending Invoices"
   - Watch the progress in the log

3. **Check Payments**
   - Click "3. Check Payment Status"
   - Payment confirmations will be marked in Excel

## 📋 Excel File Format

Your Excel file should have these columns in order:

**Column A - InvoiceNo** (Required)
- Unique invoice number
- Example: `INV-2024-001`

**Column B - CustomerName** (Required)
- Customer's full name
- Example: `Rajesh Kumar`

**Column C - PhoneNumber** (Required)
- Must include country code
- Format: `919876543210` (no spaces, +, or -)
- India: Start with `91`

**Column D - Amount** (Required)
- Invoice amount (number only)
- Example: `15000` or `15000.50`

**Column E - InvoiceDate** (Required)
- Date in any format
- Example: `2024-01-15` or `15-Jan-2024`

**Column F - Status** (Auto-updated)
- Initial: `Pending`
- After send: `Sent`
- On error: `Error: reason`

**Column G - PaymentReceived** (Auto-updated)
- Empty initially
- Filled with timestamp when payment detected

## 🎯 Common Tasks

### Send Invoices to New Customers

1. Add new rows to Excel with `Status = Pending`
2. Save Excel file
3. Click "Generate & Send Pending Invoices"

### Resend a Failed Invoice

1. In Excel, change `Status` from `Error:...` to `Pending`
2. Save Excel file
3. Click "Generate & Send Pending Invoices"

### Customize Invoice Template

1. Edit `templates/invoice.html`
2. Modify the HTML/CSS as needed
3. Test with a sample invoice

### Change WhatsApp Message

Edit `message_template` in `config.json`:

```json
"message_template": "Hi {CustomerName}, Invoice {InvoiceNo} for ₹{Amount} is attached."
```

Available variables:
- `{CustomerName}`
- `{InvoiceNo}`
- `{InvoiceDate}`
- `{Amount}`
- `{FirmName}`

## ❗ Troubleshooting

**Problem: "wkhtmltopdf not found"**
- Solution: Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html

**Problem: WhatsApp not loading**
- Solution: Delete `playwright_profile` folder and login again

**Problem: Invoice not sending**
- Solution: Check phone number format (must be 919876543210, not +91-98765-43210)

**Problem: Payment not detected**
- Solution: Add more keywords to `payment_keywords` in config.json

## 📦 Building Executable

To create a standalone `.exe` file:

```bash
pip install pyinstaller
python build_spec.py
pyinstaller whatsapp_invoice_tool.spec
```

The executable will be in `dist/` folder.

## 🔒 Privacy & Security

- ✓ All data stays on your computer
- ✓ No cloud servers or external APIs
- ✓ WhatsApp session stored locally
- ✓ Excel files are not uploaded anywhere

## 📞 Need Help?

1. Check `logs/app.log` for detailed error messages
2. Review `README.md` for full documentation
3. Verify all prerequisites are installed
4. Test with the sample Excel file first

## 🎉 You're Ready!

The tool is now set up and ready to use. Start by testing with the sample Excel file before using your real data.

Happy invoicing! 🚀
