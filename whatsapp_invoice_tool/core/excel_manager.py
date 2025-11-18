"""
Excel Manager for WhatsApp Invoice Tool.
Handles reading and writing invoice data from Excel files.
"""
import openpyxl
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from .logger import logger


class ExcelManager:
    """Manages Excel file operations for invoice data."""
    
    # Default column indices (1-based, as used by openpyxl)
    COL_INVOICE_NO = 1      # A
    COL_CUSTOMER_NAME = 2   # B
    COL_PHONE_NUMBER = 3    # C
    COL_AMOUNT = 4          # D
    COL_INVOICE_DATE = 5    # E
    COL_STATUS = 6          # F
    COL_PAYMENT_RECEIVED = 7 # G
    
    def __init__(self, file_path: str, config: Optional[Dict] = None):
        """
        Initialize Excel Manager.
        
        Args:
            file_path: Path to the Excel file
            config: Optional configuration dict with column indices
        """
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        # Load column config if provided
        if config and "column_indices" in config:
            col_config = config["column_indices"]
            self.COL_INVOICE_NO = col_config.get("invoice_no", self.COL_INVOICE_NO)
            self.COL_CUSTOMER_NAME = col_config.get("customer_name", self.COL_CUSTOMER_NAME)
            self.COL_PHONE_NUMBER = col_config.get("phone_number", self.COL_PHONE_NUMBER)
            self.COL_AMOUNT = col_config.get("amount", self.COL_AMOUNT)
            self.COL_INVOICE_DATE = col_config.get("invoice_date", self.COL_INVOICE_DATE)
            self.COL_STATUS = col_config.get("status", self.COL_STATUS)
            self.COL_PAYMENT_RECEIVED = col_config.get("payment_received", self.COL_PAYMENT_RECEIVED)
    
    def load_invoices(self) -> List[Dict]:
        """
        Load all invoice rows from Excel file.
        
        Returns:
            List of invoice dictionaries with keys: InvoiceNo, CustomerName, PhoneNumber,
            Amount, InvoiceDate, Status, PaymentReceived, and RowNumber
        """
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            sheet = workbook.active
            
            invoices = []
            
            # Skip header row (row 1), start from row 2
            for row_num in range(2, sheet.max_row + 1):
                row = sheet[row_num]
                
                # Read values from configured columns
                invoice_no = self._get_cell_value(row, self.COL_INVOICE_NO)
                customer_name = self._get_cell_value(row, self.COL_CUSTOMER_NAME)
                phone_number = self._get_cell_value(row, self.COL_PHONE_NUMBER)
                amount = self._get_cell_value(row, self.COL_AMOUNT)
                invoice_date = self._get_cell_value(row, self.COL_INVOICE_DATE)
                status = self._get_cell_value(row, self.COL_STATUS)
                payment_received = self._get_cell_value(row, self.COL_PAYMENT_RECEIVED)
                
                # Skip empty rows
                if not invoice_no:
                    continue
                
                # Convert phone number to string and clean it
                if phone_number:
                    phone_number = str(phone_number).replace(" ", "").replace("-", "").replace("+", "")
                
                # Convert invoice date to string if it's a datetime object
                if isinstance(invoice_date, datetime):
                    invoice_date = invoice_date.strftime("%Y-%m-%d")
                elif invoice_date:
                    invoice_date = str(invoice_date)
                
                invoice_data = {
                    "InvoiceNo": str(invoice_no) if invoice_no else "",
                    "CustomerName": str(customer_name) if customer_name else "",
                    "PhoneNumber": phone_number if phone_number else "",
                    "Amount": float(amount) if amount else 0.0,
                    "InvoiceDate": invoice_date if invoice_date else "",
                    "Status": str(status) if status else "Pending",
                    "PaymentReceived": str(payment_received) if payment_received else "",
                    "RowNumber": row_num  # Store for later updates
                }
                
                invoices.append(invoice_data)
            
            workbook.close()
            logger.info(f"Loaded {len(invoices)} invoices from {self.file_path}")
            return invoices
            
        except Exception as e:
            logger.error(f"Error loading invoices from Excel: {str(e)}")
            raise
    
    def update_status(self, invoice_no: str, status: str) -> bool:
        """
        Update the status column for a specific invoice.
        
        Args:
            invoice_no: Invoice number to update
            status: New status value (e.g., "Sent", "Error:...")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            sheet = workbook.active
            
            # Find the row with matching invoice number
            for row_num in range(2, sheet.max_row + 1):
                row = sheet[row_num]
                current_invoice_no = str(self._get_cell_value(row, self.COL_INVOICE_NO))
                
                if current_invoice_no == str(invoice_no):
                    # Update status column
                    sheet.cell(row=row_num, column=self.COL_STATUS, value=status)
                    workbook.save(self.file_path)
                    workbook.close()
                    logger.info(f"Updated status for invoice {invoice_no} to '{status}'")
                    return True
            
            workbook.close()
            logger.warning(f"Invoice {invoice_no} not found in Excel")
            return False
            
        except Exception as e:
            logger.error(f"Error updating status for invoice {invoice_no}: {str(e)}")
            return False
    
    def update_payment_received(self, invoice_no: str, value: str) -> bool:
        """
        Update the PaymentReceived column for a specific invoice.
        
        Args:
            invoice_no: Invoice number to update
            value: Payment received value (timestamp or "Yes")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            sheet = workbook.active
            
            # Find the row with matching invoice number
            for row_num in range(2, sheet.max_row + 1):
                row = sheet[row_num]
                current_invoice_no = str(self._get_cell_value(row, self.COL_INVOICE_NO))
                
                if current_invoice_no == str(invoice_no):
                    # Update payment received column
                    sheet.cell(row=row_num, column=self.COL_PAYMENT_RECEIVED, value=value)
                    workbook.save(self.file_path)
                    workbook.close()
                    logger.info(f"Updated payment received for invoice {invoice_no} to '{value}'")
                    return True
            
            workbook.close()
            logger.warning(f"Invoice {invoice_no} not found in Excel")
            return False
            
        except Exception as e:
            logger.error(f"Error updating payment received for invoice {invoice_no}: {str(e)}")
            return False
    
    @staticmethod
    def _get_cell_value(row, col_index: int):
        """
        Get cell value from row at given column index.
        
        Args:
            row: openpyxl row object
            col_index: 1-based column index
            
        Returns:
            Cell value or None
        """
        try:
            return row[col_index - 1].value  # Convert to 0-based index
        except IndexError:
            return None
