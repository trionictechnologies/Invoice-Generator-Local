"""
Playwright-based automation for WhatsApp Web.
"""

from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Optional

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page, sync_playwright

from .config import load_config, project_path
from .logger import get_logger


logger = get_logger(__name__)
CONFIG = load_config()
WHATSAPP_CFG = CONFIG.get("whatsapp", {})
MESSAGE_TEMPLATE = CONFIG.get("message_template", "")


class WhatsAppClient:
  """Thin wrapper around Playwright to interact with WhatsApp Web."""

  def __init__(self) -> None:
    self._playwright = None
    self._context = None
    self._page: Optional[Page] = None

  def _start(self) -> None:
    if self._playwright:
      return
    user_data_dir = project_path(WHATSAPP_CFG.get("user_data_dir", "playwright_profile"), writable=True)
    user_data_dir.mkdir(parents=True, exist_ok=True)
    self._playwright = sync_playwright().start()
    self._context = self._playwright.chromium.launch_persistent_context(
        user_data_dir=str(user_data_dir),
        headless=False,
        viewport={"width": 1280, "height": 900},
    )
    self._page = self._context.pages[0] if self._context.pages else self._context.new_page()
    logger.debug("Playwright context initialized with profile at %s", user_data_dir)

  @property
  def page(self) -> Page:
    if not self._page:
      self._start()
    return self._page  # type: ignore[return-value]

  def close(self) -> None:
    if self._context:
      self._context.close()
    if self._playwright:
      self._playwright.stop()
    self._context = None
    self._playwright = None
    self._page = None
    logger.info("Playwright session closed")

  def login(self) -> None:
    """Open WhatsApp Web and wait for the main UI to load (after QR scan)."""
    page = self.page
    page.goto("https://web.whatsapp.com", wait_until="networkidle")
    try:
      page.wait_for_selector(
          WHATSAPP_CFG.get("message_input_selector", "div[contenteditable='true']"),
          timeout=WHATSAPP_CFG.get("navigation_timeout_ms", 45000),
      )
      logger.info("WhatsApp login successful or already authenticated.")
    except PlaywrightTimeoutError:
      logger.warning("Timed out waiting for WhatsApp login UI.")
      raise

  def open_chat(self, phone_number: str) -> None:
    """Navigate directly to a chat by phone number."""
    page = self.page
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text&app_absent=0"
    page.goto(url, wait_until="domcontentloaded")
    try:
      page.wait_for_selector(
          WHATSAPP_CFG.get("message_input_selector", "div[contenteditable='true']"),
          timeout=WHATSAPP_CFG.get("navigation_timeout_ms", 45000),
      )
      logger.debug("Chat ready for %s", phone_number)
    except PlaywrightTimeoutError:
      logger.error("Failed to open chat for %s", phone_number)
      raise

  def _random_delay(self) -> None:
    delay_cfg = WHATSAPP_CFG.get("send_delay_seconds", {"min": 2, "max": 4})
    delay = random.uniform(delay_cfg.get("min", 2), delay_cfg.get("max", 4))
    time.sleep(delay)

  def send_message_with_attachment(self, phone_number: str, message: str, file_path: Path) -> bool:
    """
    Send a message with a PDF attachment to the specified phone number.
    Returns True on success, False on failure.
    """
    try:
      self.open_chat(phone_number)
      page = self.page
      message_box_selector = WHATSAPP_CFG.get("message_input_selector", "div[contenteditable='true']")
      attach_button_selector = WHATSAPP_CFG.get("attach_button_selector", "span[data-icon='clip']")
      document_input_selector = WHATSAPP_CFG.get("document_input_selector", "input[type='file']")
      send_button_selector = WHATSAPP_CFG.get("send_button_selector", "span[data-icon='send']")

      message_box = page.wait_for_selector(message_box_selector, timeout=10000)
      message_box.click()
      message_box.fill("")
      message_box.type(message, delay=25)

      page.click(attach_button_selector)
      file_input = page.wait_for_selector(document_input_selector, timeout=5000)
      file_input.set_input_files(str(file_path))

      page.wait_for_timeout(1500)
      page.click(send_button_selector)

      self._random_delay()
      logger.info("Sent WhatsApp message to %s with attachment %s", phone_number, file_path.name)
      return True
    except PlaywrightTimeoutError as exc:
      logger.error("Timeout while sending message to %s: %s", phone_number, exc)
    except Exception as exc:
      logger.exception("Unexpected error sending message to %s: %s", phone_number, exc)
    return False


def build_message(invoice_row: dict) -> str:
  """Render the configured message template using invoice row data."""
  try:
    from jinja2 import Template

    template = Template(MESSAGE_TEMPLATE)
    return template.render(**invoice_row, company=CONFIG.get("company", {}))
  except Exception as exc:
    logger.error("Failed to render message template: %s", exc)
    raise
