"""
PDF Report Generation Service using Playwright
Renders /pdf-report/:scanId route and converts to PDF
"""
import os
import asyncio
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

# Check if Playwright is available
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. PDF generation will fall back to legacy method.")


async def generate_pdf_with_playwright(scan_id: str, frontend_url: str = None) -> bytes:
    """
    Generate PDF using Playwright by rendering the /pdf-report/:scanId route
    
    Args:
        scan_id: The scan job ID
        frontend_url: Base URL of frontend (default: http://localhost:5173)
    
    Returns:
        PDF content as bytes
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install chromium")
    
    # Default to local dev if not specified
    if not frontend_url:
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    pdf_url = f"{frontend_url}/pdf-report/{scan_id}"
    
    logger.info(f"Generating PDF from: {pdf_url}")
    
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        try:
            # Create new page
            page = await browser.new_page()
            
            # Navigate to PDF template
            await page.goto(pdf_url, wait_until='networkidle', timeout=30000)
            
            # Wait for content to load (wait for the .pdf-report element)
            await page.wait_for_selector('.pdf-report', timeout=10000)
            
            # Additional wait to ensure all data is rendered
            await asyncio.sleep(1)
            
            # Generate PDF
            pdf_bytes = await page.pdf(
                format='A4',
                print_background=True,
                margin={
                    'top': '0mm',
                    'right': '0mm',
                    'bottom': '0mm',
                    'left': '0mm'
                },
                prefer_css_page_size=True
            )
            
            logger.info(f"PDF generated successfully: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        finally:
            await browser.close()


def generate_report_pdf(report_data: dict, dimensions: dict) -> tuple[str, bytes]:
    """
    Generate PDF for the report using Playwright
    
    Args:
        report_data: Report data from report engine
        dimensions: Dimensions data with scores
    
    Returns:
        (filename, pdf_content_bytes)
    """
    # Extract scan_id from report_data
    scan_id = report_data.get("job_id")
    if not scan_id:
        raise ValueError("Missing job_id in report_data")
    
    # Get frontend URL from environment
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    try:
        # Generate PDF using Playwright (async)
        pdf_content = asyncio.run(generate_pdf_with_playwright(scan_id, frontend_url))
        
        # Generate filename
        url = report_data.get("url", "")
        try:
            domain = urlparse(url).netloc.replace("www.", "")
        except:
            domain = "report"
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"Trust-WEDO-{domain}-{date_str}.pdf"
        
        return filename, pdf_content
        
    except Exception as e:
        logger.error(f"Failed to generate PDF with Playwright: {e}")
        
        # Fallback to legacy FPDF method if Playwright fails
        logger.info("Falling back to legacy PDF generation...")
        from app.services.report_pdf_legacy import generate_report_pdf as legacy_generate
        return legacy_generate(report_data, dimensions)
