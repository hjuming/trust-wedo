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
            signals.schema_types = [s.get('@type') for s in schemas if s.get('@type')]
            signals.has_organization = any(s.get('@type') == 'Organization' for s in schemas)
            signals.has_person = any(s.get('@type') == 'Person' for s in schemas)
            signals.has_website = any(s.get('@type') == 'WebSite' for s in schemas)
            signals.has_article = any(s.get('@type') == 'Article' for s in schemas)
            
            # 作者檢測
            authors = set()
            if metadata.get('author'):
                authors.add(metadata['author'])
            
            for schema in schemas:
                if schema.get('@type') in ['Article', 'BlogPosting']:
                    author = schema.get('author', {})
                    if isinstance(author, dict):
                        author_name = author.get('name')
                        if author_name:
                            authors.add(author_name)
                    elif isinstance(author, str):
                        authors.add(author)
            
            signals.author_names = list(authors)
            signals.author_count = len(authors)
            signals.has_author = len(authors) > 0
            
            # 連結分析
            links = payload.get('links', [])
            signals.outbound_links_count = len([l for l in links if l.get('type') == 'external'])
            
            # 社群連結分析
            social_domains = {
                'facebook.com': 'facebook',
                'twitter.com': 'twitter',
                'x.com': 'twitter',
                'linkedin.com': 'linkedin',
                'instagram.com': 'instagram'
            }
            
            social_platforms = set()
            for link in links:
                link_url = link.get('url', '')
                for domain, platform in social_domains.items():
                    if domain in link_url:
                        social_platforms.add(platform)
            
            signals.social_platforms = list(social_platforms)
            signals.social_links_count = len(social_platforms)
            signals.has_social_proof = len(social_platforms) >= 2
            
            # 權威連結分析
            authority_domain_patterns = {'.gov', '.edu', 'wikipedia.org', 'nytimes.com'}
            found_authorities = set()
            for link in links:
                if link.get('type') == 'external':
                    link_url = link.get('url', '')
                    for authority in authority_domain_patterns:
                        if authority in link_url:
                            found_authorities.add(authority)
            
            signals.authority_domains = list(found_authorities)
            signals.has_authority_links = len(found_authorities) > 0
        
        return signals
