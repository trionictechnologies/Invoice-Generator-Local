"""
Utility to scan WhatsApp chats for payment confirmations.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .config import load_config
from .logger import get_logger
from .whatsapp_client import WhatsAppClient


logger = get_logger(__name__)
CONFIG = load_config()
PAYMENT_KEYWORDS = [kw.lower() for kw in CONFIG.get("payment_keywords", [])]


class PaymentChecker:
  def __init__(self, client: WhatsAppClient):
    self.client = client

  def _extract_recent_messages(self, limit: int = 5) -> List[str]:
    page = self.client.page
    locator = page.locator("div.message-in span.selectable-text")
    count = locator.count()
    start = max(count - limit, 0)
    messages = []
    for idx in range(start, count):
      try:
        text = locator.nth(idx).inner_text(timeout=2000)
        messages.append(text.strip())
      except PlaywrightTimeoutError:
        continue
    return messages

  def check_payment_for_invoice(self, phone_number: str, limit: int = 5) -> Optional[str]:
    """
    Return an ISO timestamp string if a payment keyword is detected
    in the last `limit` incoming messages. Otherwise return None.
    """
    try:
      self.client.open_chat(phone_number)
      recent_messages = self._extract_recent_messages(limit=limit)
      for message in reversed(recent_messages):
        lower_msg = message.lower()
        if any(keyword in lower_msg for keyword in PAYMENT_KEYWORDS):
          timestamp = datetime.now().isoformat(timespec="seconds")
          logger.info("Payment keywords detected for %s: '%s'", phone_number, message)
          return timestamp
      return None
    except PlaywrightTimeoutError as exc:
      logger.error("Timeout while checking payments for %s: %s", phone_number, exc)
      return None
