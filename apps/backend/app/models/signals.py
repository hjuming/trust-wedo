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
    has_organization: bool = False
    has_person: bool = False
    has_website: bool = False
    has_article: bool = False
    
    # 作者與關於
    has_author: bool = False
    has_about_page: bool = False
    has_contact: bool = False
    
    # 引用與來源
    outbound_links_count: int = 0
    citation_count: int = 0
    has_authority_links: bool = False
    
    # 技術指標
    page_load_time: Optional[float] = None
    has_https: bool = False
    
    @classmethod
    def from_artifacts(cls, artifacts: List[Dict[str, Any]]) -> "SiteSignals":
        """從 artifacts 提取 signals"""
        signals = cls()
        
        # 從 scan artifact 提取
        scan_artifact = next((a for a in artifacts if a['stage'] == 'scan'), None)
        if scan_artifact:
            payload = scan_artifact['jsonb_payload']
            metadata = payload.get('metadata', {})
            
            signals.has_title = bool(metadata.get('title'))
            signals.has_description = bool(metadata.get('description'))
            signals.has_favicon = bool(metadata.get('favicon'))
            signals.has_https = payload.get('url', '').startswith('https://')
            
            # Schema.org 檢測
            schemas = payload.get('schemas', [])
            signals.schema_count = len(schemas)
            signals.has_organization = any(s.get('@type') == 'Organization' for s in schemas)
            signals.has_person = any(s.get('@type') == 'Person' for s in schemas)
            signals.has_website = any(s.get('@type') == 'WebSite' for s in schemas)
            signals.has_article = any(s.get('@type') == 'Article' for s in schemas)
            
            # 作者檢測
            signals.has_author = bool(metadata.get('author'))
            
            # 連結統計
            links = payload.get('links', [])
            signals.outbound_links_count = len([l for l in links if l.get('type') == 'external'])
        
        return signals
