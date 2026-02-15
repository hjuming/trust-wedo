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
            # Check fail or partial status where score < max potential
            if item['status'] in ['fail', 'partial']:
                suggestion = _create_suggestion(dim_key, item, signals)
                if suggestion:
                    suggestions.append(suggestion)
    
    # 依 impact (分數) 降序排序
    suggestions.sort(key=lambda x: x['impact_score'], reverse=True)
    
    # 回傳前 3 項
    return [_format_suggestion(s) for s in suggestions[:3]]


def _create_suggestion(dimension: str, item: Dict, signals: SiteSignals) -> Dict[str, Any]:
    """為單一失分項目建立建議"""
    
    name = item['name']
    
    # Description 建議 (Discoverability)
    if name == 'description':
        return {
            'title': '加上網站描述 (Meta Description)',
            'impact_score': 7,
            'impact': '+7分',
            'effort': '5分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 區塊加入 <meta name="description" content="...">',
            'code_snippet': '<meta name="description" content="您的網站簡介 (建議 150-160 字元)">',
            'priority': 1
        }
    
    # Favicon 建議 (Discoverability)
    elif name == 'favicon':
        return {
            'title': '加上網站圖示 (Favicon)',
            'impact_score': 5,
            'impact': '+5分',
            'effort': '3分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 區塊加入 <link rel="icon">',
            'code_snippet': '<link rel="icon" type="image/png" href="/favicon.png">',
            'priority': 3
        }
    
    # Schema Missing 建議 (Structure)
    elif name == 'schema_missing':
        return {
            'title': '加入 Schema.org 結構化資料',
            'impact_score': 30, # High impact as it unlocks deep analysis
            'impact': '大幅提升',
            'effort': '15分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 或 <body> 加入 WebSite 或 Organization JSON-LD',
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
    
    # Social Presence 建議 (Identity)
    elif name == 'social_presence':
        return {
            'title': '連結社群媒體帳號',
            'impact_score': 5,
            'impact': '+5分',
            'effort': '10分鐘',
            'dimension': dimension,
            'instructions': '在頁尾加入 Facebook, Twitter, LinkedIn 等連結',
            'code_snippet': '''<footer>
  <a href="https://facebook.com/yourpage" target="_blank">Facebook</a>
  <a href="https://instagram.com/yourhandle" target="_blank">Instagram</a>
</footer>''',
            'priority': 2
        }

    # Identity Page 建議 (Identity)
    elif name == 'identity_page':
        if item.get('status') == 'partial':
             return {
                'title': '建立完整的「關於我們」頁面',
                'impact_score': 5,
                'impact': '+5分',
                'effort': '30分鐘',
                'dimension': dimension,
                'instructions': '建立 /about 或 /contact 頁面，增強品牌信任度',
                'priority': 3
            }
        else:
             return {
                'title': '建立關於或聯繫頁面',
                'impact_score': 10,
                'impact': '+10分',
                'effort': '30分鐘',
                'dimension': dimension,
                'instructions': '建立 /about 或 /contact 頁面，並在首頁加入連結',
                'priority': 2
            }
            
    # HTTPS 建議 (Trust)
    elif name == 'https':
        return {
            'title': '啟用 HTTPS 加密連線',
            'impact_score': 10,
            'impact': '+10分',
            'effort': '20分鐘',
            'dimension': dimension,
            'instructions': '申請 SSL 憑證並強制將 HTTP 重定向至 HTTPS',
            'priority': 1
        }

    # Mobile Friendly (Technical)
    elif name == 'mobile_friendly':
        return {
            'title': '設定 Viewport 適配行動裝置',
            'impact_score': 10,
            'impact': '+10分',
            'effort': '1分鐘',
            'dimension': dimension,
            'instructions': '在 <head> 加入 viewport meta tag',
            'code_snippet': '<meta name="viewport" content="width=device-width, initial-scale=1">',
            'priority': 1
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
