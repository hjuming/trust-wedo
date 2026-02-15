"""
Playwright-based parser for dynamic content rendering.
Handles SPA websites (React/Vue/Angular) and basic anti-scraping.
"""
import logging
import random
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

# Common User Agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

class PlaywrightParser:
    """Parser that uses headless Chromium to render JS-heavy websites."""

    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None

    async def __aenter__(self):
        """Initialize Playwright and launch browser."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            return self
        except Exception as e:
            logger.error(f"Failed to initialize Playwright: {e}")
            if self.playwright:
                await self.playwright.stop()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup browser and Playwright resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def fetch_content(self, url: str, timeout: int = 45000) -> Optional[str]:
        """
        Fetch URL content using existing browser instance.
        
        Args:
            url: The target URL
            timeout: Timeout in milliseconds (default 45s)
            
        Returns:
            Rendered HTML content string, or None if failed.
        """
        if not self.browser:
            raise RuntimeError("Browser not initialized. Use 'async with PlaywrightParser() as parser:' context.")
            
        page: Optional[Page] = None
        context = None
        
        try:
            # Create new context for isolation (cookies, storage, etc.)
            context = await self.browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={'width': 1280, 'height': 800},
                locale='en-US',
                # Basic bot mitigation: Disable webdriver flag (simple approach)
                # java_script_enabled=True # Default is True
            )
            
            page = await context.new_page()
            
            # Resource optimization: Block images/fonts/media
            await page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["image", "media", "font"] 
                else route.continue_())
            
            # Navigate
            # networkidle is important for SPAs to finish initial rendering
            try:
                response = await page.goto(url, wait_until='networkidle', timeout=timeout)
                
                if not response:
                    logger.error(f"Playwright received no response for {url}")
                    return None
                    
                # Handle error status codes
                if response.status >= 400:
                    logger.warning(f"Playwright received status {response.status} for {url}")
                    # For 403/401, it's likely blocking. We log it.
                    if response.status in [403, 401]:
                         logger.warning(f"Access denied (Anti-scraping?) for {url}")
                
            except PlaywrightTimeoutError:
                logger.warning(f"Playwright navigation timeout for {url} (networkidle). Returning content loaded so far.")
            
            # Get full rendered HTML (whether fully idle or timed out)
            content = await page.content()
            return content
            
        except Exception as e:
            logger.error(f"Playwright page error for {url}: {e}")
            return None
            
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
