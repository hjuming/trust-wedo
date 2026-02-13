from typing import List, Dict, Any, Tuple
from app.models.signals import SiteSignals
from app.services.scoring import calculate_weighted_score, score_to_grade, calculate_dimension_scores
from app.services.site_classifier import classify_site_type, generate_custom_suggestions
from app.config.difficult_sites import check_difficult_site, get_estimated_dimensions

class Rule:
    """單一規則"""
    def __init__(self, rule_id: str, condition, issue: Dict[str, Any], suggestion: Dict[str, Any]):
        self.rule_id = rule_id
        self.condition = condition
        self.issue = issue
        self.suggestion = suggestion
    
    def evaluate(self, signals: SiteSignals) -> bool:
        """評估規則是否命中"""
        return self.condition(signals)

class ReportEngine:
    """報告引擎 v2.0 - 強化版"""
    
    VERSION = "r2.0"
    
    def __init__(self):
        self.rules = self._init_rules()
    
    def _init_rules(self) -> List[Rule]:
        """初始化規則集"""
        return [
            Rule(
                rule_id="R001",
                condition=lambda s: not s.has_title,
                issue={
                    "severity": "high",
                    "title": "網站沒有清楚的標題",
                    "description": "AI 與搜尋引擎無法快速識別你的網站主題，這會降低權威感。",
                    "why": "標題是 AI 理解網站的第一步"
                },
                suggestion={
                    "priority": "high",
                    "effort": "easy",
                    "impact": "high",
                    "action": "在網頁原始碼中新增 <title> 標籤",
                    "impact_desc": "立即提升搜尋引擎排名與 AI 引用率",
                    "how_to": [
                        "1. 打開網站的 HTML 檔案",
                        "2. 在 <head> 區塊中加入 <title>你的網站名稱</title>",
                        "3. 確保標題簡潔且描述性強（建議 50-60 字元）",
                        "4. 儲存並重新部署網站"
                    ]
                }
            ),
            Rule(
                rule_id="R002",
                condition=lambda s: not s.has_description,
                issue={
                    "severity": "medium",
                    "title": "缺少網站描述",
                    "description": "缺少 Meta Description 讓 AI 難以在不閱讀全站內容的情況下總結你的價值。",
                    "why": "描述幫助 AI 快速摘要網站內容"
                },
                suggestion={
                    "priority": "medium",
                    "effort": "easy",
                    "impact": "medium",
                    "action": "撰寫並加入 <meta name='description'> 標籤",
                    "impact_desc": "提高搜尋結果的點擊率並幫助 AI 摘要",
                    "how_to": [
                        "1. 撰寫 150-160 字元的網站描述",
                        "2. 在 <head> 區塊加入 <meta name='description' content='你的描述'>",
                        "3. 確保描述包含關鍵字且吸引人",
                        "4. 儲存並重新部署"
                    ]
                }
            ),
            Rule(
                rule_id="R003",
                condition=lambda s: not s.has_jsonld,
                issue={
                    "severity": "high",
                    "title": "缺少結構化資料（Schema.org）",
                    "description": "沒有 JSON-LD 結構化資料，AI 無法理解你的網站類型與內容結構。",
                    "why": "結構化資料是 AI 理解網站的關鍵"
                },
                suggestion={
                    "priority": "high",
                    "effort": "medium",
                    "impact": "high",
                    "action": "新增 Schema.org JSON-LD 結構化資料",
                    "impact_desc": "大幅提升 AI 對網站的理解與引用率",
                    "how_to": [
                        "1. 前往 https://schema.org 選擇適合的類型（Organization/WebSite/Article）",
                        "2. 使用 Google 的結構化資料標記協助工具產生 JSON-LD",
                        "3. 將 JSON-LD 加入 <head> 或 <body> 區塊",
                        "4. 使用 Google Rich Results Test 驗證"
                    ]
                }
            ),
            Rule(
                rule_id="R004",
                condition=lambda s: not s.has_author,
                issue={
                    "severity": "medium",
                    "title": "缺少作者資訊",
                    "description": "內容沒有明確的作者，降低可信度與權威性。",
                    "why": "作者資訊是內容可信度的重要指標"
                },
                suggestion={
                    "priority": "medium",
                    "effort": "easy",
                    "impact": "medium",
                    "action": "在內容中加入作者資訊",
                    "impact_desc": "提升內容可信度與專業形象",
                    "how_to": [
                        "1. 在文章頁面加入作者名稱",
                        "2. 使用 <meta name='author' content='作者名稱'>",
                        "3. 或在 Schema.org Article 中加入 author 欄位",
                        "4. 考慮加入作者簡介與社群連結"
                    ]
                }
            ),
            Rule(
                rule_id="R005",
                condition=lambda s: not s.has_https,
                issue={
                    "severity": "high",
                    "title": "未使用 HTTPS 加密",
                    "description": "網站使用 HTTP 而非 HTTPS，安全性不足。",
                    "why": "HTTPS 是現代網站的基本要求"
                },
                suggestion={
                    "priority": "high",
                    "effort": "medium",
                    "impact": "high",
                    "action": "啟用 HTTPS 加密連線",
                    "impact_desc": "提升安全性與搜尋引擎排名",
                    "how_to": [
                        "1. 向 SSL 憑證供應商申請憑證（Let's Encrypt 免費）",
                        "2. 在伺服器安裝 SSL 憑證",
                        "3. 設定 HTTP 自動重新導向到 HTTPS",
                        "4. 更新所有內部連結為 HTTPS"
                    ]
                }
            ),
            # 新增規則 R006-R008
            Rule(
                rule_id="R006",
                condition=lambda s: not s.has_organization,
                issue={
                    "severity": "medium",
                    "title": "缺少組織資訊",
                    "description": "缺少 Organization schema 讓 AI 難以確認網站的營運主體。",
                    "why": "組織身分驗證是信任的基石"
                },
                suggestion={
                    "priority": "medium",
                    "effort": "medium",
                    "impact": "medium",
                    "action": "新增 Organization 結構化資料",
                    "impact_desc": "建立網站的實體權威感"
                }
            ),
            Rule(
                rule_id="R007",
                condition=lambda s: not s.has_social_proof,
                issue={
                    "severity": "low",
                    "title": "社群證明不足",
                    "description": "網站未連結足夠的社群平台（Facebook, Twitter, LinkedIn 等）。",
                    "why": "社群連結可增加網站的社會認可"
                },
                suggestion={
                    "priority": "low",
                    "effort": "easy",
                    "impact": "low",
                    "action": "在頁尾或關於頁面加入社群媒體連結",
                    "impact_desc": "提升品牌可尋性與多管道信任"
                }
            )
        ]

    def extract_signals(self, artifacts: List[Dict[str, Any]]) -> SiteSignals:
        """從 artifacts 提取所有信號 (Refactored Logic)"""
        signals = SiteSignals()
        
        scan_artifact = next((a for a in artifacts if a['stage'] == 'scan'), None)
        if not scan_artifact:
            return signals
            
        payload = scan_artifact['jsonb_payload']
        site_url = payload.get('site', '')
        signals.has_https = site_url.startswith('https://')
        
        pages = payload.get('pages', [])
        if not pages:
            return signals
            
        first_page = pages[0]
        
        # 1. 基礎信號
        signals.has_title = not first_page.get('title_missing', True)
        signals.has_description = not first_page.get('meta_missing', True)
        signals.has_favicon = first_page.get('has_favicon', False)
        
        # 2. Schema.org 檢測
        self._extract_schema_types(first_page, signals)
        
        # 3. 作者資訊提取
        self._extract_author_info(first_page, signals)
        
        # 4. 社群連結提取
        self._extract_social_links(first_page, signals)
        
        # 5. 外部連結分析
        self._analyze_outbound_links(first_page, signals)
        
        # 6. 頁面與聯繫
        signals.has_about_page = any(p.get('is_about_author', False) for p in pages)
        signals.has_contact = any('contact' in p.get('url', '').lower() for p in pages)
        
        return signals

    def _extract_schema_types(self, page_data: Dict[str, Any], signals: SiteSignals):
        """解析 JSON-LD 類型"""
        signals.has_jsonld = page_data.get('has_jsonld', False)
        # 注意：目前 CLI artifact 可能未將完整 schemas 列表傳回，
        # 這裡假設未來會有一個 'schemas' 欄位或使用 has_jsonld 作為基礎
        # 暫時依賴已有的 flags (如果有)
        # 假設 CLI 擴充後會有 schema_types 陣列
        types = page_data.get('schema_types', [])
        signals.schema_types = types
        signals.schema_count = len(types)
        signals.has_organization = 'Organization' in types
        signals.has_person = 'Person' in types
        signals.has_website = 'WebSite' in types
        signals.has_article = any(t in types for t in ['Article', 'BlogPosting'])

    def _extract_author_info(self, page_data: Dict[str, Any], signals: SiteSignals):
        """提取作者資訊"""
        # 優先使用 CLI 判斷的 is_about_author
        signals.has_author = page_data.get('is_about_author', False)
        # 假設未來有作者名稱列表
        signals.author_names = page_data.get('authors', [])
        signals.author_count = len(signals.author_names)

    def _extract_social_links(self, page_data: Dict[str, Any], signals: SiteSignals):
        """識別社群連結"""
        signals.social_links_count = page_data.get('social_links_count', 0)
        signals.has_social_proof = signals.social_links_count >= 2
        # 假設未來有 platforms 列表
        signals.social_platforms = page_data.get('social_platforms', [])

    def _analyze_outbound_links(self, page_data: Dict[str, Any], signals: SiteSignals):
        """分析外部連結"""
        signals.outbound_links_count = page_data.get('external_links_count', 0)
        # 假設未來有權威網域列表
        authorities = page_data.get('authority_domains', [])
        signals.authority_domains = authorities
        signals.has_authority_links = len(authorities) > 0

    def generate_report(self, signals: SiteSignals) -> Dict[str, Any]:
        """產生報告（更新版 - 支持特殊網站檢測）"""
        
        # 0. 檢查是否為特殊網站
        difficult_site_info = check_difficult_site(signals.url) if hasattr(signals, 'url') else None
        
        # 1. 識別網站類型
        site_type, confidence = classify_site_type(signals)
        
        # 2. 評估規則
        fired_rules = []
        issues = []
        suggestions = []
        
        for rule in self.rules:
            if rule.evaluate(signals):
                fired_rules.append(rule.rule_id)
                issues.append(rule.issue)
                suggestions.append(rule.suggestion)
        
        # 3. 加入客製化建議
        custom_suggestions = generate_custom_suggestions(signals, site_type)
        suggestions.extend(custom_suggestions)
        
        # 4. 計算評分和維度分數
        grade, score = self._calculate_grade(signals, len(fired_rules))
        dimensions = calculate_dimension_scores(signals)
        conclusion = self._generate_conclusion(grade, len(fired_rules))
        
        # 5. 如果是特殊網站且評分異常低,添加預估信息
        base_report = {
            "report_version": self.VERSION,
            "signals": signals.model_dump(),
            "score": score,
            "dimensions": dimensions,
            "site_type": site_type,
            "site_type_confidence": confidence,
            "rules_fired": fired_rules,
            "summary": {
                "conclusion": conclusion,
                "grade": grade,
                "score": score,
                "total_issues": len(issues)
            },
            "issues": issues,
            "suggestions": suggestions[:8]
        }
        
        # 如果是特殊網站且檢測失敗(分數過低)
        if difficult_site_info and score < 50:
            estimated_dims = get_estimated_dimensions(difficult_site_info)
            estimated_total = sum(estimated_dims.values())
            estimated_grade = score_to_grade(estimated_total)
            
            # 構建完整的維度結構(包含 max 和 items)
            estimated_dimensions_full = {}
            dimension_max_scores = {
                'discoverability': 25,
                'structure': 25,
                'technical': 20,
                'social': 30
            }
            
            for dim_name, dim_score in estimated_dims.items():
                estimated_dimensions_full[dim_name] = {
                    'score': dim_score,
                    'max': dimension_max_scores.get(dim_name, 25),
                    'items': []  # 預估模式下不提供詳細項目
                }
            
            base_report.update({
                'is_difficult_site': True,
                'difficult_site_info': difficult_site_info,
                'estimated_score': estimated_total,
                'estimated_grade': estimated_grade,
                'estimated_dimensions': estimated_dimensions_full,
                'detection_status': 'failed',
                'detection_message': f'由於{difficult_site_info["reason"]},無法完整檢測網站信息。以下為基於網站類型的預估分數。'
            })
        else:
            base_report['is_difficult_site'] = False
        
        return base_report
    
    def _calculate_grade(self, signals: SiteSignals, issues_count: int) -> Tuple[str, int]:
        """計算可信度等級（使用加權評分）"""
        score = calculate_weighted_score(signals)
        grade = score_to_grade(score)
        return grade, score
    
    def _generate_conclusion(self, grade: str, issues_count: int) -> str:
        """產生一句話結論"""
        conclusions = {
            "A": "🎉 恭喜！你的網站已具備優秀的 AI 可信度結構",
            "B": "✅ 你的網站已具備基本可信結構，但仍有改善空間",
            "C": "⚠️ 你的網站缺少多項關鍵資訊，建議優先改善",
            "D": "❌ 目前你的網站尚未具備穩定的 AI 可引用可信度",
            "F": "🚫 分析失敗",
            "P": "⏳ 分析中..."
        }
        return conclusions.get(grade, "⏳ 分析中...")
