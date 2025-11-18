"""
Main Window for WhatsApp Invoice Tool.
PySide6 GUI for managing invoice generation and WhatsApp automation.
"""
import json
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTextEdit, QFileDialog, QMessageBox,
    QProgressBar, QGroupBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from datetime import datetime

from ..core.logger import logger
from ..core.excel_manager import ExcelManager
from ..core.invoice_generator import InvoiceGenerator
from ..core.whatsapp_client import WhatsAppClient
from ..core.payment_checker import PaymentChecker


class WorkerThread(QThread):
    """Worker thread for long-running tasks."""
    progress = Signal(str)
    finished = Signal(bool, str)
    
    def __init__(self, task_type: str, *args, **kwargs):
        super().__init__()
        self.task_type = task_type
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Run the task."""
        try:
            if self.task_type == "login":
                self.login_task()
            elif self.task_type == "send_invoices":
                self.send_invoices_task()
            elif self.task_type == "check_payments":
                self.check_payments_task()
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def login_task(self):
        """WhatsApp login task."""
        whatsapp_client = self.kwargs.get("whatsapp_client")
        self.progress.emit("Opening WhatsApp Web...")
        success = whatsapp_client.login()
        if success:
            self.finished.emit(True, "Successfully logged in to WhatsApp Web")
        else:
            self.finished.emit(False, "Failed to login to WhatsApp Web")
    
    def send_invoices_task(self):
        """Send pending invoices task."""
        excel_manager = self.kwargs.get("excel_manager")
        invoice_generator = self.kwargs.get("invoice_generator")
        whatsapp_client = self.kwargs.get("whatsapp_client")
        config = self.kwargs.get("config")
        output_dir = self.kwargs.get("output_dir")
        
        # Load invoices
        self.progress.emit("Loading invoices from Excel...")
        invoices = excel_manager.load_invoices()
        
        # Filter pending invoices
        pending = [inv for inv in invoices if inv.get("Status") != "Sent"]
        
        if not pending:
            self.finished.emit(True, "No pending invoices to send")
            return
        
        self.progress.emit(f"Found {len(pending)} pending invoices")
        
        # Process each invoice
        success_count = 0
        error_count = 0
        
        message_template = config.get("message_template", 
            "Dear {CustomerName}, please find your invoice {InvoiceNo} dated {InvoiceDate} for ₹{Amount} attached. - {FirmName}")
        firm_name = config.get("company_info", {}).get("CompanyName", "Our Firm")
        
        for i, invoice in enumerate(pending, 1):
            invoice_no = invoice["InvoiceNo"]
            self.progress.emit(f"[{i}/{len(pending)}] Processing invoice {invoice_no}...")
            
            try:
                # Generate PDF
                self.progress.emit(f"Generating PDF for {invoice_no}...")
                pdf_path = invoice_generator.generate_invoice_pdf(invoice, output_dir)
                
                # Prepare message
                message = message_template.format(
                    CustomerName=invoice["CustomerName"],
                    InvoiceNo=invoice["InvoiceNo"],
                    InvoiceDate=invoice["InvoiceDate"],
                    Amount=f"{invoice['Amount']:,.2f}",
                    FirmName=firm_name
                )
                
                # Send via WhatsApp
                self.progress.emit(f"Sending {invoice_no} to {invoice['PhoneNumber']}...")
                success, error_msg = whatsapp_client.send_message_with_attachment(
                    invoice["PhoneNumber"],
                    message,
                    pdf_path
                )
                
                # Update Excel
                if success:
                    excel_manager.update_status(invoice_no, "Sent")
                    self.progress.emit(f"✓ Successfully sent {invoice_no}")
                    success_count += 1
                else:
                    error_status = f"Error: {error_msg[:50]}"
                    excel_manager.update_status(invoice_no, error_status)
                    self.progress.emit(f"✗ Failed to send {invoice_no}: {error_msg}")
                    error_count += 1
                    
            except Exception as e:
                error_msg = str(e)
                excel_manager.update_status(invoice_no, f"Error: {error_msg[:50]}")
                self.progress.emit(f"✗ Error processing {invoice_no}: {error_msg}")
                error_count += 1
        
        summary = f"Completed! Sent: {success_count}, Failed: {error_count}"
        self.finished.emit(True, summary)
    
    def check_payments_task(self):
        """Check payment status task."""
        excel_manager = self.kwargs.get("excel_manager")
        payment_checker = self.kwargs.get("payment_checker")
        
        # Load invoices
        self.progress.emit("Loading invoices from Excel...")
        invoices = excel_manager.load_invoices()
        
        # Filter sent invoices without payment confirmation
        to_check = [inv for inv in invoices 
                   if inv.get("Status") == "Sent" and not inv.get("PaymentReceived")]
        
        if not to_check:
            self.finished.emit(True, "No invoices to check for payment")
            return
        
        self.progress.emit(f"Checking {len(to_check)} invoices for payment...")
        
        # Check payments
        found_count = 0
        for i, invoice in enumerate(to_check, 1):
            invoice_no = invoice["InvoiceNo"]
            self.progress.emit(f"[{i}/{len(to_check)}] Checking {invoice_no}...")
            
            timestamp = payment_checker.check_payment_for_invoice(invoice["PhoneNumber"])
            if timestamp:
                excel_manager.update_payment_received(invoice_no, timestamp)
                self.progress.emit(f"✓ Payment confirmed for {invoice_no}")
                found_count += 1
        
        summary = f"Completed! Found {found_count} payment confirmations"
        self.finished.emit(True, summary)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Load config
        self.config = self.load_config()
        
        # Initialize components (will be created when needed)
        self.excel_manager = None
        self.invoice_generator = None
        self.whatsapp_client = None
        self.payment_checker = None
        
        # Worker thread
        self.worker = None
        
        # UI setup
        self.init_ui()
        
        logger.info("Main window initialized")
    
    def load_config(self) -> dict:
        """Load configuration from config.json."""
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("WhatsApp Invoice Automation Tool")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("WhatsApp Invoice Automation")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Excel file selection
        excel_group = QGroupBox("Excel File")
        excel_layout = QHBoxLayout()
        excel_group.setLayout(excel_layout)
        
        self.excel_path_input = QLineEdit()
        self.excel_path_input.setPlaceholderText("Select Excel file with invoice data...")
        default_path = self.config.get("default_excel_path", "")
        if default_path:
            self.excel_path_input.setText(default_path)
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_excel_file)
        
        excel_layout.addWidget(self.excel_path_input)
        excel_layout.addWidget(browse_button)
        layout.addWidget(excel_group)
        
        # Action buttons
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        actions_group.setLayout(actions_layout)
        
        self.login_button = QPushButton("1. Login to WhatsApp")
        self.login_button.clicked.connect(self.login_whatsapp)
        actions_layout.addWidget(self.login_button)
        
        self.send_button = QPushButton("2. Generate & Send Pending Invoices")
        self.send_button.clicked.connect(self.send_invoices)
        actions_layout.addWidget(self.send_button)
        
        self.check_button = QPushButton("3. Check Payment Status")
        self.check_button.clicked.connect(self.check_payments)
        actions_layout.addWidget(self.check_button)
        
        layout.addWidget(actions_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Log output
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(300)
        log_layout.addWidget(self.log_output)
        
        clear_log_button = QPushButton("Clear Log")
        clear_log_button.clicked.connect(self.log_output.clear)
        log_layout.addWidget(clear_log_button)
        
        layout.addWidget(log_group)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def browse_excel_file(self):
        """Open file dialog to select Excel file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.excel_path_input.setText(file_path)
            self.log_message(f"Selected file: {file_path}")
    
    def log_message(self, message: str):
        """Add message to log output."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")
        logger.info(message)
    
    def show_error(self, message: str):
        """Show error dialog."""
        QMessageBox.critical(self, "Error", message)
    
    def show_info(self, message: str):
        """Show info dialog."""
        QMessageBox.information(self, "Information", message)
    
    def validate_excel_file(self) -> bool:
        """Validate that Excel file is selected and exists."""
        excel_path = self.excel_path_input.text()
        if not excel_path:
            self.show_error("Please select an Excel file first")
            return False
        if not Path(excel_path).exists():
            self.show_error("Excel file not found")
            return False
        return True
    
    def initialize_components(self):
        """Initialize core components."""
        if not self.validate_excel_file():
            return False
        
        try:
            excel_path = self.excel_path_input.text()
            
            # Initialize Excel Manager
            if not self.excel_manager or self.excel_manager.file_path != Path(excel_path):
                self.excel_manager = ExcelManager(excel_path, self.config)
            
            # Initialize Invoice Generator
            if not self.invoice_generator:
                self.invoice_generator = InvoiceGenerator(config=self.config)
            
            # Initialize WhatsApp Client
            if not self.whatsapp_client:
                profile_dir = str(Path(__file__).parent.parent / "playwright_profile")
                self.whatsapp_client = WhatsAppClient(profile_dir=profile_dir, config=self.config)
            
            # Initialize Payment Checker
            if not self.payment_checker and self.whatsapp_client:
                self.payment_checker = PaymentChecker(self.whatsapp_client, self.config)
            
            return True
            
        except Exception as e:
            self.show_error(f"Error initializing components: {str(e)}")
            return False
    
    def disable_buttons(self):
        """Disable all action buttons."""
        self.login_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.check_button.setEnabled(False)
    
    def enable_buttons(self):
        """Enable all action buttons."""
        self.login_button.setEnabled(True)
        self.send_button.setEnabled(True)
        self.check_button.setEnabled(True)
    
    def login_whatsapp(self):
        """Login to WhatsApp Web."""
        if not self.initialize_components():
            return
        
        self.log_message("Starting WhatsApp login...")
        self.disable_buttons()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Start worker thread
        self.worker = WorkerThread("login", whatsapp_client=self.whatsapp_client)
        self.worker.progress.connect(self.log_message)
        self.worker.finished.connect(self.on_login_finished)
        self.worker.start()
    
    def on_login_finished(self, success: bool, message: str):
        """Handle login completion."""
        self.enable_buttons()
        self.progress_bar.setVisible(False)
        self.log_message(message)
        
        if success:
            self.show_info(message)
        else:
            self.show_error(message)
    
    def send_invoices(self):
        """Generate and send pending invoices."""
        if not self.initialize_components():
            return
        
        if not self.whatsapp_client:
            self.show_error("Please login to WhatsApp first")
            return
        
        self.log_message("Starting invoice generation and sending...")
        self.disable_buttons()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # Get output directory
        output_dir = str(Path(__file__).parent.parent / "invoices_output")
        
        # Start worker thread
        self.worker = WorkerThread(
            "send_invoices",
            excel_manager=self.excel_manager,
            invoice_generator=self.invoice_generator,
            whatsapp_client=self.whatsapp_client,
            config=self.config,
            output_dir=output_dir
        )
        self.worker.progress.connect(self.log_message)
        self.worker.finished.connect(self.on_send_finished)
        self.worker.start()
    
    def on_send_finished(self, success: bool, message: str):
        """Handle sending completion."""
        self.enable_buttons()
        self.progress_bar.setVisible(False)
        self.log_message(message)
        
        if success:
            self.show_info(message)
        else:
            self.show_error(message)
    
    def check_payments(self):
        """Check payment status for sent invoices."""
        if not self.initialize_components():
            return
        
        if not self.whatsapp_client:
            self.show_error("Please login to WhatsApp first")
            return
        
        self.log_message("Starting payment status check...")
        self.disable_buttons()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # Start worker thread
        self.worker = WorkerThread(
            "check_payments",
            excel_manager=self.excel_manager,
            payment_checker=self.payment_checker
        )
        self.worker.progress.connect(self.log_message)
        self.worker.finished.connect(self.on_check_finished)
        self.worker.start()
    
    def on_check_finished(self, success: bool, message: str):
        """Handle payment check completion."""
        self.enable_buttons()
        self.progress_bar.setVisible(False)
        self.log_message(message)
        
        if success:
            self.show_info(message)
        else:
            self.show_error(message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Close WhatsApp client if open
        if self.whatsapp_client:
            self.log_message("Closing WhatsApp client...")
            try:
                self.whatsapp_client.close()
            except:
                pass
        
        event.accept()
