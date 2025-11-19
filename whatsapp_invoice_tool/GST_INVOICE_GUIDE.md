# GST Invoice Format - Complete Guide

## 🎯 Overview

The WhatsApp Invoice Tool now supports **professional Indian GST-compliant invoices** with a smart two-sheet Excel structure for easy column mapping and customization.

---

## 📊 Excel Structure

Your Excel file will have **TWO sheets**:

### Sheet 1: **InvoiceData**
Contains all your invoice records with GST details

### Sheet 2: **ColumnMapping**  
Maps field names to Excel columns (for easy customization)

This means you can **rearrange columns** in your data sheet and the app will still work - just update the mapping sheet!

---

## 📋 Complete Field List

The GST invoice format includes **24 fields**:

### Supplier Information (Your Company)
1. **Logo** - Path to company logo image (optional)
2. **SupplierName** - Your company name
3. **SupplierAddress** - Complete business address
4. **SupplierGSTIN** - Your GST Identification Number

### Buyer Information (Customer)
5. **BuyerName** - Customer/buyer company name
6. **BuyerAddress** - Customer's complete address
7. **BuyerGSTIN** - Customer's GSTIN (if registered)

### Invoice Details
8. **InvoiceNumber** - Unique invoice/proforma number (e.g., PI/2024/001)
9. **InvoiceDate** - Invoice date (DD-MMM-YYYY format)
10. **Description** - Description of goods/services
11. **SAC_HSN** - SAC code (services) or HSN code (goods)

### Amount Details
12. **Total** - Amount before taxes
13. **CGST** - Central GST amount (for intra-state)
14. **SGST** - State GST amount (for intra-state)
15. **IGST** - Integrated GST (for inter-state)
16. **GrandTotal** - Final total including all taxes
17. **AmountInWords** - Total in words (e.g., "One Lakh Rupees Only")

### Payment & Terms
18. **BankDetails** - Your bank account details
19. **TermsOfDelivery** - Delivery and payment terms
20. **OtherTerms** - Additional T&C (e.g., "E. & O.E.")
21. **SignatureField** - Path to signature image (optional)

### WhatsApp Integration
22. **PhoneNumber** - Customer's WhatsApp number (91XXXXXXXXXX format)
23. **Status** - Invoice status (Pending/Sent/Error) - **Auto-updated**
24. **PaymentReceived** - Payment confirmation - **Auto-updated**

---

## 💡 How Column Mapping Works

### Example Scenario

Your Excel columns are arranged differently:

```
A: InvoiceNumber
B: InvoiceDate  
C: BuyerName
D: BuyerAddress
... (your custom order)
```

**No problem!** Just update the **ColumnMapping** sheet:

| Field Name | Excel Column Letter | Description |
|------------|---------------------|-------------|
| InvoiceNumber | A | Unique invoice number |
| InvoiceDate | B | Invoice date |
| BuyerName | C | Customer name |
| BuyerAddress | D | Customer address |
| ... | ... | ... |

The application reads this mapping and knows where to find each field!

---

## 🧮 GST Calculations

### Intra-State Transaction (Same State)
Use **CGST + SGST**:
- Total: ₹100,000
- CGST @9%: ₹9,000
- SGST @9%: ₹9,000
- **GrandTotal: ₹118,000**
- IGST: 0

### Inter-State Transaction (Different State)  
Use **IGST**:
- Total: ₹100,000
- CGST: 0
- SGST: 0
- IGST @18%: ₹18,000
- **GrandTotal: ₹118,000**

### Common GST Rates
- **5%** - Essential services
- **12%** - Standard services
- **18%** - Most professional services
- **28%** - Luxury goods/services

---

## 📝 Sample Data Format

### Example Invoice Row

