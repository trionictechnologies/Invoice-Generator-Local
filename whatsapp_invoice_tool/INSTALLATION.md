# Installation Guide

## Windows Installation

### Method 1: Using Executable (Easiest)

1. Download `WhatsAppInvoiceTool.exe` from releases
2. Double-click to run
3. No Python installation needed!

### Method 2: From Source

#### Prerequisites

1. **Python 3.8 or higher**
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **wkhtmltopdf**
   - Download from https://wkhtmltopdf.org/downloads.html
   - Install to default location
   - Recommended version: 0.12.6

#### Installation Steps

1. **Extract the folder**
   ```
   Extract whatsapp_invoice_tool.zip to any location
   ```

2. **Open Command Prompt in the folder**
   - Open the folder in File Explorer
   - Hold Shift and right-click
   - Select "Open PowerShell window here" or "Open Command Prompt here"

3. **Run setup**
   ```bash
   python setup.py
   ```

4. **Configure**
   - Edit `config.json` with your company details

5. **Run the application**
   - Double-click `run.bat`
   - Or run: `python app.py`

## Verification

After installation, verify everything works:

```bash
# Check Python
python --version

# Check dependencies
pip list | findstr PySide6
pip list | findstr openpyxl
pip list | findstr playwright

# Check wkhtmltopdf
wkhtmltopdf --version
```

## Troubleshooting Installation

### "Python is not recognized"

**Problem:** Python not in system PATH

**Solution:**
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Search for "Environment Variables" in Windows
   - Edit PATH variable
   - Add: `C:\PythonXX` and `C:\PythonXX\Scripts`

### "pip is not recognized"

**Problem:** pip not installed or not in PATH

**Solution:**
```bash
python -m ensurepip --upgrade
```

### "wkhtmltopdf not found"

**Problem:** wkhtmltopdf not installed or not in PATH

**Solution:**
1. Install from https://wkhtmltopdf.org/downloads.html
2. During installation, note the installation path
3. Add to PATH:
   - Usually: `C:\Program Files\wkhtmltopdf\bin`

### Playwright installation fails

**Problem:** Network issues or permissions

**Solution:**
```bash
# Try with admin privileges
python -m playwright install chromium

# Or set environment variable
set PLAYWRIGHT_BROWSERS_PATH=0
python -m playwright install chromium
```

### "Access Denied" errors

**Problem:** Insufficient permissions

**Solution:**
- Run Command Prompt as Administrator
- Or install to a folder where you have write permissions

## Updating

To update to a new version:

1. Backup your `config.json`
2. Extract new version to a different folder
3. Copy your `config.json` back
4. Run `python setup.py` again

## Uninstallation

To remove the application:

1. Delete the `whatsapp_invoice_tool` folder
2. (Optional) Remove Python if not needed for other apps
3. (Optional) Remove wkhtmltopdf if not needed

That's it! No registry entries or system modifications are made.

## Manual Installation (Advanced)

If setup.py doesn't work, install manually:

```bash
# Install dependencies one by one
pip install PySide6==6.6.1
pip install openpyxl==3.1.2
pip install Jinja2==3.1.3
pip install pdfkit==1.0.0
pip install playwright==1.41.1

# Install Playwright browser
python -m playwright install chromium

# Create directories
mkdir logs
mkdir invoices_output
mkdir playwright_profile
```

## System Requirements

**Minimum:**
- Windows 10 (64-bit)
- 4 GB RAM
- 500 MB free disk space
- Internet connection (for WhatsApp Web)

**Recommended:**
- Windows 10/11 (64-bit)
- 8 GB RAM
- 1 GB free disk space
- Broadband internet connection

## Next Steps

After successful installation:
1. Read `QUICKSTART.md` for usage guide
2. Edit `config.json` with your details
3. Test with `sample_invoices.xlsx`
