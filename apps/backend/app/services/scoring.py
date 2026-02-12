from app.models.signals import SiteSignals
from typing import Dict, Any

def score_to_grade(score: int) -> str:
    """
    評級標準 (配合新權重 - Scheme A)
    """
    if score >= 70:
        return 'A'  # 優秀
    if score >= 55:
        return 'B'  # 良好
    if score >= 35:
        return 'C'  # 及格
    if score >= 20:
        return 'D'  # 需改善
    return 'F'      # 不及格

def calculate_score_v2(signals: SiteSignals) -> Dict[str, Any]:
    """
    新版評分系統 (2.0) - Scheme A
    移除罕見元素,聚焦可控制指標 (Discovery, Structure, Technical)
    """
    
    # 1. AI 可發現性 (30 分) - 最基本的 SEO
    discoverability_score = 0
    discoverability_items = []
    
    if signals.has_title:
        discoverability_score += 15
        discoverability_items.append({
            'name': 'title',
            'score': 15,
            'status': 'pass',
            'details': '已設置'
        })
    else:
        discoverability_items.append({
            'name': 'title',
            'score': 0,
            'status': 'fail',
            'suggestion': '在 <head> 加入 <title> 標籤'
        })
    
    if signals.has_description:
        discoverability_score += 10
        discoverability_items.append({
            'name': 'description',
            'score': 10,
            'status': 'pass',
            'details': '已設置'
        })
    else:
        discoverability_items.append({
            'name': 'description',
            'score': 0,
            'status': 'fail',
            'suggestion': '在 <head> 加入 <meta name="description">'
        })
    
    if signals.has_favicon:
        discoverability_score += 5
        discoverability_items.append({
            'name': 'favicon',
            'score': 5,
            'status': 'pass',
            'details': '已設置'
        })
    else:
        discoverability_items.append({
            'name': 'favicon',
            'score': 0,
            'status': 'fail',
            'suggestion': '加入 favicon.ico 或 <link rel="icon">'
        })
    
    # 2. 內容結構化 (35 分) - 最重要的 AI 可讀性
    structure_score = 0
    structure_items = []
    
    # 有 JSON-LD (10 分)
    if signals.has_jsonld or signals.schema_count > 0:
        structure_score += 10
        structure_items.append({
            'name': 'has_jsonld',
            'score': 10,
            'status': 'pass',
            'details': '已啟用'
        })
    else:
        structure_items.append({
            'name': 'has_jsonld',
            'score': 0,
            'status': 'fail',
            'suggestion': '加入 JSON-LD 結構化資料'
        })
    
    # Schema 多樣性
    schema_count = signals.schema_count
    if schema_count == 0 and signals.has_jsonld:
         schema_count = 1
         
    schema_variety_score = min(schema_count * 5, 20)
    structure_score += schema_variety_score
    
    structure_items.append({
        'name': 'schema_variety',
        'score': schema_variety_score,
        'status': 'pass' if schema_variety_score > 0 else 'fail',
        'details': f"{schema_count} 種類型: {', '.join(signals.schema_types[:3])}" if signals.schema_types else "一般",
    })
    
    # Schema 質量
    high_value_schemas = {'Organization', 'Person', 'Product', 'Article', 'WebSite', 'BreadcrumbList'}
    has_high_value = any(t in high_value_schemas for t in signals.schema_types)
    
    if schema_count >= 2 or has_high_value:
        structure_score += 5
        structure_items.append({
            'name': 'schema_quality',
            'score': 5,
            'status': 'pass',
            'details': '結構豐富'
        })
    else:
        structure_items.append({
            'name': 'schema_quality',
            'score': 0,
            'status': 'fail',
            'suggestion': '建議使用多種 Schema 類型'
        })
    
    # 3. 技術基礎 (20 分)
    technical_score = 0
    technical_items = []
    
    if signals.has_https:
        technical_score += 15
        technical_items.append({
            'name': 'https',
            'score': 15,
            'status': 'pass',
            'details': '已啟用'
        })
    else:
        technical_items.append({
            'name': 'https',
            'score': 0,
            'status': 'fail',
            'suggestion': '啟用 HTTPS 加密連線'
        })
    
    # 基本可用性
    if signals.has_title or signals.has_description:
        technical_score += 5
        technical_items.append({
            'name': 'basic_usability',
            'score': 5,
            'status': 'pass',
            'details': '正常存取'
        })
    else:
        technical_items.append({
            'name': 'basic_usability',
            'score': 0,
            'status': 'fail'
        })
    
    # 4. 社群信任 (15 分)
    social_score = 0
    social_items = []
    
    # 社群連結
    social_count = signals.social_links_count
    if social_count >= 2:
        social_score += 10
        social_items.append({
            'name': 'social_links',
            'score': 10,
            'status': 'pass',
            'details': f"{social_count} 個平台"
        })
    elif social_count == 1:
        social_score += 5
        social_items.append({
            'name': 'social_links',
            'score': 5,
            'status': 'partial',
            'details': "1 個平台",
            'suggestion': '建議至少連結 2 個社群平台'
        })
    else:
        social_items.append({
            'name': 'social_links',
            'score': 0,
            'status': 'fail',
            'suggestion': '在頁尾加入社群連結'
        })
    
    # 權威連結
    outbound_count = signals.outbound_links_count
    if outbound_count >= 1:
        social_score += 5
        social_items.append({
            'name': 'authority_links',
            'score': 5,
            'status': 'pass',
            'details': f"{outbound_count} 條外部連結"
        })
    else:
        social_items.append({
            'name': 'authority_links',
            'score': 0,
            'status': 'fail',
            'suggestion': '適當引用權威網站資源'
        })
    
    # 計算總分
    total_score = (
        discoverability_score +  # 最多 30
        structure_score +         # 最多 35
        technical_score +         # 最多 20
        social_score              # 最多 15
    )
    
    return {
        'score': min(total_score, 100),
        'grade': score_to_grade(total_score),
        'dimensions': {
            'discoverability': {
                'score': discoverability_score,
                'max': 30,
                'items': discoverability_items
            },
            'structure': {
                'score': structure_score,
                'max': 35,
                'items': structure_items
            },
            'technical': {
                'score': technical_score,
                'max': 20,
                'items': technical_items
            },
            'social': {
                'score': social_score,
                'max': 15,
                'items': social_items
            },
            # 保留 identity 以防前端報錯 (雖不計分但結構需存在)
            'identity': {
                'score': 0, # 已被移除權重
                'max': 0,
                'items': []
            }
        }
    }

def calculate_weighted_score(signals: SiteSignals) -> int:
    return calculate_score_v2(signals)['score']

def calculate_dimension_scores(signals: SiteSignals) -> Dict[str, Dict]:
    return calculate_score_v2(signals)['dimensions']
