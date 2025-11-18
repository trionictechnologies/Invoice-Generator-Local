# File Structure and Description

Complete list of all files in the WhatsApp Invoice Tool project.

## 📁 Root Directory

### Application Files

**`app.py`** (37 lines)
- Main entry point for the application
- Initializes Qt application and main window
- Handles application lifecycle

**`config.json`** (31 lines)
- Configuration file for the application
- Contains company information, message templates, column mappings
- Customizable settings for automation behavior

**`requirements.txt`** (5 lines)
- Python package dependencies
- PySide6, openpyxl, Jinja2, pdfkit, playwright

### Setup and Build Files

**`setup.py`** (100 lines)
- Automated setup script
- Installs dependencies and sets up environment
- Creates directories and sample files

**`create_sample_excel.py`** (65 lines)
- Generates sample Excel file for testing
- Creates 5 sample invoices with proper formatting
- Includes header styling

**`build_spec.py`** (50 lines)
- PyInstaller configuration generator
- Creates .spec file for building Windows executable
- Includes instructions for building

**`run.bat`** (15 lines)
- Windows batch file to launch application
- Checks for Python installation
- Simple double-click launcher

### Documentation

**`README.md`** (280 lines)
- Complete project documentation
- Features, installation, usage, troubleshooting
- Configuration guide and examples

**`QUICKSTART.md`** (260 lines)
- Quick start guide for new users
- Step-by-step setup instructions
- Common tasks and troubleshooting

**`INSTALLATION.md`** (220 lines)
- Detailed installation instructions
- Prerequisites and verification steps
- Platform-specific guides

**`PROJECT_SUMMARY.md`** (450 lines)
- Technical project overview
- Architecture, modules, workflows
- Development notes and future enhancements

**`FILES.md`** (this file)
- Complete file structure documentation
- Purpose and description of each file

### Sample Data

**`sample_invoices.xlsx`** (Excel file)
- Example Excel file with 5 sample invoices
- Proper column structure and formatting
- Ready to test with

### Git Files

**`.gitignore`** (40 lines)
- Git ignore patterns
- Excludes logs, generated PDFs, Python cache
- Includes sample Excel file

---

## 📁 core/ Directory

Python modules containing core business logic.

**`__init__.py`** (1 line)
- Package initializer
- Makes core a Python package

**`logger.py`** (80 lines)
- Logging utility class
- Logs to both file and console
- Singleton pattern for global logger access
- Creates logs/app.log automatically

**`excel_manager.py`** (220 lines)
- Excel file operations
- Functions: load_invoices(), update_status(), update_payment_received()
- Configurable column indices
- Handles data type conversions and error handling

**`invoice_generator.py`** (120 lines)
- PDF invoice generation
- Uses Jinja2 templates and pdfkit
- Functions: generate_invoice_pdf(), generate_multiple_invoices()
- Injects company info and formats currency

**`whatsapp_client.py`** (350 lines)
- WhatsApp Web automation using Playwright
- Functions: login(), open_chat(), send_message_with_attachment(), get_recent_messages()
- Session persistence (no repeat QR scanning)
- Configurable selectors and timeouts

**`payment_checker.py`** (145 lines)
- Payment confirmation detection
- Keyword-based message scanning
- Functions: check_payment_for_invoice(), check_multiple_invoices()
- Configurable payment keywords

---

## 📁 ui/ Directory

User interface components using PySide6 (Qt6).

**`__init__.py`** (1 line)
- Package initializer
- Makes ui a Python package

**`main_window.py`** (440 lines)
- Main application window (QMainWindow)
- Three main actions: Login, Send Invoices, Check Payments
- Worker threads for long-running tasks
- Real-time activity log and progress indicators
- File selection, error handling, status updates

**`resources/`** (directory)
- Placeholder for UI resources
- Icons, images, stylesheets (future)

---

## 📁 templates/ Directory

HTML templates for PDF generation.

**`invoice.html`** (225 lines)
- Professional invoice template
- Jinja2 placeholders for dynamic content
- Indian business format (₹ symbol, GSTIN, etc.)
- Includes:
  - Company header with logo placeholder
  - Customer details
  - Invoice items table
  - Total amount
  - Payment information (bank details, UPI)
  - Terms and conditions section
  - Professional styling with CSS

---

## 📁 Output Directories

Directories created at runtime.

**`invoices_output/`**
- Generated PDF invoices stored here
- One PDF per invoice (named by invoice number)
- Example: INV-2024-001.pdf

