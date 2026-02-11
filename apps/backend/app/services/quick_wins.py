"""Quick Wins 建議生成邏輯"""
from typing import List, Dict, Any
from app.models.signals import SiteSignals


def generate_quick_wins(signals: SiteSignals, dimension_scores: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """生成快速勝利建議
    
    Args:
        signals: 網站信號資料
        dimension_scores: 五大維度分數明細
        
    Returns:
        List[Dict]: 排序後的建議列表,回傳前 3 項
    """
    suggestions = []
    
    # 從各維度找出失分項目
    for dim_key, dim_data in dimension_scores.items():
        for item in dim_data['items']:
            if item['status'] == 'fail' and item['score'] == 0:
                suggestion = _create_suggestion(dim_key, item, signals)
                if suggestion:
                    suggestions.append(suggestion)
    
    # 依 impact (分數) 降序排序
    suggestions.sort(key=lambda x: x['impact_score'], reverse=True)
    
    # 回傳前 3 項
    return [_format_suggestion(s) for s in suggestions[:3]]


def _create_suggestion(dimension: str, item: Dict, signals: SiteSignals) -> Dict[str, Any]:
    """為單一失分項目建立建議"""
    
    # 計算該項目的最大分數 (失分量)
    potential_gain = 10 if 'organization' in item['name'] else \
                    10 if 'author' in item['name'] else \
                    10 if 'description' in item['name'] else \
                    10 if 'social_links' in item['name'] else \
                    7 if 'description' in item['name'] else \
                    5 if 'has_jsonld' in item['name'] or 'schema_quality' in item['name'] or 'contact' in item['name'] or 'authority_links' in item['name'] else \
                    3
    
    # Description 建議
    if item['name'] == 'description':
        return {
            'title': '加上網站描述',
            'impact_score': 7,
            'impact': '+7分',
            'effort': '5分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 區塊加入 <meta name="description" content="...">',
            'code_snippet': '<meta name="description" content="您的網站簡介 (建議 150-160 字元)">',
            'priority': 1
        }
    
    # Favicon 建議
    elif item['name'] == 'favicon':
        return {
            'title': '加上網站圖示',
            'impact_score': 3,
            'impact': '+3分',
            'effort': '3分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 區塊加入 <link rel="icon">',
            'code_snippet': '<link rel="icon" type="image/png" href="/favicon.png">',
            'priority': 3
        }
    
    # Organization Schema 建議
    elif item['name'] == 'organization':
        return {
            'title': '加上組織資訊 (Schema.org)',
            'impact_score': 10,
            'impact': '+10分',
            'effort': '10分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 或 <body> 加入 Organization JSON-LD',
            'code_snippet': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "您的組織名稱",
  "url": "https://yoursite.com"
}
</script>''',
            'priority': 2
        }
    
    # Social Links 建議
    elif item['name'] == 'social_links':
        return {
            'title': '連結至少 2 個社群平台',
            'impact_score': 10,
            'impact': '+10分',
            'effort': '10分鐘',
            'dimension': dimension,
            'instructions': '在頁尾加入 Facebook, Twitter, LinkedIn 等連結',
            'code_snippet': '''<footer>
  <a href="https://facebook.com/yourpage">Facebook</a>
  <a href="https://twitter.com/yourhandle">Twitter</a>
</footer>''',
            'priority': 2
        }
    
    # Author 建議
    elif item['name'] == 'author':
        return {
            'title': '加上作者資訊',
            'impact_score': 10,
            'impact': '+10分',
            'effort': '5分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 加入 <meta name="author">',
            'code_snippet': '<meta name="author" content="作者名稱">',
            'priority': 3
        }
    
    # JSON-LD 建議
    elif item['name'] == 'has_jsonld':
        return {
            'title': '加上基本 Schema.org 結構化資料',
            'impact_score': 5,
            'impact': '+5分',
            'effort': '10分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 或 <body> 加入 WebSite JSON-LD',
            'code_snippet': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "您的網站名稱",
  "url": "https://yoursite.com"
}
</script>''',
            'priority': 1
        }
    
    # Contact 建議
    elif item['name'] == 'contact':
        return {
            'title': '加上聯絡資訊頁面',
            'impact_score': 5,
            'impact': '+5分',
            'effort': '15分鐘',
            'dimension': dimension,
            'instructions': '建立 /contact 頁面或在首頁加入聯絡資訊',
            'priority': 3
        }
    
    return None


def _format_suggestion(suggestion: Dict[str, Any]) -> Dict[str, Any]:
    """格式化建議輸出,移除內部欄位"""
    return {
        'title': suggestion['title'],
        'impact': suggestion['impact'],
        'effort': suggestion['effort'],
        'dimension': suggestion['dimension'],
        'instructions': suggestion['instructions'],
        'code_snippet': suggestion.get('code_snippet'),
        'priority': suggestion['priority']
    }