```excel
| Field | Value |
|-------|-------|
| SupplierName | ABC Enterprises Pvt Ltd |
| SupplierAddress | 123, Business Park, MG Road, Mumbai - 400001 |
| SupplierGSTIN | 27AABCU9603R1ZM |
| BuyerName | XYZ Corporation |
| BuyerAddress | 456, Industrial Area, Pune - 411001 |
| BuyerGSTIN | 27AABCX1234E1Z5 |
| InvoiceNumber | PI/2024/001 |
| InvoiceDate | 15-Jan-2024 |
| Description | Professional Consulting Services |
| SAC_HSN | 998314 |
| Total | 100000.00 |
| CGST | 9000.00 |
| SGST | 9000.00 |
| IGST | 0.00 |
| GrandTotal | 118000.00 |
| AmountInWords | One Lakh Eighteen Thousand Rupees Only |
| BankDetails | Bank: HDFC Bank\nAccount: 50200012345678\nIFSC: HDFC0001234 |
| TermsOfDelivery | Payment: 30 days from invoice date |
| OtherTerms | Subject to Mumbai Jurisdiction |
| PhoneNumber | 919876543210 |
| Status | Pending |
| PaymentReceived | |
```

---

## 🎨 Invoice Template Features

The GST invoice includes:

### Header Section
- ✅ Company logo placeholder
- ✅ Supplier name and address
- ✅ Supplier GSTIN
- ✅ Professional layout

### Invoice Details
- ✅ Buyer information with GSTIN
- ✅ Invoice number and date
- ✅ "PROFORMA INVOICE" title

### Items Table
- ✅ Serial number, Description, SAC/HSN
- ✅ Quantity, Rate, Amount
- ✅ Professional formatting

### Tax Summary
- ✅ Sub-total
- ✅ CGST/SGST (if intra-state)
- ✅ IGST (if inter-state)
- ✅ Grand Total (highlighted)

### Footer
- ✅ Amount in words
- ✅ Bank details for payment
- ✅ Terms of delivery
- ✅ Other terms and conditions
- ✅ Authorized signatory space

---

## 🔧 Customization Options

### 1. Rearrange Excel Columns
- Move columns in InvoiceData sheet
- Update ColumnMapping sheet accordingly
- App adapts automatically!

### 2. Add Company Logo
- Save logo as PNG/JPG
- Put file path in Logo column
- Example: `C:\logos\company_logo.png`

### 3. Add Signature
- Scan signature or create digital signature
- Put file path in SignatureField column
- Example: `C:\signatures\authorized_sign.png`

### 4. Customize Bank Details
Use multi-line format:
```
Bank: HDFC Bank
Account No: 50200012345678
IFSC: HDFC0001234
Branch: Mumbai Main
UPI: company@hdfc
```

### 5. Customize Terms
```
TermsOfDelivery:
- Immediate delivery
- Payment: 30 days from invoice date
- Late payment: 2% interest per month

OtherTerms:
- Subject to Mumbai Jurisdiction
- E. & O.E. (Errors and Omissions Excepted)
- This is a proforma invoice
```

---

## 📱 WhatsApp Integration

### Phone Number Format
**Must include country code:**
- ✅ Correct: `919876543210` (India)
- ✅ Correct: `971501234567` (UAE)
- ❌ Wrong: `+91-98765-43210`
- ❌ Wrong: `9876543210` (missing country code)

### Message Template
Configure in `config.json`:
```json
"message_template": "Dear {CustomerName}, please find your Proforma Invoice {InvoiceNumber} dated {InvoiceDate} for ₹{Amount}. Thank you for your business. - {FirmName}"
```

Available placeholders:
- `{CustomerName}` → BuyerName
- `{InvoiceNumber}` → InvoiceNumber
- `{InvoiceDate}` → InvoiceDate
- `{Amount}` → GrandTotal (formatted)
- `{FirmName}` → SupplierName

---

## 🚀 Quick Setup Guide

### Step 1: Use the Template
```bash
cd whatsapp_invoice_tool
# Use: gst_invoices_template.xlsx
```

### Step 2: Fill Your Data
1. Open **InvoiceData** sheet
2. Replace sample data with your invoices
3. Fill all required fields
4. Save file

### Step 3: Check Mapping
1. Open **ColumnMapping** sheet
2. Verify field-to-column mapping
3. Adjust if you rearranged columns

### Step 4: Configure App
Edit `config.json`:
```json
{
  "data_sheet_name": "InvoiceData",
  "mapping_sheet_name": "ColumnMapping",
  "invoice_template": "gst_invoice.html"
}
```

### Step 5: Run Application
```bash
python app.py
```

---

## 📖 Best Practices

