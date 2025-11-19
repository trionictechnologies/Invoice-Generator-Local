"""
Payment Checker for WhatsApp Invoice Tool.
Detects payment confirmation messages in WhatsApp chats.
"""
import re
from datetime import datetime
from typing import Optional, List
from .logger import logger
from .whatsapp_client import WhatsAppClient


class PaymentChecker:
    """
    Checks WhatsApp chats for payment confirmation messages.
    """
    
    # Payment keywords (case-insensitive)
    DEFAULT_KEYWORDS = [
        "paid",
        "payment done",
        "payment completed",
        "sent",
        "done",
        "upi",
        "imps",
        "rtgs",
        "neft",
        "transferred",
        "transaction",
        "successful",
        "credited"
    ]
    
    def __init__(self, whatsapp_client: WhatsAppClient, config: Optional[dict] = None):
        """
        Initialize Payment Checker.
        
        Args:
            whatsapp_client: Instance of WhatsAppClient
            config: Optional configuration dictionary
        """
        self.whatsapp_client = whatsapp_client
        self.config = config or {}
        
        # Load keywords from config or use defaults
        self.keywords = self.config.get("payment_keywords", self.DEFAULT_KEYWORDS)
        
        # Make keywords lowercase for case-insensitive matching
        self.keywords = [kw.lower() for kw in self.keywords]
        
        # Number of recent messages to check
        self.message_count = self.config.get("messages_to_check", 5)
        
        logger.info(f"Payment Checker initialized with {len(self.keywords)} keywords")
    
    def check_payment_for_invoice(self, phone_number: str) -> Optional[str]:
        """
        Check if payment confirmation message exists for a given phone number.
        
        Args:
            phone_number: Phone number to check messages from
            
        Returns:
            Timestamp string if payment found, None otherwise
        """
        try:
            logger.info(f"Checking payment status for {phone_number}")
            
            # Get recent messages from chat
            messages = self.whatsapp_client.get_recent_messages(phone_number, self.message_count)
            
            if not messages:
                logger.info(f"No messages found for {phone_number}")
                return None
            
            # Check each message for payment keywords
            for message in messages:
                if self._contains_payment_keyword(message):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Payment confirmation found for {phone_number}: '{message}'")
                    return timestamp
            
            logger.info(f"No payment confirmation found for {phone_number}")
            return None
            
        except Exception as e:
            logger.error(f"Error checking payment for {phone_number}: {str(e)}")
            return None
    
    def check_multiple_invoices(self, invoices: List[dict]) -> dict:
        """
        Check payment status for multiple invoices.
        
        Args:
            invoices: List of invoice dictionaries with PhoneNumber and InvoiceNo
            
        Returns:
            Dictionary mapping invoice numbers to timestamps (for paid invoices only)
        """
        results = {}
        
        for invoice in invoices:
            invoice_no = invoice.get("InvoiceNo")
            phone_number = invoice.get("PhoneNumber")
            
            if not phone_number:
                logger.warning(f"No phone number for invoice {invoice_no}")
                continue
            
            # Only check if payment not already received
            if invoice.get("PaymentReceived"):
                logger.info(f"Invoice {invoice_no} already marked as paid")
                continue
            
            # Check for payment
            timestamp = self.check_payment_for_invoice(phone_number)
            if timestamp:
                results[invoice_no] = timestamp
        
        logger.info(f"Found payment confirmations for {len(results)} invoices")
        return results
    
    def _contains_payment_keyword(self, message: str) -> bool:
        """
        Check if a message contains any payment-related keywords.
        
        Args:
            message: Message text to check
            
        Returns:
            True if payment keyword found, False otherwise
        """
        if not message:
            return False
        
        # Convert to lowercase for case-insensitive matching
        message_lower = message.lower()
        
        # Check for each keyword
        for keyword in self.keywords:
            # Use word boundaries for more accurate matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, message_lower):
                logger.debug(f"Payment keyword '{keyword}' found in message")
                return True
        
        return False
    
    def add_keyword(self, keyword: str):
        """
        Add a new payment keyword to the list.
        
        Args:
            keyword: Keyword to add
        """
        keyword_lower = keyword.lower()
        if keyword_lower not in self.keywords:
            self.keywords.append(keyword_lower)
            logger.info(f"Added payment keyword: {keyword}")
    
    def remove_keyword(self, keyword: str):
        """
        Remove a payment keyword from the list.
        
        Args:
            keyword: Keyword to remove
        """
        keyword_lower = keyword.lower()
        if keyword_lower in self.keywords:
            self.keywords.remove(keyword_lower)
            logger.info(f"Removed payment keyword: {keyword}")
    
    def get_keywords(self) -> List[str]:
        """
        Get the current list of payment keywords.
        
        Returns:
            List of keywords
        """
        return self.keywords.copy()
