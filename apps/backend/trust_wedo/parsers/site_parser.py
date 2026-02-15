"""Site parser module for Trust WEDO."""

import asyncio
import json
import logging
import time
from typing import List, Dict, Any, Optional, Set, Callable, Awaitable
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from trust_wedo.utils.meta import get_meta

try:
    from trust_wedo.parsers.playwright_parser import PlaywrightParser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[WARN] Playwright parser not available, falling back to static parser")


class SiteParser:
    """Parser for scanning websites."""

    def __init__(self, base_url: str, max_pages: int = 10, use_playwright: bool = True, progress_callback: Optional[Callable[[int, str], Awaitable[None]]] = None):
        self.base_url = base_url.rstrip("/")
        self.max_pages = max_pages
        self.progress_callback = progress_callback
        self.pages: List[Dict[str, Any]] = []
        self.checks = {"robots_ok": False, "sitemap_ok": False}
        self.visited_urls = set()
        self.use_playwright = use_playwright and PLAYWRIGHT_AVAILABLE
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"'
        }

    async def scan(self) -> Dict[str, Any]:
        """Perform site scan."""
        if self.progress_callback:
            await self.progress_callback(5, "正在初始化爬蟲引擎...")
            
        playwright_parser = None
        # Parser selection logic
        # Note: self.use_playwright is already set in __init__ based on input and PLAYWRIGHT_AVAILABLE
        # The following block adds logging based on that decision.
        if self.use_playwright:
            if not PLAYWRIGHT_AVAILABLE:
                # Use print for critical initialization issues that might happen before logging is fully set up
                print("[ERROR] Playwright requested but NOT AVAILABLE. Falling back to static HTTP.")
            else:
                print(f"[INFO] Strict Mode: Playwright enabled for scan of {self.base_url}")
        else:
            print("[INFO] Default Mode: Using static HTTP parser.")
        
        # Initialize Playwright if enabled
        if self.use_playwright:
            try:
                playwright_parser = PlaywrightParser()
                await playwright_parser.__aenter__()
                print(f"[INFO] Initialized Playwright parser for {self.base_url}")
            except Exception as e:
                print(f"[ERROR] Failed to init Playwright: {e}")
                # In strict mode, we should probably fail here instead of falling back
                # to static parsing which we know will give poor results for SPAs.
                raise RuntimeError(f"Playwright initialization failed: {e}") from e
        elif not PLAYWRIGHT_AVAILABLE:
             print("[WARN] Playwright not available, using static parser.")

        try:
            async with httpx.AsyncClient(follow_redirects=True, headers=self.headers, timeout=30.0) as client:
                # 1. Check robots.txt (minimal check)
                if self.base_url.startswith("file://"):
                    self.checks["robots_ok"] = True
                else:
                    try:
                        robots_resp = await client.get(f"{self.base_url}/robots.txt")
                        self.checks["robots_ok"] = robots_resp.status_code == 200
                    except Exception as e:
                        print(f"[WARN] Failed to check robots.txt: {e}")
                        self.checks["robots_ok"] = False

                # 2. Check sitemap.xml
                urls_to_scan = [self.base_url]
                if not self.base_url.startswith("file://"):
                    try:
                        sitemap_urls = await self._find_sitemap_urls(client)
                        if sitemap_urls:
                            self.checks["sitemap_ok"] = True
                            urls_to_scan = sitemap_urls[:self.max_pages]
                        else:
                            self.checks["sitemap_ok"] = False
                    except Exception as e:
                        print(f"[WARN] Failed to check sitemap: {e}")
                        self.checks["sitemap_ok"] = False

                # 3. Scan pages
                print(f"[INFO] Starting scan for {self.base_url} with {len(urls_to_scan)} URLs")
                
                current_count = 0
                total_to_scan = min(len(urls_to_scan), self.max_pages)

                for url in urls_to_scan:
                    if len(self.pages) >= self.max_pages:
                        break
                    
                    current_count += 1
                    percent = 10 + int((current_count / total_to_scan) * 80)
                    if self.progress_callback:
                        await self.progress_callback(percent, f"正在掃描頁面 ({current_count}/{total_to_scan})...")
                        
                    try:
                        page_info = await self._scan_page(client, url, playwright_parser)
                        if page_info:
                            self.pages.append(page_info)
                    except Exception as e:
                        print(f"[ERROR] Failed to scan page {url}: {e}")

        finally:
            if playwright_parser:
                await playwright_parser.__aexit__(None, None, None)

        return {
            "site": self.base_url,
            "pages": self.pages,
            "checks": self.checks,
            "meta": get_meta(self.base_url),
            "parser_used": "playwright" if playwright_parser else "static"
        }

    async def _find_sitemap_urls(self, client: httpx.AsyncClient) -> List[str]:
        """Find URLs from sitemap.xml."""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        try:
            resp = await client.get(sitemap_url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "xml")
                urls = [loc.text for loc in soup.find_all("loc")]
                return urls
        except Exception:
            pass
        return []

    def _extract_schemas(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract all JSON-LD schema objects."""
        schemas = []
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            if not script.string:
                continue
                
            try:
                data = json.loads(script.string)
                
                # Handle list format
                if isinstance(data, list):
                    schemas.extend([item for item in data if isinstance(item, dict)])
                
                # Handle object format
                elif isinstance(data, dict):
                    # Handle @graph format
                    if "@graph" in data and isinstance(data["@graph"], list):
                        schemas.extend([item for item in data["@graph"] if isinstance(item, dict)])
                    else:
                        schemas.append(data)
                            
            except (json.JSONDecodeError, TypeError, KeyError):
                continue
        
        return schemas

    async def _scan_page(self, client: httpx.AsyncClient, url: str, playwright_parser: Any = None) -> Optional[Dict[str, Any]]:
        """Scan a single page using Playwright or static fallback."""
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        soup = None
        fetched = False
        start_time = time.time()
        
        # 1. Try Playwright first if available
        if playwright_parser and not url.startswith("file://"):
            try:
                content = await playwright_parser.fetch_content(url)
                if content:
                    soup = BeautifulSoup(content, "html.parser")
                    fetched = True
                else:
                    print(f"[WARN] Playwright returned no content for {url}, falling back to static")
            except Exception as e:
                print(f"[WARN] Playwright error for {url}: {e}")

        # 2. Fallback to httpx if not fetched and playwright NOT attempted
        if not fetched and not (playwright_parser and not url.startswith("file://")):
            if url.startswith("file://"):
                try:
                    with open(url[7:], "rb") as f:
                        content = f.read()
                    soup = BeautifulSoup(content, "html.parser")
                    fetched = True
                except Exception:
                    pass
            else:
                for attempt in range(2):
                    try:
                        resp = await client.get(url, timeout=30.0)
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.content, "html.parser")
                            fetched = True
                            
                            # Quick check if blocked
                            if not soup.find("title"):
                                print(f"[WARN] No title tag found for {url} (status {resp.status_code})")
                            break
                        elif resp.status_code in [429, 500, 502, 503, 504]:
                            await asyncio.sleep(2)
                    except Exception as e:
                        print(f"[WARN] Fetch attempt {attempt+1} failed for {url}: {e}")
                        await asyncio.sleep(1)

        # 3. Analyze content
        has_jsonld = False
        has_meta = False
        schema_types = []
        raw_schemas = []
        has_favicon = False
        social_platforms = []
        external_links_count = 0
        social_links_count = 0
        
        if fetched and soup:
            # Extract raw schemas
            raw_schemas = self._extract_schemas(soup)
            
            # Extract types from raw schemas
            types_set = set()
            for s in raw_schemas:
                t = s.get('@type')
                if isinstance(t, list):
                    types_set.update(t)
                elif t:
                    types_set.add(t)
            schema_types = list(types_set)
            
            has_jsonld = len(schema_types) > 0 or bool(soup.find("script", type="application/ld+json"))
            
            # 基本 meta 資訊
            title_tag = soup.find("title")
            has_title = bool(title_tag and title_tag.string and title_tag.string.strip())
            
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if not meta_desc:
                meta_desc = soup.find("meta", attrs={"property": "og:description"})
            
            has_meta_desc = bool(meta_desc and meta_desc.get("content", "").strip())
            has_meta = has_meta_desc
            
            has_meta_desc = bool(meta_desc and meta_desc.get("content", "").strip())
            has_meta = has_meta_desc
            
            # 視口檢查 (Mobile Friendly)
            has_viewport = bool(soup.find("meta", attrs={"name": "viewport"}))
            
            load_time = time.time() - start_time
            print(f"[DEBUG] Parsed{'(PW)' if playwright_parser and not url.startswith('file://') else ''} {url}: Title={has_title}, Desc={has_meta_desc}, Schema={len(schema_types)}, Time={load_time:.2f}s")
            
            # Favicon 偵測
            has_favicon = bool(
                soup.find("link", rel="icon") or 
                soup.find("link", rel="shortcut icon") or
                soup.find("link", rel="apple-touch-icon")
            )
            
            # Check for about/author pages
            about_author_keywords = ["about", "author", "team", "contact", "關於", "作者"]
            url_path = urlparse(url).path.lower()
            is_about_author = any(kw in url_path for kw in about_author_keywords)
            
            # Count external links
            all_links = soup.find_all("a", href=True)
            external_links = []
            
            def get_root_domain(url_str):
                try:
                    netloc = urlparse(url_str).netloc.lower().replace('www.', '')
                    parts = netloc.split('.')
                    if len(parts) >= 2:
                        return f"{parts[-2]}.{parts[-1]}"
                    return netloc
                except:
                    return ""

            base_root = get_root_domain(self.base_url)
            
            for l in all_links:
                href = l.get("href")
                if isinstance(href, list):
                    href = href[0] if href else ""
                
                if href and isinstance(href, str) and href.startswith("http"):
                    link_root = get_root_domain(href)
                    if link_root and link_root != base_root:
                        external_links.append(href)
            
            external_links_count = len(external_links)
            
            # Count social links & platforms
            social_domains = {
                "twitter.com": "Twitter",
                "x.com": "X (Twitter)",
                "facebook.com": "Facebook",
                "linkedin.com": "LinkedIn",
                "github.com": "GitHub",
                "instagram.com": "Instagram",
                "youtube.com": "YouTube",
                "tiktok.com": "TikTok"
            }
            social_links = []
            for link in external_links:
                for domain, platform in social_domains.items():
                    if domain in link:
                        social_links.append(link)
                        if platform not in social_platforms:
                            social_platforms.append(platform)
                        break
            
            social_links_count = len(social_links)

            return {
                "url": url,
                "fetched": fetched,
                "has_jsonld": has_jsonld,
                "schema_types": schema_types,
                "schemas": raw_schemas,
                "has_meta": has_meta,
                "has_favicon": has_favicon,
                "has_viewport": has_viewport,
                "load_time": load_time,
                "title_missing": not has_title,
                "meta_missing": not has_meta_desc,
                "is_about_author": is_about_author,
                "external_links_count": external_links_count,
                "social_links_count": social_links_count,
                "social_platforms": social_platforms
            }
        
        return {
            "url": url,
            "fetched": False,
            "has_jsonld": False,
            "schema_types": [],
            "schemas": [],
            "has_meta": False,
            "has_favicon": False,
            "title_missing": True,
            "meta_missing": True,
            "is_about_author": False,
            "external_links_count": 0,
            "social_links_count": 0,
            "social_platforms": []
        }
