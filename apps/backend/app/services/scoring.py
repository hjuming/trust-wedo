from app.models.signals import SiteSignals

# 權重配置（總和 = 100）
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

def calculate_weighted_score(signals: SiteSignals) -> int:
    """計算加權分數（0-100）"""
    score = 0
    
    # HTTPS（20分）
    if signals.has_https:
        score += WEIGHTS['https']
    
    # Schema.org（20分）
    if signals.schema_count > 0:
        base_score = 10
        
        # 重要 schema 額外加分
        if signals.has_organization:
            base_score += 3
        if signals.has_person:
            base_score += 3
        if signals.has_article:
            base_score += 4
        
        score += min(base_score, 20)
    
    # Title（15分）
    if signals.has_title:
        score += WEIGHTS['title']
    
    # Description（10分）
    if signals.has_description:
        score += WEIGHTS['description']
    
    # Author（10分）
    if signals.has_author:
        score += WEIGHTS['author']
    
    # Favicon（5分）
    if signals.has_favicon:
        score += WEIGHTS['favicon']
    
    # Social（5分）
    if signals.has_social_proof:
        score += WEIGHTS['social']
    
    # Authority Links（5分）
    if signals.has_authority_links:
        score += WEIGHTS['authority_links']
    
    # Performance（10分）
    if signals.page_load_time:
        if signals.page_load_time < 2.0:
            score += 10
        elif signals.page_load_time < 3.0:
            score += 7
        elif signals.page_load_time < 5.0:
            score += 5
    
    return min(score, 100)

def score_to_grade(score: int) -> str:
    """分數轉換為等級"""
    if score >= 80:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 40:
        return 'C'
    else:
        return 'D'
