"""
Schema.org analyzer for deep content structure evaluation.
"""
from typing import List, Dict, Any

# Required fields for common types
SCHEMA_REQUIRED_FIELDS = {
    'Organization': ['name', 'url', 'logo', 'description'],
    'LocalBusiness': ['name', 'image', 'address', 'telephone'],
    'Article': ['headline', 'author', 'datePublished', 'image'],
    'NewsArticle': ['headline', 'author', 'datePublished', 'image'],
    'BlogPosting': ['headline', 'author', 'datePublished'],
    'Product': ['name', 'image', 'description', 'offers'],
    'Person': ['name', 'jobTitle', 'worksFor'],
    'BreadcrumbList': ['itemListElement'],
    'FAQPage': ['mainEntity'],
    'JobPosting': ['title', 'description', 'datePosted'],
    'Event': ['name', 'startDate', 'location'],
    'Recipe': ['name', 'image', 'author', 'recipeIngredient'],
    'Review': ['author', 'reviewRating', 'itemReviewed'],
    'WebSite': ['name', 'url', 'potentialAction'],
}

class SchemaAnalyzer:
    @staticmethod
    def analyze(schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze Schema.org data for completeness and quality.
        Returns detailed score breakdown (Max 30 points).
        """
        score = 0
        details = []
        
        if not schemas:
            return {
                "score": 0, 
                "max_score": 30, 
                "details": ["未偵測到 Schema.org 結構化資料"], 
                "completeness": 0
            }
            
        # 1. Existence (5 pts)
        score += 5
        details.append("已偵測到 Schema.org 結構化資料 (+5)")
        
        # 2. Diversity (Max 8 pts)
        types = set()
        for s in schemas:
            t = s.get('@type')
            if isinstance(t, list):
                types.update(t)
            elif t:
                types.add(t)
                
        diversity_score = min(len(types) * 2, 8)
        score += diversity_score
        type_str = ", ".join(list(types)[:3]) + ("..." if len(types) > 3 else "")
        details.append(f"包含 {len(types)} 種不同類型的 Schema ({type_str}) (+{diversity_score})")
        
        # 3. Completeness & Quality (Max 10 pts)
        completeness_scores = []
        for s in schemas:
             t = s.get('@type')
             if isinstance(t, list) and t:
                 t = t[0]
                 
             if t in SCHEMA_REQUIRED_FIELDS:
                 req = SCHEMA_REQUIRED_FIELDS[t]
                 present = [f for f in req if s.get(f)]
                 if req:
                     ratio = len(present) / len(req)
                     completeness_scores.append(ratio)
                 
        avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.5
        # If no known types to check, assume partial completeness (0.5)
        
        quality_score = min(round(avg_completeness * 10), 10)
        score += quality_score
        
        percentage = int(avg_completeness * 100)
        if percentage >= 80:
            details.append(f"Schema 資料欄位完整度極高 ({percentage}%) (+{quality_score})")
        elif percentage >= 50:
            details.append(f"Schema 資料欄位完整度良好 ({percentage}%) (+{quality_score})")
        else:
            details.append(f"Schema 資料欄位有缺失，建議補全 ({percentage}%) (+{quality_score})")
        
        # 4. Hierarchy / Nesting (Bonus Max 5 pts)
        nesting_found = False
        for s in schemas:
            for k, v in s.items():
                if isinstance(v, dict) and '@type' in v:
                    nesting_found = True
                    break
                if isinstance(v, list) and v and isinstance(v[0], dict) and '@type' in v[0]:
                    nesting_found = True
                    break
            if nesting_found:
                break
                
        if nesting_found:
            score += 5
            details.append("偵測到豐富的巢狀結構 (Nested Structure) (+5)")
        
        # 5. Core Types Bonus (Max 2 pts)
        # Reward having Organization or WebSite implies basic setup is done
        if 'Organization' in types or 'WebSite' in types or 'LocalBusiness' in types:
            score += 2
            details.append("包含核心識別資料 (Organization/WebSite) (+2)")
            
        # Cap at 30
        final_score = min(score, 30)
        
        return {
            "score": final_score,
            "max_score": 30,
            "types": list(types),
            "details": details,
            "completeness": avg_completeness
        }
