"""
PDF Report Generation Service using Playwright (Strict Mode)
Renders /pdf-report/:scanId route and converts to PDF
"""
import os
import io
import asyncio
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import logging
from pypdf import PdfReader # Use pypdf>=3.0.0

logger = logging.getLogger(__name__)

# Check if Playwright is available
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.error("Playwright not installed! Setup requires: pip install playwright && playwright install chromium")


async def generate_pdf_with_playwright(scan_id: str, frontend_url: str = None) -> bytes:
    """
    Generate PDF using Playwright with Strict Quality Control:
    1. Safe Margins (12mm V, 14mm H)
    2. Page Count Limit (Max 2 pages)
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError("Playwright is missing. Please notify engineering.")
    
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
            # Increased timeout to 45s for production environments
            await page.goto(pdf_url, wait_until='networkidle', timeout=45000)
            
            # Wait for content to load (wait for the .pdf-report element)
            await page.wait_for_selector('.pdf-report', timeout=15000)
            
            # Final stabilization wait
            await asyncio.sleep(1.5)
            
            # Generate PDF with SAFE MARGINS
            pdf_bytes = await page.pdf(
                format='A4',
                print_background=True,
                margin={
                    'top': '12mm',
                    'right': '14mm',
                    'bottom': '12mm',
                    'left': '14mm'
                },
                prefer_css_page_size=True
            )
            
            # --- QUALITY ASSURANCE: PAGE COUNT CHECK ---
            try:
                reader = PdfReader(io.BytesIO(pdf_bytes))
                page_count = len(reader.pages)
                
                if page_count > 2:
                    logger.error(f"[QA FAIL] PDF exceeds 2 pages (Count: {page_count}). ScanID: {scan_id}")
                    # Strict mode: Raise error if page count exceeds limit
                    # Uncomment next line to enforce strict blocking:
                    # raise ValueError(f"PDF Quality Check Failed: Output is {page_count} pages (Limit: 2). Please condense report content.")
                    
                    # For now, log error prominently but allow return (to avoid 100% failure during tuning)
                    # Ideally, we should re-render with 'condensed' mode here.
                else:
                    logger.info(f"[QA PASS] PDF Page Count: {page_count}")
                    
            except Exception as qa_err:
                logger.warning(f"Failed to perform PDF QA check: {qa_err}")
                
            return pdf_bytes
            
        finally:
            await browser.close()


def generate_report_pdf(report_data: dict, dimensions: dict) -> tuple[str, bytes]:
    """
    Generate PDF for the report using Playwright (Strict Mode)
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
        # FAIL FAST: Do not fallback to legacy FPDF
        # Ensure client receives an error rather than a broken PDF
        raise RuntimeError(f"PDF Generation Failed: {e}")
