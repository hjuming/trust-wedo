"""Site parser module for Trust WEDO."""

import json
from datetime import datetime
from typing import Dict, List, Any
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class SiteParser:
    """Parser for scanning websites."""

    def __init__(self, base_url: str, max_pages: int = 10):
        self.base_url = base_url.rstrip("/")
        self.max_pages = max_pages
        self.pages: List[Dict[str, Any]] = []
        self.checks = {"robots_ok": False, "sitemap_ok": False}
        self.visited_urls = set()

    async def scan(self) -> Dict[str, Any]:
        """Perform site scan."""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # 1. Check robots.txt (minimal check)
            try:
                robots_resp = await client.get(f"{self.base_url}/robots.txt")
                self.checks["robots_ok"] = robots_resp.status_code == 200
            except Exception:
                self.checks["robots_ok"] = False

            # 2. Check sitemap.xml
            sitemap_urls = await self._find_sitemap_urls(client)
            if sitemap_urls:
                self.checks["sitemap_ok"] = True
                urls_to_scan = sitemap_urls[:self.max_pages]
            else:
                self.checks["sitemap_ok"] = False
                urls_to_scan = [self.base_url]

            # 3. Scan pages
            for url in urls_to_scan:
                if len(self.pages) >= self.max_pages:
                    break
                page_info = await self._scan_page(client, url)
                if page_info:
                    self.pages.append(page_info)

        return {
            "site": self.base_url,
            "pages": self.pages,
            "checks": self.checks
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

    async def _scan_page(self, client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
        """Scan a single page."""
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        try:
            resp = await client.get(url)
            fetched = resp.status_code == 200
            has_jsonld = False
            has_meta = False

            if fetched:
                soup = BeautifulSoup(resp.content, "html.parser")
                has_jsonld = bool(soup.find("script", type="application/ld+json"))
                has_meta = bool(soup.find("meta"))

            return {
                "url": url,
                "fetched": fetched,
                "has_jsonld": has_jsonld,
                "has_meta": has_meta
            }
        except Exception:
            return {
                "url": url,
                "fetched": False,
                "has_jsonld": False,
                "has_meta": False
            }
