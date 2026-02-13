from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SiteSignals(BaseModel):
    """網站信號（從 artifacts 提取的特徵）"""
    
    # URL (用於特殊網站檢測)
    url: Optional[str] = None
    
    # 基礎信號
    has_title: bool = False
    has_description: bool = False
    has_favicon: bool = False
    
    # Schema.org 信號
    schema_count: int = 0
    schema_types: List[str] = []
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
    social_platforms: List[str] = []
    
    # 外部連結
    outbound_links_count: int = 0
    citation_count: int = 0
    has_authority_links: bool = False
    authority_domains: List[str] = []
    
    # 效能指標
    page_load_time: Optional[float] = None
    has_https: bool = False
    is_mobile_friendly: Optional[bool] = None
    
    @classmethod
    def from_artifacts(cls, artifacts: List[Dict[str, Any]]) -> "SiteSignals":
        """從 artifacts 提取 signals（由 ReportEngine 調用特定邏輯）"""
        # 這裡我們維持基礎結構，邏輯會移動到 ReportEngine 以符合最新 Task 指令
        signals = cls()
        return signals
