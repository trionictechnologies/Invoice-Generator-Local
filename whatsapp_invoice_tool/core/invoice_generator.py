"""
Render invoice HTML templates and export to PDF.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import load_config, project_path
from .logger import get_logger


logger = get_logger(__name__)
CONFIG = load_config()
INVOICE_CFG = CONFIG.get("invoice", {})
COMPANY_INFO = CONFIG.get("company", {})


def _build_environment(template_path: Path) -> Environment:
  return Environment(
      loader=FileSystemLoader(template_path.parent),
      autoescape=select_autoescape(["html", "xml"]),
  )


def _pdfkit_config() -> Optional[pdfkit.configuration]:
  binary_path = INVOICE_CFG.get("wkhtmltopdf_binary")
  if binary_path:
    return pdfkit.configuration(wkhtmltopdf=project_path(binary_path))
  return None


def generate_invoice_pdf(invoice_data: Dict[str, Any], output_dir: Optional[str] = None) -> Path:
  """
  Render the invoice HTML template using invoice_data and company info,
  then export it to PDF. Returns the absolute path to the generated PDF.
  """
  template_path = project_path(INVOICE_CFG.get("template_path", "templates/invoice.html"))
  output_directory = project_path(output_dir or INVOICE_CFG.get("output_dir", "invoices_output"), writable=True)
  output_directory.mkdir(parents=True, exist_ok=True)

  env = _build_environment(template_path)
  template = env.get_template(template_path.name)

  payload = {
      **invoice_data,
      "company": COMPANY_INFO,
      "currency_symbol": INVOICE_CFG.get("currency_symbol", "₹"),
  }
  rendered_html = template.render(**payload)

  pdf_path = output_directory / f"{invoice_data['InvoiceNo']}.pdf"
  try:
    pdfkit.from_string(
        rendered_html,
        str(pdf_path),
        options={"enable-local-file-access": ""},
        configuration=_pdfkit_config(),
    )
  except OSError as exc:
    logger.error("Failed to generate PDF for %s: %s", invoice_data["InvoiceNo"], exc)
    raise

  logger.info("Generated invoice PDF at %s", pdf_path)
  return pdf_path
