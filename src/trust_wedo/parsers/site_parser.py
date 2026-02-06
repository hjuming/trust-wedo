"""Site parser module for Trust WEDO."""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
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
            if self.base_url.startswith("file://"):
                self.checks["robots_ok"] = True
            else:
                try:
                    robots_resp = await client.get(f"{self.base_url}/robots.txt")
                    self.checks["robots_ok"] = robots_resp.status_code == 200
                except Exception:
                    self.checks["robots_ok"] = False

            # 2. Check sitemap.xml
            if self.base_url.startswith("file://"):
                self.checks["sitemap_ok"] = False
                urls_to_scan = [self.base_url]
            else:
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

    async def _scan_page(self, client: httpx.AsyncClient, url: str) -> Optional[Dict[str, Any]]:
        """Scan a single page."""
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        try:
            if url.startswith("file://"):
                file_path = url[7:]
                with open(file_path, "rb") as f:
                    content = f.read()
                fetched = True
                # Mock a response object-like behavior for consistency if needed,
                # but we only need the content here.
                soup = BeautifulSoup(content, "html.parser")
            else:
                resp = await client.get(url)
                fetched = resp.status_code == 200
                if fetched:
                    soup = BeautifulSoup(resp.content, "html.parser")
                else:
                    soup = None

            has_jsonld = False
            has_meta = False

            if fetched and soup:
                has_jsonld = bool(soup.find("script", type="application/ld+json"))
                
                title = soup.find("title")
                has_meta_desc = bool(soup.find("meta", attrs={"name": "description"}))
                has_meta = has_meta_desc
                
                # Check for about/author pages
                about_author_keywords = ["about", "author", "team", "contact", "關於", "作者"]
                url_path = urlparse(url).path.lower()
                is_about_author = any(kw in url_path for kw in about_author_keywords)
                
                # Count external links
                all_links = soup.find_all("a", href=True)
                external_links = []
                for l in all_links:
                    href = l.get("href")
                    if isinstance(href, list):
                        href = href[0] if href else ""
                    if href and isinstance(href, str) and href.startswith("http") and self.base_url not in href:
                        external_links.append(href)
                
                external_links_count = len(external_links)
                
                # Count social links
                social_domains = ["twitter.com", "facebook.com", "linkedin.com", "github.com", "instagram.com"]
                social_links = [l for l in external_links if any(sd in l for sd in social_domains)]
                social_links_count = len(social_links)

                return {
                    "url": url,
                    "fetched": fetched,
                    "has_jsonld": has_jsonld,
                    "has_meta": has_meta,
                    "title_missing": not bool(title),
                    "meta_missing": not has_meta_desc,
                    "is_about_author": is_about_author,
                    "external_links_count": external_links_count,
                    "social_links_count": social_links_count
                }
            
            return {
                "url": url,
                "fetched": False,
                "has_jsonld": False,
                "has_meta": False,
                "title_missing": True,
                "meta_missing": True,
                "is_about_author": False,
                "external_links_count": 0,
                "social_links_count": 0
            }
        except Exception:
            return {
                "url": url,
                "fetched": False,
                "has_jsonld": False,
                "has_meta": False,
                "title_missing": True,
                "meta_missing": True,
                "is_about_author": False,
                "external_links_count": 0,
                "social_links_count": 0
            }
