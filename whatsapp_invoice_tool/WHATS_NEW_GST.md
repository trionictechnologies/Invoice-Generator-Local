# 🎉 What's New: GST Invoice Support!

## Major Update: Professional Indian GST-Compliant Invoices

Your WhatsApp Invoice Tool now supports **full-featured Indian GST invoices** with smart column mapping!

---

## ✨ New Features

### 1. **Two-Sheet Excel Structure**

Your Excel file now has:
- **Sheet 1: InvoiceData** - All your invoice records
- **Sheet 2: ColumnMapping** - Field-to-column mapping

**Benefits:**
- ✅ Rearrange columns however you want
- ✅ App adapts automatically via mapping
- ✅ No hardcoded column positions
- ✅ Easy to customize

### 2. **Complete GST Invoice Format**

All fields Indian businesses need:

**Supplier Details:**
- Company name, address, GSTIN
- Logo support

**Buyer Details:**
- Customer name, address, GSTIN

**Invoice Information:**
- Invoice number, date
- Description, SAC/HSN codes

**Tax Calculations:**
- Subtotal amount
- CGST (Central GST)
- SGST (State GST)
- IGST (Integrated GST)
- Grand Total
- Amount in words

**Payment & Terms:**
- Bank details
- Terms of delivery
- Other terms & conditions
- Signature field

**WhatsApp Integration:**
- Phone number
- Auto-updated status
- Auto-updated payment confirmation

**Total: 24 fields** - everything you need!

### 3. **Professional Invoice Template**

New `gst_invoice.html` template with:
- ✅ Clean, professional layout
- ✅ GST-compliant format
- ✅ Logo and signature support
- ✅ Tax breakdown (CGST/SGST or IGST)
- ✅ Amount in words
- ✅ Bank details section
- ✅ Terms and conditions
- ✅ Print-ready design

### 4. **Smart Column Mapping**

**Before (Old Way):**
```
Column A MUST be InvoiceNo
Column B MUST be CustomerName
Column C MUST be PhoneNumber
... (fixed positions)
```

**Now (New Way):**
```
Your columns can be ANYWHERE!
Just update the ColumnMapping sheet:

Field Name     | Excel Column
---------------|-------------
InvoiceNumber  | H  (your choice!)
BuyerName      | E  (your choice!)
PhoneNumber    | V  (your choice!)
```

**Result:** Total flexibility!

---

## 📦 What's Included

### New Files

1. **`gst_invoices_template.xlsx`** - Ready-to-use template with sample data
   - InvoiceData sheet (3 sample invoices)
   - ColumnMapping sheet (field mappings)

2. **`templates/gst_invoice.html`** - Professional GST invoice template

3. **`GST_INVOICE_GUIDE.md`** - Complete 300+ line guide covering:
   - All 24 fields explained
   - GST calculation examples
   - Column mapping tutorial
   - Sample data formats
   - Customization options
   - Best practices
   - Troubleshooting

### Updated Files

1. **`core/excel_manager.py`** - Now reads multiple sheets and column mappings
2. **`config.json`** - New settings for GST format
3. **`README.md`** - Updated with GST format info

---

## 🚀 How to Use

### Quick Start (3 Steps)

**Step 1: Use the new template**
```bash
cd whatsapp_invoice_tool
# Open: gst_invoices_template.xlsx
```

**Step 2: Fill your data**
- Sheet 1 (InvoiceData): Add your invoices
- Sheet 2 (ColumnMapping): Verify mapping (or customize)

**Step 3: Run the app**
```bash
python app.py
```

That's it! The app will:
- Read your data using the mapping
- Generate GST-compliant PDFs
- Send via WhatsApp
- Track payments

---

## 📊 Sample Invoice Data

### Intra-State Transaction (Same State)
```
SupplierName: ABC Enterprises (Mumbai)
SupplierGSTIN: 27AABCU9603R1ZM
BuyerName: XYZ Corp (Pune)
BuyerGSTIN: 27AABCX1234E1Z5

Total: ₹100,000
CGST @9%: ₹9,000
SGST @9%: ₹9,000
IGST: ₹0
GrandTotal: ₹118,000
```

### Inter-State Transaction (Different States)
```
SupplierName: ABC Enterprises (Mumbai)
SupplierGSTIN: 27AABCU9603R1ZM
BuyerName: LMN Industries (Bangalore)
BuyerGSTIN: 29AABCL5678F1Z3

Total: ₹100,000
CGST: ₹0
SGST: ₹0
IGST @18%: ₹18,000
GrandTotal: ₹118,000
```

---

## 🎨 Customization Options

### 1. Add Your Logo
```excel
Logo column: C:\logos\company_logo.png
```

### 2. Add Digital Signature
```excel
SignatureField: C:\signatures\authorized_sign.png
```

### 3. Rearrange Columns
- Rearrange columns in InvoiceData sheet however you want
- Update ColumnMapping sheet with new column letters
- App reads mapping and works automatically!

