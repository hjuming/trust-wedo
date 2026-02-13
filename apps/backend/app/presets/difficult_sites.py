"""
特殊網站配置 - 已知難以爬取的高防護網站

這些網站通常採用嚴格的反爬蟲機制,導致自動化檢測困難。
本模組提供預估分數和用戶友好的說明。
"""

from typing import Optional, Dict
from urllib.parse import urlparse

DIFFICULT_SITES = {
    'wikipedia.org': {
        'name': 'Wikipedia',
        'name_zh': '維基百科',
        'reason': '維基百科採用嚴格的反爬蟲機制以保護服務器資源',
        'estimated_score': 90,
        'estimated_grade': 'A',
        'note': '作為全球最大的開放知識庫,具備完整的結構化資料和極高的外部引用量,實際評分應在 85-95 分之間',
        'detection_method': 'partial',  # 'none', 'partial', 'full'
    },
    'developer.mozilla.org': {
        'name': 'MDN Web Docs',
        'name_zh': 'Mozilla 開發者文檔',
        'reason': 'MDN 採用進階防護機制以確保文檔服務穩定性',
        'estimated_score': 92,
        'estimated_grade': 'A',
        'note': '作為前端技術權威文檔,具備優秀的結構化資料和技術社群信任度,實際評分應在 88-95 分之間',
        'detection_method': 'partial',
    },
    'github.com': {
        'name': 'GitHub',
        'name_zh': 'GitHub',
        'reason': 'GitHub 對自動化訪問有速率限制',
        'estimated_score': 88,
        'estimated_grade': 'A',
        'note': '作為全球最大的代碼託管平台,具備完整的技術權威性,實際評分應在 85-92 分之間',
        'detection_method': 'partial',
    },
}


def check_difficult_site(url: str) -> Optional[Dict]:
    """
    檢查是否為已知的難以爬取網站
    
    Args:
        url: 要檢查的網址
        
    Returns:
        如果是特殊網站,返回配置信息;否則返回 None
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 移除 www. 前綴進行匹配
        if domain.startswith('www.'):
            domain = domain[4:]
        
        for special_domain, info in DIFFICULT_SITES.items():
            if special_domain in domain:
                return {
                    'is_difficult': True,
                    'domain': special_domain,
                    **info
                }
        
        return None
        
    except Exception:
        return None


def get_estimated_dimensions(site_info: Dict) -> Dict[str, int]:
    """
    根據特殊網站類型返回預估的維度分數
    
    Args:
        site_info: 特殊網站配置信息
        
    Returns:
        各維度的預估分數
    """
    # 根據網站類型返回不同的預估值
    if 'wikipedia.org' in site_info['domain']:
        return {
            'discoverability': 25,  # 完整的 title, description, favicon
            'structure': 25,        # 豐富的 Schema.org 結構化資料
            'technical': 20,        # HTTPS + 高可用性
            'social': 20,           # 大量外部引用,但缺少社群連結
        }
    elif 'developer.mozilla.org' in site_info['domain']:
        return {
            'discoverability': 25,
            'structure': 25,
            'technical': 20,
            'social': 22,
        }
    elif 'github.com' in site_info['domain']:
        return {
            'discoverability': 23,
            'structure': 20,
            'technical': 20,
            'social': 25,
        }
    else:
        # 默認值
        return {
            'discoverability': 20,
            'structure': 20,
            'technical': 20,
            'social': 20,
        }
