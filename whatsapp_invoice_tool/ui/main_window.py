"""
PySide6 main window for the WhatsApp Invoice Tool.
"""

from __future__ import annotations

import traceback
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QRunnable, QThreadPool, Signal, Slot, QObject
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.config import load_config, project_path
from core.excel_manager import load_invoices, update_payment_received, update_status
from core.invoice_generator import generate_invoice_pdf
from core.payment_checker import PaymentChecker
from core.whatsapp_client import WhatsAppClient, build_message


CONFIG = load_config()


class WorkerSignals(QObject):
  finished = Signal()
  error = Signal(str)
  log = Signal(str)


class Worker(QRunnable):
  def __init__(self, fn: Callable, *args, **kwargs):
    super().__init__()
    self.fn = fn
    self.args = args
    self.kwargs = kwargs
    self.signals = WorkerSignals()

  @Slot()
  def run(self) -> None:
    def status_callback(message: str) -> None:
      self.signals.log.emit(message)

    execution_kwargs = dict(self.kwargs)
    execution_kwargs.setdefault("status_callback", status_callback)

    try:
      self.fn(*self.args, **execution_kwargs)
    except Exception as exc:  # noqa: BLE001
      error_text = f"{exc}\n{traceback.format_exc()}"
      self.signals.error.emit(error_text)
    finally:
      self.signals.finished.emit()


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("WhatsApp Invoice Tool")
    self.resize(900, 600)

    self.thread_pool = QThreadPool.globalInstance()
    self.whatsapp_client = WhatsAppClient()
    self.payment_checker = PaymentChecker(self.whatsapp_client)

    self._init_ui()
    self._load_default_excel_path()

  def _init_ui(self) -> None:
    central = QWidget(self)
    self.setCentralWidget(central)

    main_layout = QVBoxLayout()

    file_layout = QHBoxLayout()
    self.excel_path_edit = QLineEdit()
    file_layout.addWidget(QLabel("Excel File:"))
    file_layout.addWidget(self.excel_path_edit)
    browse_button = QPushButton("Browse…")
    browse_button.clicked.connect(self._browse_excel)
    file_layout.addWidget(browse_button)
    main_layout.addLayout(file_layout)

    buttons_layout = QHBoxLayout()
    self.login_button = QPushButton("Login to WhatsApp")
    self.login_button.clicked.connect(self._handle_login)
    buttons_layout.addWidget(self.login_button)

    self.send_button = QPushButton("Generate & Send Pending Invoices")
    self.send_button.clicked.connect(self._handle_send_invoices)
    buttons_layout.addWidget(self.send_button)

    self.payment_button = QPushButton("Check Payments")
    self.payment_button.clicked.connect(self._handle_check_payments)
    buttons_layout.addWidget(self.payment_button)
    main_layout.addLayout(buttons_layout)

    self.log_view = QPlainTextEdit()
    self.log_view.setReadOnly(True)
    self.log_view.setMaximumBlockCount(1000)
    main_layout.addWidget(QLabel("Activity Log:"))
    main_layout.addWidget(self.log_view, stretch=1)

    central.setLayout(main_layout)

  def _load_default_excel_path(self) -> None:
    default_path = CONFIG.get("excel_path", "")
    self.excel_path_edit.setText(default_path)

  def _browse_excel(self) -> None:
    path, _ = QFileDialog.getOpenFileName(self, "Select invoices Excel file", "", "Excel Files (*.xlsx)")
    if path:
      self.excel_path_edit.setText(path)

  def _get_excel_path(self) -> Optional[str]:
    path_text = self.excel_path_edit.text().strip()
    if not path_text:
      path_text = CONFIG.get("excel_path", "")
    if not path_text:
      QMessageBox.warning(self, "Excel Path", "Please specify the invoices Excel file path.")
      return None
    resolved = Path(path_text)
    if not resolved.is_absolute():
      resolved = project_path(resolved, writable=True)
    if not resolved.exists():
      QMessageBox.warning(self, "Excel Path", f"Excel file not found: {resolved}")
      return None
    return str(resolved)

  def _handle_login(self) -> None:
    self._run_async_task(self._perform_login, "Opening WhatsApp Web for login…")

  def _handle_send_invoices(self) -> None:
    excel_path = self._get_excel_path()
    if excel_path:
      self._run_async_task(self._process_pending_invoices, f"Processing invoices from {excel_path}", excel_path)

  def _handle_check_payments(self) -> None:
    excel_path = self._get_excel_path()
    if excel_path:
      self._run_async_task(self._check_payments, "Checking payment confirmations…", excel_path)

  def _run_async_task(self, fn: Callable, start_message: str, *args) -> None:
    self._set_buttons_enabled(False)
    self.append_status(start_message)
    worker = Worker(fn, *args)
    worker.signals.log.connect(self.append_status)
    worker.signals.error.connect(lambda msg: self.append_status(f"Error: {msg}"))
    worker.signals.finished.connect(lambda: self._set_buttons_enabled(True))
    self.thread_pool.start(worker)

  def _set_buttons_enabled(self, enabled: bool) -> None:
    self.login_button.setEnabled(enabled)
    self.send_button.setEnabled(enabled)
    self.payment_button.setEnabled(enabled)

  def append_status(self, message: str) -> None:
    self.log_view.appendPlainText(message)
    self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())

  def _perform_login(self, status_callback: Callable[[str], None]) -> None:
    status_callback("Waiting for WhatsApp login (scan QR if prompted)…")
    self.whatsapp_client.login()
    status_callback("WhatsApp ready.")

  def _process_pending_invoices(self, excel_path: str, status_callback: Callable[[str], None]) -> None:
    invoices = load_invoices(excel_path)
    pending = [row for row in invoices if str(row.get("Status") or "").lower() != "sent"]
    if not pending:
      status_callback("No pending invoices found.")
      return

    status_callback(f"Found {len(pending)} pending invoices.")
    for invoice in pending:
      invoice_no = invoice["InvoiceNo"]
      phone_number = self._normalize_phone(invoice.get("PhoneNumber"))
      if not phone_number:
        status_callback(f"Skipping {invoice_no}: invalid phone number.")
        continue

      payload = self._prepare_invoice_payload(invoice)
      status_callback(f"Generating invoice PDF for {invoice_no}…")
      pdf_path = generate_invoice_pdf(payload)

      message = build_message(payload)
      status_callback(f"Sending WhatsApp message for {invoice_no} to {phone_number}…")
      sent = self.whatsapp_client.send_message_with_attachment(phone_number, message, pdf_path)
      if sent:
        update_status(excel_path, invoice_no, "Sent")
        status_callback(f"Invoice {invoice_no} sent successfully.")
      else:
        update_status(excel_path, invoice_no, "Error:SendFailed")
        status_callback(f"Failed to send invoice {invoice_no}.")

  def _check_payments(self, excel_path: str, status_callback: Callable[[str], None]) -> None:
    invoices = load_invoices(excel_path)
    awaiting = [
        row for row in invoices
        if str(row.get("Status") or "").lower() == "sent"
        and not str(row.get("PaymentReceived") or "").strip()
    ]
    if not awaiting:
      status_callback("No sent invoices awaiting payment confirmation.")
      return

    status_callback(f"Checking payments for {len(awaiting)} invoices.")
    for invoice in awaiting:
      invoice_no = invoice["InvoiceNo"]
      phone_number = self._normalize_phone(invoice.get("PhoneNumber"))
      if not phone_number:
        status_callback(f"Skipping payment check for {invoice_no}: invalid phone.")
        continue

      timestamp = self.payment_checker.check_payment_for_invoice(phone_number)
      if timestamp:
        update_payment_received(excel_path, invoice_no, timestamp)
        status_callback(f"Payment confirmed for {invoice_no} at {timestamp}.")
      else:
        status_callback(f"No payment confirmation found for {invoice_no}.")

  @staticmethod
  def _prepare_invoice_payload(invoice: dict) -> dict:
    payload = dict(invoice)
    payload["InvoiceDate"] = MainWindow._format_date(invoice.get("InvoiceDate"))
    payload["Amount"] = MainWindow._format_amount(invoice.get("Amount"))
    payload["CustomerName"] = (invoice.get("CustomerName") or "").strip()
    return payload

  @staticmethod
  def _format_date(value) -> str:
    if isinstance(value, datetime):
      return value.strftime("%d-%m-%Y")
    if isinstance(value, date):
      return value.strftime("%d-%m-%Y")
    return str(value or "")

  @staticmethod
  def _format_amount(value) -> str:
    try:
      return f"{float(value):.2f}"
    except (TypeError, ValueError):
      return str(value or "0.00")

  @staticmethod
  def _normalize_phone(value) -> Optional[str]:
    if value is None:
      return None
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return digits or None

  def closeEvent(self, event) -> None:  # noqa: N802
    self.whatsapp_client.close()
    super().closeEvent(event)