### 4. Customize Template
- Edit `templates/gst_invoice.html`
- Change colors, fonts, layout
- Add/remove sections as needed

### 5. Multi-line Fields
Bank Details example:
```
Bank: HDFC Bank
Account No: 50200012345678
IFSC: HDFC0001234
Branch: Mumbai Main
UPI: company@hdfc
```

---

## 🔄 Backward Compatibility

**Don't worry!** Your old Excel files still work:

- Old format (`sample_invoices.xlsx`) - Still supported
- Old template (`invoice.html`) - Still available
- Simple format - Still works perfectly

**New GST format is optional** - use it when you need GST-compliant invoices!

---

## 📚 Documentation

### Complete Guides Available

1. **`GST_INVOICE_GUIDE.md`** (NEW!)
   - 300+ lines of detailed documentation
   - All fields explained
   - GST calculations
   - Examples and samples
   - Best practices
   - Troubleshooting

2. **`README.md`** (Updated)
   - Overview of both formats
   - Quick start guide
   - Installation instructions

3. **`QUICKSTART.md`** (Updated)
   - Get started in 5 minutes
   - Supports both formats

4. **`BUILD_WINDOWS.md`**
   - Build Windows executable
   - Packaging instructions

---

## 🎯 Common Use Cases

### Use Case 1: B2B Services (Professional Consulting)
- Use GST format
- Add your GSTIN and logo
- Include SAC code (998314 for consulting)
- Apply 18% GST
- Professional bank details
- Clear payment terms

### Use Case 2: Interstate Sales
- Use IGST (not CGST+SGST)
- Ensure buyer GSTIN is correct
- State codes should differ
- Include HSN codes for goods

### Use Case 3: Small Local Invoices
- Use simple format (old style)
- Quick and easy
- No GST complexity

### Use Case 4: Proforma Invoices
- Use GST format
- Title: "PROFORMA INVOICE"
- All details included
- Professional appearance

---

## 💡 Pro Tips

1. **Use Excel Formulas**
   ```excel
   CGST: =L2*0.09  (9% of Total)
   SGST: =L2*0.09
   IGST: =L2*0.18  (for inter-state)
   GrandTotal: =L2+M2+N2+O2
   ```

2. **Master Template**
   - Keep a blank copy
   - Use it to create new batches
   - Save time on data entry

3. **Batch Processing**
   - Group similar invoices
   - Same GST rate = faster processing
   - Same state = consistent CGST/SGST

4. **Validation**
   - Check GSTIN format (15 characters)
   - Verify state codes match addresses
   - Ensure totals are correct
   - Test with one invoice first

5. **Backups**
   - Save copies of sent invoices
   - Version control your Excel files
   - Keep PDF archives

---

## 🆘 Need Help?

### Quick References

**For GST Format:**
→ Read `GST_INVOICE_GUIDE.md` (comprehensive)

**For Basic Usage:**
→ Read `QUICKSTART.md` (5-minute setup)

**For Installation:**
→ Read `INSTALLATION.md` (detailed steps)

**For Building .exe:**
→ Read `BUILD_WINDOWS.md` (Windows executable)

### Common Questions

**Q: Do I have to use GST format?**
A: No! Old simple format still works. Use GST when you need it.

**Q: Can I use my own column order?**
A: Yes! Just update the ColumnMapping sheet.

**Q: What if I don't have a GSTIN?**
A: Leave it blank or use simple format.

**Q: Can I mix CGST/SGST and IGST?**
A: No. Use CGST+SGST for intra-state OR IGST for inter-state, not both.

**Q: Is this GST-compliant?**
A: Yes! The format follows GST invoice requirements.

---

## 🎉 Summary

**What's New:**
- ✅ Full GST invoice support (24 fields)
- ✅ Two-sheet Excel structure
- ✅ Smart column mapping
- ✅ Professional invoice template
- ✅ Complete documentation
- ✅ Sample data included
- ✅ Backward compatible

**Benefits:**
- 💼 Professional appearance
- 📋 GST-compliant
- 🔄 Flexible column arrangement
- ⚡ Easy to customize
- 📱 WhatsApp integration
- 💰 Payment tracking
- 🚀 Time-saving automation

**Files:**
- 📊 `gst_invoices_template.xlsx` - New template
- 📄 `templates/gst_invoice.html` - New template
- 📖 `GST_INVOICE_GUIDE.md` - Complete guide

---

## 🚀 Get Started Now!

1. **Open:** `gst_invoices_template.xlsx`
2. **Explore:** Two sheets (InvoiceData + ColumnMapping)
3. **Read:** `GST_INVOICE_GUIDE.md` for details
4. **Fill:** Your invoice data
5. **Run:** `python app.py`
6. **Send:** Professional GST invoices via WhatsApp!

---

**Everything you need for professional, GST-compliant invoice automation! 🎊**

---

*For questions, refer to the comprehensive `GST_INVOICE_GUIDE.md` or other documentation files.*
