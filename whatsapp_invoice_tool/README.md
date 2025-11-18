# WhatsApp Invoice Automation Tool

A Windows desktop application for automating invoice generation and delivery via WhatsApp Web. Built for Indian SMEs and accounting firms.

## Features

- 📊 **Excel Integration**: Read invoice data from Excel files
- 📄 **PDF Generation**: Create professional invoices from customizable HTML templates
- 📱 **WhatsApp Automation**: Send invoices automatically via WhatsApp Web
- 💰 **Payment Tracking**: Monitor WhatsApp messages for payment confirmations
- 🔄 **Status Updates**: Automatically update Excel with send status and payment confirmations

## Prerequisites

### System Requirements
- Windows 10/11
- Python 3.8 or higher (for development)
- wkhtmltopdf (for PDF generation)

### Installing wkhtmltopdf

1. Download from: https://wkhtmltopdf.org/downloads.html
2. Install to default location (usually `C:\Program Files\wkhtmltopdf`)
3. Add to PATH or the tool will find it automatically

## Installation

### For Users (Executable)

1. Download the `WhatsAppInvoiceTool.exe` from releases
2. Run the executable - no installation needed!

### For Developers

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

### 1. Prepare Your Excel File

Create an Excel file with the following columns:

| Column | Name | Description | Example |
|--------|------|-------------|---------|
| A | InvoiceNo | Unique invoice number | INV-001 |
| B | CustomerName | Customer's name | John Doe |
| C | PhoneNumber | Phone with country code | 919876543210 |
| D | Amount | Invoice amount | 5000 |
| E | InvoiceDate | Invoice date | 2024-01-15 |
| F | Status | Send status | Pending/Sent |
| G | PaymentReceived | Payment confirmation | Yes/No/Timestamp |

**Sample Excel file structure:**

```
InvoiceNo | CustomerName | PhoneNumber   | Amount | InvoiceDate | Status  | PaymentReceived
INV-001   | John Doe     | 919876543210  | 5000   | 2024-01-15  | Pending |
INV-002   | Jane Smith   | 919876543211  | 7500   | 2024-01-15  | Pending |
```

### 2. Configure the Application

Edit `config.json` to customize:

- **Company Information**: Name, address, bank details
- **Message Template**: Customize the WhatsApp message
- **Payment Keywords**: Words to detect payment confirmations
- **Column Indices**: If your Excel has different column layout

Example configuration:

```json
{
  "company_info": {
    "CompanyName": "ABC Enterprises",
    "CompanyAddress": "123 Business Street",
    "CompanyPhone": "+91 9876543210",
    "CompanyEmail": "accounts@abc.com"
  },
  "message_template": "Dear {CustomerName}, your invoice {InvoiceNo} for ₹{Amount} is attached."
}
```

### 3. Using the Application

#### Step 1: Login to WhatsApp

1. Click **"1. Login to WhatsApp"**
2. A browser window will open with WhatsApp Web
3. Scan the QR code with your phone
4. Wait for login confirmation
5. Session will be saved - you won't need to scan again next time

#### Step 2: Generate & Send Invoices

1. Select your Excel file using the **Browse** button
2. Click **"2. Generate & Send Pending Invoices"**
3. The tool will:
   - Generate PDF invoices for all "Pending" rows
   - Send them via WhatsApp with your custom message
   - Update Excel status to "Sent" or "Error"

#### Step 3: Check Payment Status

1. Click **"3. Check Payment Status"**
2. The tool will:
   - Check WhatsApp messages for payment keywords
   - Update Excel with payment timestamps when found

## Configuration Options

### Message Template Variables

Available placeholders for `message_template`:
- `{CustomerName}` - Customer's name
- `{InvoiceNo}` - Invoice number
- `{InvoiceDate}` - Invoice date
- `{Amount}` - Invoice amount
- `{FirmName}` - Your company name

### Payment Keywords

Default keywords that indicate payment:
- paid, payment done, payment completed
- sent, done, transferred
- upi, imps, rtgs, neft
- transaction, successful, credited

You can add more keywords in `config.json`.

### Excel Column Configuration

If your Excel has different column positions, update `column_indices` in `config.json`:

```json
"column_indices": {
  "invoice_no": 1,
  "customer_name": 2,
  "phone_number": 3,
  "amount": 4,
  "invoice_date": 5,
  "status": 6,
  "payment_received": 7
}
```

## Invoice Template Customization

The invoice PDF is generated from `templates/invoice.html`. You can customize:

- Layout and styling (CSS)
- Company logo (add `<img>` tag)
- Additional fields (add variables in template)
- Colors and fonts

## Troubleshooting

### "wkhtmltopdf not found" Error

**Solution**: Download and install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html

### WhatsApp Web Not Loading

**Solutions**:
- Clear browser cache: Delete `playwright_profile` folder
- Check internet connection
- Try logging in again

### Messages Not Sending

**Solutions**:
- Verify phone numbers have country code (e.g., 91 for India)
- Ensure numbers are saved in WhatsApp
- Check if WhatsApp Web session is active
- Increase `send_delay` in config.json

### Payment Not Detected

**Solutions**:
- Add more payment keywords to `payment_keywords` in config.json
- Check if customer sent message in correct chat
- Increase `messages_to_check` in config.json

## Building Executable

To create a standalone `.exe` file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_spec.py
pyinstaller whatsapp_invoice_tool.spec

# Executable will be in dist/ folder
```

## Project Structure

```
whatsapp_invoice_tool/
├── app.py                      # Main entry point
├── config.json                 # Configuration file
├── requirements.txt            # Python dependencies
├── core/
│   ├── excel_manager.py       # Excel read/write operations
│   ├── invoice_generator.py   # PDF generation
│   ├── whatsapp_client.py     # WhatsApp automation
│   ├── payment_checker.py     # Payment detection
│   └── logger.py              # Logging utility
├── ui/
│   └── main_window.py         # GUI interface
├── templates/
│   └── invoice.html           # Invoice PDF template
├── invoices_output/           # Generated PDFs
├── logs/                      # Application logs
└── playwright_profile/        # WhatsApp session storage
```

## Important Notes

⚠️ **Disclaimer**: This tool automates WhatsApp Web for business purposes. Use responsibly and in compliance with WhatsApp's Terms of Service.

⚠️ **Data Privacy**: All data is processed locally on your machine. No data is sent to external servers.

⚠️ **WhatsApp Updates**: WhatsApp Web's interface may change. If the tool stops working, check for updates.

## Support

For issues, questions, or contributions:
- Check the logs in `logs/app.log`
- Review the configuration in `config.json`
- Ensure all prerequisites are installed

## License

This tool is provided as-is for business automation purposes.

## Credits

Built for Indian SMEs and accounting firms to streamline invoice delivery and payment tracking.
