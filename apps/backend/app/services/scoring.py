from app.models.signals import SiteSignals
from typing import Dict, Any

def score_to_grade(score: int) -> str:
    """
    評級標準 (配合 Scoring 2.0)
    A: 80-100 (優秀)
    B: 60-79 (良好)
    C: 40-59 (及格)
    D: 20-39 (需改善)
    F: 0-19 (不及格)
    """
    if score >= 80:
        return 'A'
    if score >= 60:
        return 'B'
    if score >= 40:
        return 'C'
    if score >= 20:
        return 'D'
    return 'F'

def calculate_score_v2(signals: SiteSignals) -> Dict[str, Any]:
    """
    新版評分系統 (2.0) - Scheme B Revised
    
    Dimensions (Total 100):
    1. 結構化 (Structure): 30% (Deep Schema Analysis)
    2. 可發現性 (Discoverability): 20% (Title 8, Desc 7, Favicon 5)
    3. 信任訊號 (Trust): 20% (HTTPS 10, Performance 10)
    4. 技術基礎 (Technical): 15% (Mobile 10, Basic 5)
    5. 身份識別 (Identity): 15% (About/Contact 10, Social 5)
    """
    
    # 1. 結構化 (30 分) - 核心權重
    analysis = getattr(signals, 'schema_analysis', {})
    structure_score = analysis.get('score', 0) if analysis else 0
    structure_items = []
    
    if analysis and analysis.get('details'):
        for detail in analysis.get('details', []):
            structure_items.append({
                'name': 'schema_detail',
                'score': 0,
                'status': 'pass',
                'details': detail
            })
    else:
        # Fallback for legacy signals or empty analysis
        if signals.has_jsonld or signals.schema_count > 0:
            structure_score = 10 # Basic score
            structure_items.append({'name': 'basic_schema', 'score': 10, 'status': 'pass', 'details': '基本結構化資料'})
        else:
            structure_items.append({
                'name': 'schema_missing',
                'score': 0,
                'status': 'fail',
                'suggestion': '加入 Schema.org 結構化資料以大幅提升 AI 理解度'
            })
    
    # 2. 可發現性 (20 分)
    discoverability_score = 0
    discoverability_items = []
    
    if signals.has_title:
        discoverability_score += 8
        discoverability_items.append({'name': 'title', 'score': 8, 'status': 'pass', 'details': '已設置'})
    else:
        discoverability_items.append({'name': 'title', 'score': 0, 'status': 'fail', 'suggestion': '設置網頁標題 <title>'})
        
    if signals.has_description:
        discoverability_score += 7
        discoverability_items.append({'name': 'description', 'score': 7, 'status': 'pass', 'details': '已設置'})
    else:
        discoverability_items.append({'name': 'description', 'score': 0, 'status': 'fail', 'suggestion': '設置 Meta Description'})
        
    if signals.has_favicon:
        discoverability_score += 5
        discoverability_items.append({'name': 'favicon', 'score': 5, 'status': 'pass', 'details': '已設置'})
    else:
        discoverability_items.append({'name': 'favicon', 'score': 0, 'status': 'fail', 'suggestion': '設置網站圖示 (Favicon)'})

    # 3. 信任訊號 (20 分)
    trust_score = 0
    trust_items = []
    
    # HTTPS (10)
    if signals.has_https:
        trust_score += 10
        trust_items.append({'name': 'https', 'score': 10, 'status': 'pass', 'details': '已啟用 SSL'})
    else:
        trust_items.append({'name': 'https', 'score': 0, 'status': 'fail', 'suggestion': '啟用 HTTPS 加密連線'})
        
    # Performance (10)
    load_time = getattr(signals, 'page_load_time', None)
    if load_time is not None:
        if load_time < 2.0:
            trust_score += 10
            trust_items.append({'name': 'performance', 'score': 10, 'status': 'pass', 'details': f'載入速度極快 ({load_time:.2f}s)'})
        elif load_time < 4.0:
            trust_score += 5
            trust_items.append({'name': 'performance', 'score': 5, 'status': 'pass', 'details': f'載入速度尚可 ({load_time:.2f}s)'})
        else:
            trust_items.append({'name': 'performance', 'score': 0, 'status': 'fail', 'suggestion': f'優化網站效能 (目前 {load_time:.2f}s)'})
    else:
        # If load time unavailable (legacy), give partial score
        trust_score += 5
        trust_items.append({'name': 'performance', 'score': 5, 'status': 'partial', 'details': '無法測量，給予預設分數'})

    # 4. 技術基礎 (15 分)
    technical_score = 0
    technical_items = []
    
    # Mobile Friendly (10)
    is_mobile = getattr(signals, 'is_mobile_friendly', False)
    if is_mobile:
        technical_score += 10
        technical_items.append({'name': 'mobile_friendly', 'score': 10, 'status': 'pass', 'details': '適配行動裝置'})
    else:
        technical_items.append({'name': 'mobile_friendly', 'score': 0, 'status': 'fail', 'suggestion': '設定 Viewport Meta Tag 適配行動裝置'})
        
    # Basic Usability (5)
    if signals.has_title or signals.has_description:
        technical_score += 5
        technical_items.append({'name': 'basic_usability', 'score': 5, 'status': 'pass', 'details': '基礎結構正常'})
    else:
        technical_items.append({'name': 'basic_usability', 'score': 0, 'status': 'fail'})

    # 5. 身份識別 (15 分)
    identity_score = 0
    identity_items = []
    
    # About/Contact (10)
    if signals.has_about_page or signals.has_contact:
        identity_score += 10
        identity_items.append({'name': 'identity_page', 'score': 10, 'status': 'pass', 'details': '有關於/聯繫頁面'})
    elif getattr(signals, 'has_author', False):
         identity_score += 5
         identity_items.append({'name': 'identity_page', 'score': 5, 'status': 'partial', 'details': '僅有作者資訊', 'suggestion': '建議新增關於/聯繫頁面'})
    else:
        identity_items.append({'name': 'identity_page', 'score': 0, 'status': 'fail', 'suggestion': '建立關於我們或聯繫頁面'})
        
    # Social Links (5)
    social_count = getattr(signals, 'social_links_count', 0)
    if social_count >= 1:
        identity_score += 5
        identity_items.append({'name': 'social_presence', 'score': 5, 'status': 'pass', 'details': f'{social_count} 個社群連結'})
    else:
        identity_items.append({'name': 'social_presence', 'score': 0, 'status': 'fail', 'suggestion': '連結社群媒體帳號'})

    # Calculate Total
    total_score = (
        structure_score +        # Max 30
        discoverability_score +  # Max 20
        trust_score +            # Max 20
        technical_score +        # Max 15
        identity_score           # Max 15
    )
    
    return {
        'score': min(total_score, 100),
        'grade': score_to_grade(total_score),
        'dimensions': {
            'structure': {
                'name': '結構化',
                'score': structure_score,
                'max': 30,
                'percentage': int((structure_score / 30) * 100) if structure_score > 0 else 0,
                'items': structure_items
            },
            'discoverability': {
                'name': '可發現性',
                'score': discoverability_score,
                'max': 20,
                'percentage': int((discoverability_score / 20) * 100) if discoverability_score > 0 else 0,
                'items': discoverability_items
            },
            'trust': {
                'name': '信任訊號',
                'score': trust_score,
                'max': 20,
                'percentage': int((trust_score / 20) * 100) if trust_score > 0 else 0,
                'items': trust_items
            },
            'technical': {
                'name': '技術體質',
                'score': technical_score,
                'max': 15,
                'percentage': int((technical_score / 15) * 100) if technical_score > 0 else 0,
                'items': technical_items
            },
            'identity': {
                'name': '身份識別',
                'score': identity_score,
                'max': 15,
                'percentage': int((identity_score / 15) * 100) if identity_score > 0 else 0,
                'items': identity_items
            }
        }
    }

def calculate_weighted_score(signals: SiteSignals) -> int:
    return calculate_score_v2(signals)['score']

def calculate_dimension_scores(signals: SiteSignals) -> Dict[str, Dict]:
    return calculate_score_v2(signals)['dimensions']
