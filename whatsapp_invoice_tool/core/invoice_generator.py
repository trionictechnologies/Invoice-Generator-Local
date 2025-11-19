"""
Invoice Generator for WhatsApp Invoice Tool.
Generates PDF invoices from HTML templates using Jinja2 and pdfkit.
"""
import pdfkit
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, Optional
from .logger import logger


class InvoiceGenerator:
    """Generates PDF invoices from HTML templates."""
    
    def __init__(self, template_dir: Optional[str] = None, config: Optional[Dict] = None):
        """
        Initialize Invoice Generator.
        
        Args:
            template_dir: Path to templates directory (defaults to ../templates)
            config: Optional configuration dict with company info
        """
        # Set template directory
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            # Default to templates directory relative to this file
            self.template_dir = Path(__file__).parent.parent / "templates"
        
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")
        
        # Set up Jinja2 environment
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        
        # Store company config
        self.config = config or {}
        self.company_info = self.config.get("company_info", {})
        
        # Configure pdfkit options
        self.pdfkit_options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
    
    def generate_invoice_pdf(self, invoice_data: Dict, output_dir: str) -> str:
        """
        Generate a PDF invoice for the given invoice data.
        
        Args:
            invoice_data: Dictionary containing invoice details
            output_dir: Directory to save the generated PDF
            
        Returns:
            Path to the generated PDF file
            
        Raises:
            Exception if PDF generation fails
        """
        try:
            # Ensure output directory exists
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Prepare template data
            template_data = {
                **invoice_data,
                **self.company_info,
                # Add formatted amount with rupee symbol
                "AmountFormatted": f"₹{invoice_data.get('Amount', 0):,.2f}"
            }
            
            # Load and render template
            template_name = self.config.get("invoice_template", "gst_invoice.html")
            template = self.jinja_env.get_template(template_name)
            html_content = template.render(**template_data)
            
            # Generate PDF filename
            invoice_no = invoice_data.get("InvoiceNo", "unknown")
            pdf_filename = f"{invoice_no}.pdf"
            pdf_path = output_path / pdf_filename
            
            # Convert HTML to PDF
            try:
                pdfkit.from_string(html_content, str(pdf_path), options=self.pdfkit_options)
            except OSError as e:
                # If wkhtmltopdf is not found, provide helpful error
                if "wkhtmltopdf" in str(e).lower():
                    logger.error(
                        "wkhtmltopdf not found. Please install it from: "
                        "https://wkhtmltopdf.org/downloads.html"
                    )
                raise
            
            logger.info(f"Generated PDF invoice: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            logger.error(f"Error generating PDF for invoice {invoice_data.get('InvoiceNo')}: {str(e)}")
            raise
    
    def generate_multiple_invoices(self, invoices: list, output_dir: str) -> Dict[str, str]:
        """
        Generate PDFs for multiple invoices.
        
        Args:
            invoices: List of invoice data dictionaries
            output_dir: Directory to save the generated PDFs
            
        Returns:
            Dictionary mapping invoice numbers to PDF paths (successful only)
        """
        results = {}
        
        for invoice in invoices:
            invoice_no = invoice.get("InvoiceNo", "unknown")
            try:
                pdf_path = self.generate_invoice_pdf(invoice, output_dir)
                results[invoice_no] = pdf_path
            except Exception as e:
                logger.error(f"Failed to generate PDF for invoice {invoice_no}: {str(e)}")
                # Continue with next invoice
                continue
        
        logger.info(f"Generated {len(results)} PDFs out of {len(invoices)} invoices")
        return results
