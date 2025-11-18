"""
Simple logging utility for the WhatsApp Invoice Tool.
Logs to both file and console for debugging sends and errors.
"""
import logging
import os
from datetime import datetime
from pathlib import Path


class AppLogger:
    """Application logger that writes to file and optionally to console."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        
        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        log_file = log_dir / "app.log"
        
        # Configure logger
        self.logger = logging.getLogger("WhatsAppInvoiceTool")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info level message."""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log error level message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug level message."""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log warning level message."""
        self.logger.warning(message)


# Global logger instance
logger = AppLogger()
