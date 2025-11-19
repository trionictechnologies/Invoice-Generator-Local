# Building Windows Executable (.exe)

## ⚠️ Important Note

**PyInstaller must run on the target platform.** To create a Windows `.exe`, you must run PyInstaller on a Windows machine.

This guide shows you how to build the executable on Windows.

---

## 🪟 Method 1: Build on Windows (Recommended)

### Prerequisites

1. **Windows 10/11** (64-bit)
2. **Python 3.8-3.11** installed from [python.org](https://www.python.org/downloads/)
3. **Git** (optional, to clone the project)

### Step 1: Copy Project to Windows

**Option A: Download from GitHub/repository**
- Download and extract the `whatsapp_invoice_tool` folder to your Windows machine

**Option B: Copy manually**
- Copy the entire `whatsapp_invoice_tool` folder to your Windows PC

### Step 2: Open Command Prompt

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to the project folder:
   ```cmd
   cd C:\path\to\whatsapp_invoice_tool
   ```

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
pip install pyinstaller
```

### Step 4: Install wkhtmltopdf

1. Download from: https://wkhtmltopdf.org/downloads.html
2. Install to default location
3. Note the installation path (usually `C:\Program Files\wkhtmltopdf\bin`)

### Step 5: Build the Executable

**Option A: Using the spec file (Recommended)**

```cmd
python build_windows.py
```

This will:
- Create the PyInstaller spec file
- Build the executable
- Output: `dist/WhatsAppInvoiceTool.exe`

**Option B: Manual PyInstaller command**

```cmd
pyinstaller --onefile --windowed --name WhatsAppInvoiceTool ^
  --add-data "config.json;." ^
  --add-data "templates;templates" ^
  --hidden-import PySide6 ^
  --hidden-import openpyxl ^
  --hidden-import jinja2 ^
  --hidden-import pdfkit ^
  --hidden-import playwright ^
  --icon=icon.ico ^
  app.py
```

### Step 6: Find Your Executable

The `.exe` file will be in:
```
whatsapp_invoice_tool/dist/WhatsAppInvoiceTool.exe
```

### Step 7: Create Distribution Package

Create a folder with:
```
WhatsAppInvoiceTool/
  ├── WhatsAppInvoiceTool.exe    (from dist/)
  ├── config.json                (copy from project)
  ├── templates/                 (copy folder from project)
  │   └── invoice.html
  ├── README.md                  (copy from project)
  └── sample_invoices.xlsx       (copy from project)
```

Users can now run `WhatsAppInvoiceTool.exe` directly!

---

## 🎯 Method 2: Automated Build Script

I've created an automated build script for you.

### Using build_windows.py

1. **On Windows**, navigate to project folder
2. Run:
   ```cmd
   python build_windows.py
   ```

3. Wait for build to complete (2-5 minutes)

4. Check the `dist/` folder for the executable

### What the script does:

- ✅ Checks Python version
- ✅ Installs PyInstaller
- ✅ Creates optimized spec file
- ✅ Builds executable
- ✅ Creates distribution folder
- ✅ Copies necessary files
- ✅ Shows final location

---

## 📦 Distribution Package Structure

After building, create this structure for distribution:

```
WhatsAppInvoiceTool_v1.0/
├── WhatsAppInvoiceTool.exe
├── config.json
├── templates/
│   └── invoice.html
├── README.md
├── QUICKSTART.md
└── sample_invoices.xlsx
```

Zip this folder and distribute to users.

---

## 🐛 Troubleshooting Build Issues

### "Python is not recognized"

**Solution:** Add Python to PATH
1. Search for "Environment Variables"
2. Edit PATH
3. Add: `C:\Python3X` and `C:\Python3X\Scripts`

### "PyInstaller is not recognized"

**Solution:**
```cmd
python -m PyInstaller --onefile app.py
```

### "ModuleNotFoundError" during build

**Solution:** Install missing module
```cmd
pip install <module_name>
```

### Build takes very long

**Normal:** First build can take 3-5 minutes
**If stuck:** Press Ctrl+C and try again

### Executable won't run

**Check:**
1. Windows Defender/Antivirus (may block)
2. Run as Administrator
3. Check for error messages

### Antivirus flags the .exe

**Normal:** PyInstaller executables are sometimes flagged
**Solution:** 
- Add exception in antivirus
- Or use `--windowed` flag (already included)

---

## 📊 Expected Build Output

```
Building WhatsApp Invoice Tool...
✓ Checking dependencies
✓ Creating spec file
✓ Building executable
✓ Packaging resources
✓ Creating distribution folder

Build Complete!
═══════════════════════════════════════════
Executable Location:
  dist/WhatsAppInvoiceTool.exe

File Size: ~150-200 MB
(Large due to bundled Python + Qt + Browser)

Distribution Package:
  dist_package/WhatsAppInvoiceTool/

Ready for distribution!
═══════════════════════════════════════════
```

---

## 🎁 What's Included in the Executable

The `.exe` includes:
- ✅ Python interpreter
- ✅ All Python libraries (PySide6, Playwright, etc.)
- ✅ Application code
- ✅ Templates and configuration

**NOT included** (user must have):
- ❌ wkhtmltopdf (must install separately)
- ❌ Playwright browsers (installed on first run)

---

## 📋 First-Time Setup for Users

When users run the executable for the first time:

1. **Install wkhtmltopdf**
   - Download: https://wkhtmltopdf.org/downloads.html
   - Install to default location

2. **Install Playwright browser** (optional, done automatically)
   - The app will download Chromium on first WhatsApp login

3. **Configure company details**
   - Edit `config.json` in the same folder as the .exe

4. **Run the executable**
   - Double-click `WhatsAppInvoiceTool.exe`

---

## 🔧 Advanced Build Options

### Reduce File Size

Use `--onefile` with compression:
```cmd
pyinstaller --onefile --windowed ^
  --upx-dir C:\path\to\upx ^
  app.py
```

Download UPX from: https://upx.github.io/

### Add Custom Icon

```cmd
pyinstaller --icon=icon.ico --onefile app.py
```

Create `icon.ico` (256x256 recommended)

### Console Version (for debugging)

Remove `--windowed` flag:
```cmd
pyinstaller --onefile app.py
```

This shows a console window with debug output.

---

## 🚀 Quick Build Commands

**Minimal build:**
```cmd
pyinstaller --onefile app.py
```

**GUI application:**
```cmd
pyinstaller --onefile --windowed app.py
```

**With icon and name:**
```cmd
pyinstaller --onefile --windowed --name WhatsAppInvoiceTool --icon=icon.ico app.py
```

**Full build (recommended):**
```cmd
python build_windows.py
```

---

## 📝 Build Checklist

Before building:
- [ ] All dependencies installed
- [ ] wkhtmltopdf installed
- [ ] Code tested and working
- [ ] config.json has defaults
- [ ] Templates are in place
- [ ] README is up to date

After building:
- [ ] Test the .exe on clean Windows machine
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test with sample data
- [ ] Create distribution package

---

## 🎓 Understanding the Build

### What PyInstaller Does

1. **Analyzes** your Python script
2. **Finds** all imported modules
3. **Bundles** Python interpreter + libraries
4. **Creates** a single executable
5. **Packages** resources (templates, config)

### Build Time

- **First build:** 3-5 minutes (downloads dependencies)
- **Subsequent builds:** 1-2 minutes (uses cache)

### File Size

- **Expected:** 150-250 MB
- **Reason:** Includes Qt framework + Playwright + Python
- **Normal:** This is standard for Qt-based applications

---

## 💡 Tips

1. **Test before distributing:** Always test on a clean Windows machine
2. **Include README:** Users need setup instructions
3. **Provide support:** Include contact/support information
4. **Version your builds:** Use version numbers
5. **Sign your executable:** For professional distribution (optional)

---

## 🆘 Need Help?

**Build fails:**
1. Check Python version (3.8-3.11)
2. Ensure all dependencies installed
3. Try cleaning build cache: `rmdir /s build dist`
4. Check logs in `build/` folder

**Executable doesn't work:**
1. Test on Windows 10/11
2. Check antivirus settings
3. Run from command prompt to see errors
4. Ensure wkhtmltopdf is installed

---

## 📞 Support

For build issues:
1. Check build logs in `build/warn-xxx.txt`
2. Review PyInstaller documentation
3. Test each module individually
4. Simplify and rebuild

---

## ✅ Success Checklist

Your build is successful when:
- [x] .exe file created in dist/
- [x] File size is 150-250 MB
- [x] Double-clicking opens the application
- [x] GUI appears correctly
- [x] Can select Excel file
- [x] Can login to WhatsApp
- [x] Can generate PDFs
- [x] Can send messages

---

**Happy Building! 🎉**
