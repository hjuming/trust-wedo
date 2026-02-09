from app.models.signals import SiteSignals
from typing import Tuple, List, Dict, Any

def classify_site_type(signals: SiteSignals) -> Tuple[str, float]:
    """
    識別網站類型
    
    Returns:
        (site_type, confidence)
        site_type: 'ecommerce' | 'blog' | 'corporate' | 'personal' | 'unknown'
        confidence: 0.0 - 1.0
    """
    
    # 電商網站
    if 'Product' in signals.schema_types or 'Offer' in signals.schema_types:
        return ('ecommerce', 0.9)
    
    # 部落格
    if signals.has_article and signals.has_author:
        return ('blog', 0.85)
    
    # 企業網站
    if signals.has_organization and signals.has_contact:
        return ('corporate', 0.8)
    
    # 個人網站
    if signals.has_person and not signals.has_organization:
        return ('personal', 0.75)
    
    # 未知類型
    return ('unknown', 0.5)

def generate_custom_suggestions(signals: SiteSignals, site_type: str) -> List[Dict[str, Any]]:
    """根據網站類型生成客製化建議"""
    
    suggestions = []
    
    # 電商網站專屬建議
    if site_type == 'ecommerce':
        if 'Product' not in signals.schema_types:
            suggestions.append({
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action": "加入 Product Schema.org 結構化資料",
                "impact_desc": "讓 Google 顯示產品資訊與價格，提升點擊率",
                "how_to": [
                    "1. 前往 https://schema.org/Product",
                    "2. 為每個產品頁面加入 JSON-LD",
                    "3. 包含 name, price, availability, image",
                    "4. 使用 Google Rich Results Test 驗證"
                ]
            })
    
    # 部落格專屬建議
    elif site_type == 'blog':
        if not signals.has_article:
            suggestions.append({
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action": "為文章加入 Article Schema.org",
                "impact_desc": "提升 Google 新聞收錄機會與 AI 引用率",
                "how_to": [
                    "1. 使用 Article 或 BlogPosting schema",
                    "2. 包含 headline, author, datePublished",
                    "3. 加入 image 與 publisher 資訊"
                ]
            })
    
    # 企業網站專屬建議
    elif site_type == 'corporate':
        if not signals.has_organization:
            suggestions.append({
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action": "加入 Organization Schema.org",
                "impact_desc": "讓 Google 顯示公司資訊與 Knowledge Graph",
                "how_to": [
                    "1. 使用 Organization schema",
                    "2. 包含 name, logo, address, contactPoint",
                    "3. 加入社群連結 (sameAs)"
                ]
            })
    
    # 個人網站專屬建議
    elif site_type == 'personal':
        if not signals.has_person:
            suggestions.append({
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action": "加入 Person Schema.org",
                "impact_desc": "建立個人 Knowledge Graph，提升專業形象",
                "how_to": [
                    "1. 使用 Person schema",
                    "2. 包含 name, jobTitle, description",
                    "3. 加入 image 與 sameAs (社群連結)"
                ]
            })
    
    return suggestions