**`logs/`**
- Application log files
- `app.log` - Main application log
- Includes timestamps, log levels, messages

**`playwright_profile/`**
- Playwright browser profile storage
- WhatsApp Web session persistence
- Created on first login
- Delete this folder to force re-login

---

## 📊 File Statistics

### Total Files
- Python files: 10
- Documentation files: 5
- Configuration files: 2
- Template files: 1
- Utility files: 3
- Sample files: 1
- **Total: 22 files**

### Lines of Code (Approximate)
- Python code: ~1,700 lines
- Documentation: ~1,400 lines
- HTML/Templates: ~225 lines
- Configuration: ~60 lines
- **Total: ~3,385 lines**

### File Categories

**Core Application (2 files)**
- app.py
- config.json

**Business Logic (5 files)**
- excel_manager.py
- invoice_generator.py
- whatsapp_client.py
- payment_checker.py
- logger.py

**User Interface (1 file)**
- main_window.py

**Templates (1 file)**
- invoice.html

**Utilities (4 files)**
- setup.py
- create_sample_excel.py
- build_spec.py
- run.bat

**Documentation (5 files)**
- README.md
- QUICKSTART.md
- INSTALLATION.md
- PROJECT_SUMMARY.md
- FILES.md

**Sample Data (1 file)**
- sample_invoices.xlsx

**Configuration (3 files)**
- requirements.txt
- .gitignore
- __init__.py files

---

## 🔍 Finding Files

### By Function

**Want to customize invoices?**
→ `templates/invoice.html`

**Want to change company info?**
→ `config.json`

**Want to see logs?**
→ `logs/app.log`

**Want to modify Excel columns?**
→ `config.json` (column_indices)

**Want to add payment keywords?**
→ `config.json` (payment_keywords)

**Want to change WhatsApp message?**
→ `config.json` (message_template)

### By Task

**Installing:**
→ `setup.py`, `requirements.txt`, `INSTALLATION.md`

**Running:**
→ `app.py`, `run.bat`

**Building Executable:**
→ `build_spec.py`

**Learning:**
→ `README.md`, `QUICKSTART.md`, `PROJECT_SUMMARY.md`

**Testing:**
→ `sample_invoices.xlsx`, `create_sample_excel.py`

**Troubleshooting:**
→ `logs/app.log`, `README.md` (Troubleshooting section)

---

## 🎯 Key Files for Customization

1. **`config.json`** - All settings and configuration
2. **`templates/invoice.html`** - Invoice appearance
3. **`ui/main_window.py`** - GUI customization
4. **`core/whatsapp_client.py`** - WhatsApp automation tweaks

---

## 📦 Files Included in Executable Build

When building with PyInstaller, these files are bundled:

- app.py (main script)
- config.json (configuration)
- templates/invoice.html (template)
- All core/ modules
- All ui/ modules
- Python dependencies

**Not included** (user must create):
- Excel invoice files
- logs/ directory (created at runtime)
- playwright_profile/ (created on first login)

---

## 🔐 Sensitive Files (Do Not Share)

- `logs/app.log` - May contain personal data
- `playwright_profile/` - Contains WhatsApp session
- Your actual Excel files with customer data
- Modified `config.json` with real bank details

---

## ✨ Complete File Tree

```
whatsapp_invoice_tool/
│
├── app.py                      # Main entry point
├── config.json                 # Configuration
├── requirements.txt            # Dependencies
├── .gitignore                 # Git ignore rules
│
├── setup.py                    # Setup script
├── create_sample_excel.py     # Sample generator
├── build_spec.py              # Build configuration
├── run.bat                     # Windows launcher
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── INSTALLATION.md            # Install instructions
├── PROJECT_SUMMARY.md         # Technical overview
├── FILES.md                   # This file
│
├── sample_invoices.xlsx       # Sample data
│
├── core/                      # Core modules
│   ├── __init__.py
│   ├── logger.py
│   ├── excel_manager.py
│   ├── invoice_generator.py
│   ├── whatsapp_client.py
│   └── payment_checker.py
│
├── ui/                        # User interface
│   ├── __init__.py
│   ├── main_window.py
│   └── resources/
│
├── templates/                 # Invoice templates
│   └── invoice.html
│
├── invoices_output/          # Generated PDFs
│
├── logs/                     # Log files
│   └── app.log
│
└── playwright_profile/       # Browser session
```

---

**Last Updated:** 2024-01-19
