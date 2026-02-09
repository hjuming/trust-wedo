from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SiteSignals(BaseModel):
    """網站信號（從 artifacts 提取的特徵）"""
    
    # 基礎信號
    has_title: bool = False
    has_description: bool = False
    has_favicon: bool = False
    
    # Schema.org 信號
    schema_count: int = 0
    schema_types: List[str] = []  # 所有檢測到的 schema 類型
    has_organization: bool = False
    has_person: bool = False
    has_website: bool = False
    has_article: bool = False
    has_jsonld: bool = False
    
    # 作者與關於
    has_author: bool = False
    author_count: int = 0
    author_names: List[str] = []
    has_about_page: bool = False
    has_contact: bool = False
    
    # 社群連結
    social_links_count: int = 0
    has_social_proof: bool = False
    social_platforms: List[str] = []  # ['facebook', 'twitter', 'linkedin']
    
    # 引用與來源
    outbound_links_count: int = 0
    citation_count: int = 0
    has_authority_links: bool = False
    authority_domains: List[str] = []  # ['.gov', '.edu', 'nytimes.com']
    
    # 技術指標
    page_load_time: Optional[float] = None
    has_https: bool = False
    is_mobile_friendly: Optional[bool] = None
    
    @classmethod
    def from_artifacts(cls, artifacts: List[Dict[str, Any]]) -> "SiteSignals":
        """從 artifacts 提取 signals（修復版）"""
        signals = cls()
        
        # 從 scan artifact 提取
        scan_artifact = next((a for a in artifacts if a['stage'] == 'scan'), None)
        if not scan_artifact:
            return signals
        
        payload = scan_artifact['jsonb_payload']
        
        # ✅ 正確：從 site URL 判斷 HTTPS
        site_url = payload.get('site', '')
        signals.has_https = site_url.startswith('https://')
        
        # ✅ 正確：從 pages 陣列提取資訊
        pages = payload.get('pages', [])
        if not pages:
            return signals
        
        # 使用第一個頁面（通常是首頁）
        first_page = pages[0]
        
        # 基礎信號
        signals.has_title = not first_page.get('title_missing', True)
        signals.has_description = not first_page.get('meta_missing', True)
        signals.has_favicon = first_page.get('has_favicon', False)
        
        # Schema.org 檢測
        signals.has_jsonld = first_page.get('has_jsonld', False)
        # TODO: 當 CLI 提供更多 schemas 資訊時擴充 schema_types, schema_count 等
        
        # 作者檢測
        signals.has_author = first_page.get('is_about_author', False)
        
        # 連結統計
        signals.outbound_links_count = first_page.get('external_links_count', 0)
        signals.social_links_count = first_page.get('social_links_count', 0)
        signals.has_social_proof = signals.social_links_count >= 2
        
        # About 頁面檢測
        signals.has_about_page = any(
            page.get('is_about_author', False) for page in pages
        )
        
        # Contact 頁面檢測（簡化判斷）
        signals.has_contact = any(
            'contact' in page.get('url', '').lower() for page in pages
        )
        
        return signals
