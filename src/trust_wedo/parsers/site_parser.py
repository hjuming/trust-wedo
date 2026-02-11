"""Site parser module for Trust WEDO."""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from trust_wedo.utils.meta import get_meta


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
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 TrustWEDO/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7"
        }
        
        async with httpx.AsyncClient(follow_redirects=True, headers=headers, timeout=30.0) as client:
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
            if self.base_url.startswith("file://"):
                self.checks["sitemap_ok"] = False
                urls_to_scan = [self.base_url]
            else:
                try:
                    sitemap_urls = await self._find_sitemap_urls(client)
                    if sitemap_urls:
                        self.checks["sitemap_ok"] = True
                        urls_to_scan = sitemap_urls[:self.max_pages]
                    else:
                        self.checks["sitemap_ok"] = False
                        urls_to_scan = [self.base_url]
                except Exception as e:
                    print(f"[WARN] Failed to check sitemap: {e}")
                    self.checks["sitemap_ok"] = False
                    urls_to_scan = [self.base_url]

            # 3. Scan pages
            print(f"[INFO] Starting scan for {self.base_url} with {len(urls_to_scan)} URLs")
            for url in urls_to_scan:
                if len(self.pages) >= self.max_pages:
                    break
                try:
                    page_info = await self._scan_page(client, url)
                    if page_info:
                        self.pages.append(page_info)
                except Exception as e:
                    print(f"[ERROR] Failed to scan page {url}: {e}")

        return {
            "site": self.base_url,
            "pages": self.pages,
            "checks": self.checks,
            "meta": get_meta(self.base_url)
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

    def _parse_jsonld(self, soup: BeautifulSoup) -> List[str]:
        """解析 JSON-LD 結構化資料,提取所有 @type 欄位。
        
        支援格式:
        1. 單一物件: {"@type": "Organization", ...}
        2. @graph 格式: {"@graph": [{"@type": "Organization"}, ...]}
        3. 陣列格式: [{"@type": "WebSite"}, {"@type": "Organization"}]
        
        Returns:
            List[str]: 所有找到的 @type 值列表
        """
        schema_types = []
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            if not script.string:
                continue
                
            try:
                data = json.loads(script.string)
                
                # 處理陣列格式
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "@type" in item:
                            type_value = item["@type"]
                            # @type 可能是字串或陣列
                            if isinstance(type_value, list):
                                schema_types.extend(type_value)
                            else:
                                schema_types.append(type_value)
                
                # 處理物件格式
                elif isinstance(data, dict):
                    # 處理 @graph 格式 (常見於 Google 推薦的格式)
                    if "@graph" in data:
                        for item in data["@graph"]:
                            if isinstance(item, dict) and "@type" in item:
                                type_value = item["@type"]
                                if isinstance(type_value, list):
                                    schema_types.extend(type_value)
                                else:
                                    schema_types.append(type_value)
                    
                    # 處理單一物件
                    elif "@type" in data:
                        type_value = data["@type"]
                        if isinstance(type_value, list):
                            schema_types.extend(type_value)
                        else:
                            schema_types.append(type_value)
                            
            except (json.JSONDecodeError, TypeError, KeyError):
                # 忽略無效的 JSON-LD
                continue
        
        # 去除重複
        return list(set(schema_types))

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
            schema_types = []
            has_favicon = False
            social_platforms = []
            
            if fetched and soup:
                # 解析 JSON-LD Schema.org
                schema_types = self._parse_jsonld(soup)
                has_jsonld = len(schema_types) > 0 or bool(soup.find("script", type="application/ld+json"))
                
                # 基本 meta 資訊
                title = soup.find("title")
                has_meta_desc = bool(soup.find("meta", attrs={"name": "description"}))
                has_meta = has_meta_desc
                
                print(f"[DEBUG] Parsed {url}: Title={bool(title)}, Desc={has_meta_desc}, Schema={len(schema_types)}")

                
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
                
                # Count external links (修復:使用網域比對而非完整 URL)
                all_links = soup.find_all("a", href=True)
                external_links = []
                
                # 從 base_url 提取主網域
                base_domain = urlparse(self.base_url).netloc.replace('www.', '')
                
                for l in all_links:
                    href = l.get("href")
                    if isinstance(href, list):
                        href = href[0] if href else ""
                    
                    # 只處理絕對 URL
                    if href and isinstance(href, str) and href.startswith("http"):
                        link_domain = urlparse(href).netloc.replace('www.', '')
                        
                        # 如果網域不同,才算外部連結
                        if link_domain and link_domain != base_domain:
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
                    "schema_types": schema_types,  # 新增欄位
                    "has_meta": has_meta,
                    "has_favicon": has_favicon,   # 新增欄位
                    "title_missing": not bool(title),
                    "meta_missing": not has_meta_desc,
                    "is_about_author": is_about_author,
                    "external_links_count": external_links_count,
                    "social_links_count": social_links_count,
                    "social_platforms": social_platforms  # 新增欄位
                }
            
            return {
                "url": url,
                "fetched": False,
                "has_jsonld": False,
                "schema_types": [],
                "has_meta": False,
                "has_favicon": False,
                "title_missing": True,
                "meta_missing": True,
                "is_about_author": False,
                "external_links_count": 0,
                "social_links_count": 0,
                "social_platforms": []
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
