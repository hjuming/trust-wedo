from typing import List, Dict, Any, Tuple
from app.models.signals import SiteSignals
from app.services.scoring import calculate_weighted_score, score_to_grade
from app.services.site_classifier import classify_site_type, generate_custom_suggestions

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
    """報告引擎 v2.0"""
    
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
                condition=lambda s: s.schema_count == 0,
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
            )
        ]
    
    def generate_report(self, signals: SiteSignals) -> Dict[str, Any]:
        """產生報告（更新版）"""
        
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
        
        # 4. 計算評分
        grade, score = self._calculate_grade(signals, len(fired_rules))
        conclusion = self._generate_conclusion(grade, len(fired_rules))
        
        return {
            "report_version": self.VERSION,
            "signals": signals.model_dump(),
            "score": score,
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
            "suggestions": suggestions[:8]  # 限制建議數量
        }
    
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
            "D": "❌ 目前你的網站尚未具備穩定的 AI 可引用可信度"
        }
        return conclusions.get(grade, "⏳ 分析中...")