### 1. Invoice Numbering
Use consistent format:
- `PI/2024/001` - Proforma Invoice
- `INV/2024/001` - Tax Invoice
- `QT/2024/001` - Quotation

### 2. GSTIN Validation
- 15 characters
- Format: `22AAAAA0000A1Z5`
- State code (first 2 digits) should match

### 3. SAC/HSN Codes
**Common SAC codes for services:**
- `998311` - Advertising services
- `998313` - IT design & development
- `998314` - Consultancy services
- `998316` - Marketing services
- `998319` - Other professional services

**HSN codes for goods:** 4-8 digit codes (e.g., `6109` for T-shirts)

### 4. Amount in Words
Be consistent:
- ✅ "One Lakh Eighteen Thousand Rupees Only"
- ✅ "Rs. 1,18,000/- (Rupees One Lakh Eighteen Thousand Only)"

### 5. Bank Details
Include all payment options:
- Bank account details
- IFSC code
- UPI ID
- QR code (optional, in template)

---

## 🔍 Validation Checklist

Before sending invoices:

### Supplier Details
- [ ] SupplierName filled
- [ ] SupplierAddress complete
- [ ] SupplierGSTIN valid (15 chars)

### Buyer Details
- [ ] BuyerName filled
- [ ] BuyerAddress complete
- [ ] BuyerGSTIN (if customer is registered)

### Invoice Details
- [ ] InvoiceNumber unique
- [ ] InvoiceDate in correct format
- [ ] Description clear and detailed
- [ ] SAC/HSN code correct

### Amounts
- [ ] Total calculated correctly
- [ ] GST rates applied correctly
- [ ] CGST+SGST for intra-state OR IGST for inter-state
- [ ] GrandTotal = Total + CGST + SGST + IGST
- [ ] AmountInWords matches GrandTotal

### WhatsApp
- [ ] PhoneNumber with country code
- [ ] PhoneNumber is valid WhatsApp number

---

## 🆘 Troubleshooting

### Issue: Columns not mapping correctly
**Solution:** Check ColumnMapping sheet, ensure column letters match your InvoiceData sheet

### Issue: GST amounts wrong
**Solution:** 
- For intra-state: Set CGST + SGST, IGST = 0
- For inter-state: Set IGST, CGST = 0, SGST = 0

### Issue: Invoice looks broken
**Solution:** Check that all required fields have values, especially SupplierName, BuyerName, InvoiceNumber

### Issue: WhatsApp number not working
**Solution:** Use format `91XXXXXXXXXX` (no spaces, hyphens, or plus signs)

---

## 📚 Additional Resources

### File Locations
- **Template:** `gst_invoices_template.xlsx`
- **Invoice Template:** `templates/gst_invoice.html`
- **Config:** `config.json`

### Sample Files
- **With data:** `gst_invoices_template.xlsx` (3 sample invoices)
- **Basic template:** `sample_invoices.xlsx` (simple format)

### Customization
- Edit `templates/gst_invoice.html` for layout changes
- Edit `config.json` for settings
- Both templates (basic & GST) are supported

---

## 🎓 Pro Tips

1. **Keep a master template** - Save a blank copy for creating new invoice batches

2. **Use Excel formulas** - Calculate CGST, SGST, IGST, GrandTotal automatically:
   ```excel
   CGST: =L2*0.09  (9% of Total)
   SGST: =L2*0.09  (9% of Total)
   GrandTotal: =L2+M2+N2+O2  (Total + all taxes)
   ```

3. **Create reusable bank details** - Save common text in a separate sheet, copy when needed

4. **Batch similar invoices** - Group by state (for consistent GST type)

5. **Backup regularly** - Keep copies of sent invoices

6. **Version control** - Add date to filename: `invoices_jan2024.xlsx`

---

## ✅ Summary

**New GST Format Advantages:**
- ✅ Fully GST-compliant
- ✅ Professional appearance
- ✅ Flexible column arrangement
- ✅ Easy customization via mapping sheet
- ✅ Supports both intra-state and inter-state transactions
- ✅ All fields Indian businesses need
- ✅ Backward compatible (old format still works)

**Result:** Professional, compliant invoices that impress clients and simplify accounting!

---

**Need Help?** Check `README.md` and `QUICKSTART.md` for application usage, or refer to this guide for GST-specific questions.
