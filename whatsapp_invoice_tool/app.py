"""
WhatsApp Invoice Automation Tool
Main entry point for the application.

This tool automates:
- Invoice PDF generation from Excel data
- Sending invoices via WhatsApp Web
- Payment confirmation tracking

Author: Created for Indian SMEs/Accounting Firms
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logger import logger


def main():
    """Main application entry point."""
    try:
        logger.info("=" * 60)
        logger.info("WhatsApp Invoice Automation Tool - Starting")
        logger.info("=" * 60)
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("WhatsApp Invoice Tool")
        app.setOrganizationName("Invoice Automation")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application window displayed")
        
        # Start event loop
        exit_code = app.exec()
        
        logger.info("Application shutting down")
        return exit_code
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
