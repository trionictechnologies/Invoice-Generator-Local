"""
WhatsApp Client for WhatsApp Invoice Tool.
Automates WhatsApp Web using Playwright for sending invoices and messages.
"""
import time
from pathlib import Path
from typing import Optional, Tuple
from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeout
from .logger import logger


class WhatsAppClient:
    """
    WhatsApp Web automation client using Playwright.
    Handles login, sending messages with attachments, and reading messages.
    """
    
    # WhatsApp Web selectors (may need updates if WhatsApp changes)
    SELECTORS = {
        # Login and main UI
        "qr_code": "canvas[aria-label='Scan this QR code to link a device!'], canvas[aria-label='Scan me!']",
        "main_chat_list": "div[aria-label='Chat list']",
        "search_box": "div[contenteditable='true'][data-tab='3']",
        
        # Chat window
        "message_input": "div[contenteditable='true'][data-tab='10']",
        "attach_button": "div[title='Attach'], span[data-icon='plus'], span[data-icon='clip']",
        "document_input": "input[accept*='document'], input[type='file']",
        "send_button": "span[data-icon='send']",
        
        # Message elements
        "message_out": "div[class*='message-out']",
        "message_in": "div[class*='message-in']",
        
        # Error indicators
        "error_icon": "span[data-icon='msg-time'], span[data-icon='msg-check']"
    }
    
    def __init__(self, profile_dir: Optional[str] = None, headless: bool = False, config: Optional[dict] = None):
        """
        Initialize WhatsApp Client.
        
        Args:
            profile_dir: Directory to store browser profile (for session persistence)
            headless: Whether to run browser in headless mode
            config: Optional configuration dictionary
        """
        # Set profile directory
        if profile_dir:
            self.profile_dir = Path(profile_dir)
        else:
            self.profile_dir = Path(__file__).parent.parent / "playwright_profile"
        
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        
        self.headless = headless
        self.config = config or {}
        
        # Playwright objects
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # Delays (in seconds)
        self.send_delay = self.config.get("send_delay", 3)
        self.page_load_timeout = self.config.get("page_load_timeout", 60000)  # 60 seconds
        
        logger.info("WhatsApp Client initialized")
    
    def start_browser(self):
        """Start Playwright browser with persistent context."""
        try:
            self.playwright = sync_playwright().start()
            
            # Launch browser with persistent context for session storage
            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ],
                viewport={'width': 1280, 'height': 720}
            )
            
            # Get the first page
            if len(self.browser.pages) > 0:
                self.page = self.browser.pages[0]
            else:
                self.page = self.browser.new_page()
            
            # Set default timeout
            self.page.set_default_timeout(self.page_load_timeout)
            
            logger.info("Browser started successfully")
            
        except Exception as e:
            logger.error(f"Error starting browser: {str(e)}")
            raise
    
    def login(self) -> bool:
        """
        Open WhatsApp Web and wait for user to scan QR code.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.browser or not self.page:
                self.start_browser()
            
            logger.info("Navigating to WhatsApp Web...")
            self.page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
            
            # Check if already logged in
            try:
                self.page.wait_for_selector(self.SELECTORS["main_chat_list"], timeout=5000)
                logger.info("Already logged in to WhatsApp Web")
                return True
            except PlaywrightTimeout:
                pass
            
            # Wait for QR code to appear
            logger.info("Waiting for QR code to appear...")
            try:
                self.page.wait_for_selector(self.SELECTORS["qr_code"], timeout=10000)
                logger.info("QR code displayed. Please scan with your phone.")
            except PlaywrightTimeout:
                logger.warning("QR code not found - may already be logged in or page structure changed")
            
            # Wait for chat list to appear (indicates successful login)
            logger.info("Waiting for login confirmation...")
            self.page.wait_for_selector(self.SELECTORS["main_chat_list"], timeout=120000)  # 2 minutes
            
            logger.info("Successfully logged in to WhatsApp Web")
            time.sleep(3)  # Wait for full page load
            return True
            
        except Exception as e:
            logger.error(f"Error during WhatsApp login: {str(e)}")
            return False
    
    def open_chat(self, phone_number: str) -> bool:
        """
        Open chat with a specific phone number.
        
        Args:
            phone_number: Phone number in format 91XXXXXXXXXX (country code + number)
            
        Returns:
            True if chat opened successfully, False otherwise
        """
        try:
            # Navigate to wa.me link to open chat
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            logger.info(f"Opening chat for {phone_number}")
            
            self.page.goto(url, wait_until="domcontentloaded")
            
            # Wait for message input to appear (indicates chat is loaded)
            self.page.wait_for_selector(self.SELECTORS["message_input"], timeout=15000)
            
            time.sleep(2)  # Wait for full chat load
            logger.info(f"Chat opened for {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error opening chat for {phone_number}: {str(e)}")
            return False
    
    def send_message_with_attachment(self, phone_number: str, message: str, file_path: str) -> Tuple[bool, str]:
        """
        Send a message with file attachment to a phone number.
        
        Args:
            phone_number: Phone number in format 91XXXXXXXXXX
            message: Message text to send
            file_path: Path to file to attach
            
        Returns:
            Tuple of (success: bool, error_message: str or empty)
        """
        try:
            # Open chat
            if not self.open_chat(phone_number):
                return False, "Failed to open chat"
            
            # Verify file exists
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return False, f"File not found: {file_path}"
            
            # Find and click attach button
            try:
                attach_button = self.page.wait_for_selector(self.SELECTORS["attach_button"], timeout=5000)
                attach_button.click()
                time.sleep(1)
            except PlaywrightTimeout:
                logger.error("Attach button not found")
                return False, "Attach button not found"
            
            # Upload file using file input
            try:
                # Look for file input element
                file_input = self.page.locator("input[type='file']").first
                file_input.set_input_files(str(file_path_obj.absolute()))
                time.sleep(2)  # Wait for file to upload
            except Exception as e:
                logger.error(f"Error uploading file: {str(e)}")
                return False, f"File upload failed: {str(e)}"
            
            # Type message in caption box (if visible)
            try:
                # Look for caption input or message input
                caption_input = self.page.locator("div[contenteditable='true'][data-tab='10']").first
                caption_input.click()
                caption_input.fill(message)
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Could not add caption: {str(e)}")
            
            # Click send button
            try:
                send_button = self.page.wait_for_selector(self.SELECTORS["send_button"], timeout=5000)
                send_button.click()
                logger.info(f"Message with attachment sent to {phone_number}")
            except PlaywrightTimeout:
                return False, "Send button not found"
            
            # Wait to confirm message was sent
            time.sleep(self.send_delay)
            
            # Check for error indicators
            try:
                error_elements = self.page.locator("span[data-icon='msg-time']").all()
                if len(error_elements) > 0:
                    logger.warning("Possible error in message delivery")
            except:
                pass
            
            return True, ""
            
        except Exception as e:
            error_msg = f"Error sending message: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_recent_messages(self, phone_number: str, count: int = 5) -> list:
        """
        Get recent incoming messages from a chat.
        
        Args:
            phone_number: Phone number in format 91XXXXXXXXXX
            count: Number of recent messages to retrieve
            
        Returns:
            List of message texts (incoming only)
        """
        try:
            # Open chat
            if not self.open_chat(phone_number):
                return []
            
            time.sleep(2)  # Wait for messages to load
            
            # Find incoming message elements
            messages = []
            try:
                # Get all message containers
                message_elements = self.page.locator("div.message-in").all()
                
                # Get last N incoming messages
                recent_messages = message_elements[-count:] if len(message_elements) > count else message_elements
                
                for msg_element in recent_messages:
                    try:
                        # Extract text content
                        text_content = msg_element.locator("span.selectable-text").first.inner_text()
                        if text_content:
                            messages.append(text_content.strip())
                    except:
                        continue
                
                logger.info(f"Retrieved {len(messages)} recent messages from {phone_number}")
                
            except Exception as e:
                logger.warning(f"Error retrieving messages: {str(e)}")
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting recent messages for {phone_number}: {str(e)}")
            return []
    
    def close(self):
        """Close browser and cleanup."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")
