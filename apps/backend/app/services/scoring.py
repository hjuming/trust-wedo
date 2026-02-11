from app.models.signals import SiteSignals
from typing import Dict, Tuple

# === 新版 100 分制五大維度評分系統 (v2.0) ===

# 五大維度權重定義
DIMENSIONS = {
    'discoverability': {  # AI 可發現性 (20分)
        'title': 10,
        'description': 7,
        'favicon': 3
    },
    'identity': {  # 身分可信度 (25分)
        'organization': 10,
        'author': 10,
        'contact': 5
    },
    'structure': {  # 內容結構化 (25分)
        'has_jsonld': 5,        # 有任何 Schema
        'schema_variety': 15,    # 多樣性 (每種 +3 分,最多 15)
        'schema_quality': 5      # Organization/Person 額外加分
    },
    'social': {  # 社群信任 (15分)
        'social_links': 10,  # 2+ 平台
        'authority_links': 5
    },
    'technical': {  # 技術基礎 (15分)
        'https': 10,
        'performance': 5
    }
}


def calculate_dimension_scores(signals: SiteSignals) -> Dict[str, Dict]:
    """計算五大維度分數明細
    
    Returns:
        Dict[str, Dict]: 每個維度包含 score, max, items
    """
    dimensions = {}
    
    # 1. AI可發現性 (20分)
    discoverability_items = []
    discoverability_score = 0
    
    if signals.has_title:
        discoverability_score += 10
        discoverability_items.append({'name': 'title', 'score': 10, 'status': 'pass'})
    else:
        discoverability_items.append({'name': 'title', 'score': 0, 'status': 'fail'})
    
    if signals.has_description:
        discoverability_score += 7
        discoverability_items.append({'name': 'description', 'score': 7, 'status': 'pass'})
    else:
        discoverability_items.append({'name': 'description', 'score': 0, 'status': 'fail'})
    
    if signals.has_favicon:
        discoverability_score += 3
        discoverability_items.append({'name': 'favicon', 'score': 3, 'status': 'pass'})
    else:
        discoverability_items.append({'name': 'favicon', 'score': 0, 'status': 'fail'})
    
    dimensions['discoverability'] = {
        'score': discoverability_score,
        'max': 20,
        'items': discoverability_items
    }
    
    # 2. 身分可信度 (25分)
    identity_items = []
    identity_score = 0
    
    if signals.has_organization:
        identity_score += 10
        identity_items.append({'name': 'organization', 'score': 10, 'status': 'pass'})
    else:
        identity_items.append({'name': 'organization', 'score': 0, 'status': 'fail'})
    
    if signals.has_author:
        identity_score += 10
        identity_items.append({'name': 'author', 'score': 10, 'status': 'pass'})
    else:
        identity_items.append({'name': 'author', 'score': 0, 'status': 'fail'})
    
    if signals.has_contact:
        identity_score += 5
        identity_items.append({'name': 'contact', 'score': 5, 'status': 'pass'})
    else:
        identity_items.append({'name': 'contact', 'score': 0, 'status': 'fail'})
    
    dimensions['identity'] = {
        'score': identity_score,
        'max': 25,
        'items': identity_items
    }
    
    # 3. 內容結構化 (25分)
    structure_items = []
    structure_score = 0
    
    # 有任何 JSON-LD
    if signals.has_jsonld:
        structure_score += 5
        structure_items.append({'name': 'has_jsonld', 'score': 5, 'status': 'pass'})
    else:
        structure_items.append({'name': 'has_jsonld', 'score': 0, 'status': 'fail'})
    
    # Schema 多樣性 (每種 +3 分,最多 15 分)
    variety_score = min(signals.schema_count * 3, 15)
    structure_score += variety_score
    structure_items.append({
        'name': 'schema_variety',
        'score': variety_score,
        'status': 'pass' if variety_score > 0 else 'fail',
        'details': f'{signals.schema_count} types: {", ".join(signals.schema_types)}'
    })
    
    # Schema 質量 (Organization/Person 額外加分)
    quality_score = 0
    if signals.has_organization or signals.has_person:
        quality_score = 5
        structure_score += quality_score
        structure_items.append({'name': 'schema_quality', 'score': 5, 'status': 'pass'})
    else:
        structure_items.append({'name': 'schema_quality', 'score': 0, 'status': 'fail'})
    
    dimensions['structure'] = {
        'score': structure_score,
        'max': 25,
        'items': structure_items
    }
    
    # 4. 社群信任 (15分)
    social_items = []
    social_score = 0
    
    if signals.social_links_count >= 2:
        social_score += 10
        social_items.append({
            'name': 'social_links',
            'score': 10,
            'status': 'pass',
            'details': f'{signals.social_links_count} platforms'
        })
    else:
        social_items.append({
            'name': 'social_links',
            'score': 0,
            'status': 'fail',
            'details': f'{signals.social_links_count} platforms (need 2+)'
        })
    
    if signals.has_authority_links:
        social_score += 5
        social_items.append({'name': 'authority_links', 'score': 5, 'status': 'pass'})
    else:
        social_items.append({'name': 'authority_links', 'score': 0, 'status': 'fail'})
    
    dimensions['social'] = {
        'score': social_score,
        'max': 15,
        'items': social_items
    }
    
    # 5. 技術基礎 (15分)
    technical_items = []
    technical_score = 0
    
    if signals.has_https:
        technical_score += 10
        technical_items.append({'name': 'https', 'score': 10, 'status': 'pass'})
    else:
        technical_items.append({'name': 'https', 'score': 0, 'status': 'fail'})
    
    # Performance
    if signals.page_load_time:
        if signals.page_load_time < 2.0:
            perf_score = 5
        elif signals.page_load_time < 3.0:
            perf_score = 3
        elif signals.page_load_time < 5.0:
            perf_score = 2
        else:
            perf_score = 0
        technical_score += perf_score
        technical_items.append({
            'name': 'performance',
            'score': perf_score,
            'status': 'pass' if perf_score > 0 else 'fail',
            'details': f'{signals.page_load_time:.2f}s'
        })
    else:
        technical_items.append({'name': 'performance', 'score': 0, 'status': 'unknown'})
    
    dimensions['technical'] = {
        'score': technical_score,
        'max': 15,
        'items': technical_items
    }
    
    return dimensions


def calculate_weighted_score(signals: SiteSignals) -> int:
    """計算總分 (v2.0 - 五大維度)
    
    Returns:
        int: 0-100 的總分
    """
    dimensions = calculate_dimension_scores(signals)
    total_score = sum(d['score'] for d in dimensions.values())
    return min(total_score, 100)


def score_to_grade(score: int) -> str:
    """分數轉換為等級 (v2.1 - 優化門檻)"""
    if score >= 80:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 40:
        return 'C'
    elif score >= 20:
        return 'D'
    else:
        return 'F'


# === 向後相容:保留舊版權重配置 ===
WEIGHTS = {
    'https': 20,
    'schema': 20,
    'title': 15,
    'description': 10,
    'author': 10,
    'favicon': 5,
    'social': 5,
    'authority_links': 5,
    'performance': 10
}
