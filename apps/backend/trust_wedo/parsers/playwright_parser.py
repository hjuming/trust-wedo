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

    def __init__(self, browser: Optional[Browser] = None):
        self.playwright = None
        self.browser: Optional[Browser] = browser
        self._owns_browser = browser is None

    async def __aenter__(self):
        """Initialize Playwright and launch browser if not provided."""
        if not self.browser:
            try:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox', 
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled'  # Stealth: Hide webdriver
                    ]
                )
                self._owns_browser = True
            except Exception as e:
                logger.error(f"Failed to initialize Playwright: {e}")
                if self.playwright:
                    await self.playwright.stop()
                raise
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup browser and Playwright resources if owned."""
        if self._owns_browser:
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
            logger.info(f"[Playwright] Starting fetch for {url}")
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
                logger.debug(f"[Playwright] Navigating to {url} (networkidle)...")
                # 1. Navigation with extended timeout (30s)
                response = await page.goto(url, wait_until='networkidle', timeout=30000)
                
                if not response:
                    logger.error(f"[Playwright] No response for {url}")
                    return None
                    
                # Handle error status codes
                if response.status >= 400:
                    logger.warning(f"[Playwright] Status {response.status} for {url}")
                    # For 403/401, it's likely blocking. We log it.
                    if response.status in [403, 401]:
                         logger.warning(f"[Playwright] Access denied (Anti-scraping?) for {url}")
                         
                # 2. Explicitly wait for DOM to be present (Hydration check)
                try:
                    logger.debug(f"[Playwright] Waiting for 'body' selector...")
                    # Wait for body to be attached to DOM
                    await page.wait_for_selector('body', timeout=10000)
                except Exception as e:
                    logger.warning(f"[Playwright] Timeout waiting for body selector on {url}: {e}")

                # 3. Fixed delay for React/Vue hydration (Critical for Scoring 2.0)
                # Some SPAs render 'body' but content comes later via JS
                logger.debug(f"[Playwright] Hydration buffer (3s)...")
                await page.wait_for_timeout(3000)
                
            except PlaywrightTimeoutError:
                logger.warning(f"[Playwright] Navigation timeout for {url} (networkidle). Retrying with domcontentloaded.")
                try:
                     response = await page.goto(url, wait_until='domcontentloaded', timeout=15000)
                     logger.debug(f"[Playwright] Hydration buffer after retry (3s)...")
                     await page.wait_for_timeout(3000) # Wait for hydration
                except Exception as e:
                     logger.error(f"[Playwright] Fallback navigation failed: {e}")

            # Get full rendered HTML (whether fully idle or timed out)
            try:
                content = await page.content()
                if content:
                    size_kb = len(content) / 1024
                    has_schema = 'application/ld+json' in content
                    logger.info(f"[Playwright] Successfully fetched {url}. Size: {size_kb:.1f}KB, Has Schema: {has_schema}")
                    
                    if len(content) < 1000:
                        logger.warning(f"[Playwright] Warning: Content size very small ({len(content)} bytes). Might be blocked or empty.")
                    
                    if not has_schema and "wedopr" in url:
                        logger.warning(f"[Playwright] Warning: No Schema.org detected for wedopr. Check hydration.")
                
                return content
            except Exception as e:
                logger.error(f"[Playwright] Failed to get page content: {e}")
                return None
            
        except Exception as e:
            logger.error(f"[Playwright] Page error for {url}: {e}")
            return None
            
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
