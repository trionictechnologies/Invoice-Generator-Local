"""
Excel read/write utilities for invoice workflow.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string

from .config import load_config, project_path
from .logger import get_logger


logger = get_logger(__name__)
CONFIG = load_config()
COLUMNS = CONFIG.get("columns", {})


def _column_index(column_key: str) -> int:
  letter = COLUMNS.get(column_key)
  if not letter:
    raise KeyError(f"Column mapping missing for {column_key}")
  return column_index_from_string(letter)


def _resolve_path(path: str) -> Path:
  return project_path(path, writable=True)


def load_invoices(path: str) -> List[Dict[str, Optional[str]]]:
  """
  Read invoice data from the provided Excel file.
  Returns a list of dictionaries keyed by column names.
  """
  excel_path = _resolve_path(path)
  workbook = load_workbook(excel_path, data_only=True)
  sheet = workbook.active
  invoices: List[Dict[str, Optional[str]]] = []

  for row in range(2, sheet.max_row + 1):
    invoice_no = sheet.cell(row=row, column=_column_index("InvoiceNo")).value
    if invoice_no is None:
      continue
    record = {
        "InvoiceNo": str(invoice_no).strip(),
        "CustomerName": sheet.cell(row=row, column=_column_index("CustomerName")).value,
        "PhoneNumber": sheet.cell(row=row, column=_column_index("PhoneNumber")).value,
        "Amount": sheet.cell(row=row, column=_column_index("Amount")).value,
        "InvoiceDate": sheet.cell(row=row, column=_column_index("InvoiceDate")).value,
        "Status": sheet.cell(row=row, column=_column_index("Status")).value,
        "PaymentReceived": sheet.cell(row=row, column=_column_index("PaymentReceived")).value,
    }
    invoices.append(record)

  workbook.close()
  logger.debug("Loaded %d invoices from %s", len(invoices), excel_path)
  return invoices


def _update_cell(path: str, invoice_no: str, column_key: str, value: str) -> bool:
  excel_path = _resolve_path(path)
  workbook = load_workbook(excel_path)
  sheet = workbook.active
  updated = False

  for row in range(2, sheet.max_row + 1):
    cell_value = sheet.cell(row=row, column=_column_index("InvoiceNo")).value
    if cell_value is None:
      continue
    if str(cell_value).strip() == str(invoice_no).strip():
      sheet.cell(row=row, column=_column_index(column_key), value=value)
      updated = True
      break

  if updated:
    workbook.save(excel_path)
    logger.info("Updated %s for invoice %s -> %s", column_key, invoice_no, value)
  else:
    logger.warning("Invoice %s not found when updating %s", invoice_no, column_key)

  workbook.close()
  return updated


def update_status(path: str, invoice_no: str, status: str) -> bool:
  """Update the Status cell for a given invoice."""
  return _update_cell(path, invoice_no, "Status", status)


def update_payment_received(path: str, invoice_no: str, value: str) -> bool:
  """Update the PaymentReceived cell for a given invoice."""
  return _update_cell(path, invoice_no, "PaymentReceived", value)
