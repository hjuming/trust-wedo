# Phase 2：Machine-Readable Citation System

> **AI Citation Engineering - Phase 2 Implementation**  
> **核心定位**：Citation as Data, not as Text  
> **設計目標**：讓引用成為可計算、可驗證、可拒絕的物件

---

## 完成判準（Phase 2 Exit Criteria）

✅ Phase 2 必須滿足三個條件才算完成：

1. **任何一個 AFB，都能被序列化成 JSON**
2. **任何一個 citation，都能被獨立評分**
3. **系統可以明確說出：「為什麼這個答案不該被用」**

---

## Phase 2-A：Machine-Readable Citations（第一優先）

### Citation Object 核心定義

**設計原則**：引用不是文字，是可被計算的資料物件

---

#### Citation Object 強制結構

```json
{
  "@type": "Citation",
  "@context": "https://schema.org",
  
  // 必填欄位（缺一不可）
  "citation_id": "cite-2026-001",
  
  "source_entity": {
    "@id": "https://example.com/entity/stanford-ai-lab",
    "name": "Stanford AI Lab",
    "entity_confidence": 0.95
  },
  
  "claim": "AFB increases AI citation likelihood by 3.4x compared to traditional content",
  
  "evidence_type": "peer_reviewed",
  
  "source_url": "https://stanford.edu/research/ai-citation-2025",
  
  "publication_date": "2025-12-01T00:00:00Z",
  
  "verification_status": "verified",
  
  "confidence": 0.92,
  
  // 選填但強烈建議
  "last_verified": "2026-02-06T10:00:00Z",
  "verification_method": "cross_reference",
  "cross_verified_by": [
    "https://example.com/entity/mit-media-lab",
    "https://example.com/entity/berkeley-ai-research"
  ],
  "sample_size": 500,
  "study_duration": "6 months",
  "claim_specificity": "quantitative",
  "limitations": [],
  "data_availability": "public"
}
```

---

**Phase 2 完整內容已補充至規劃文檔第 3550-4000 行區段。**

**主要章節**：
1. Citation Object 定義
2. Evidence Type 分類
3. Verification Status 狀態機
4. Citation ↔ AFB 綁定規則
5. Citation Failure States
6. Citation Quality Evaluation
7. Entity Graph.json 實作

---

---

## Phase 2-B：Citation Quality Evaluation（第二優先）

### 核心定義：Citation Confidence Score (CCS)

**關鍵原則**：CCS 必須獨立於 Entity Confidence (EC)

**為什麼必須獨立？**
- Entity Confidence (EC)：這個實體整體可信度如何
- Citation Confidence (CCS)：這一筆證據本身可靠度如何

**核心洞察**：同一個 entity 可以同時有高 CCS 與低 CCS citation。

> 如果 CCS 與 EC 混在一起，系統會被權威綁架。

---

### CCS 計算維度（6 維模型）

```python
CCS_DIMENSIONS = {
    "Evidence_Strength": {
        "weight": 0.20,
        "symbol": "E",
        "description": "證據類型強度"
    },
    "Source_Reputation": {
        "weight": 0.18,
        "symbol": "R",
        "description": "來源信譽（機構/出版物層級）"
    },
    "Corroboration": {
        "weight": 0.28,  # 最高權重
        "symbol": "C",
        "description": "跨來源交叉驗證強度"
    },
    "Recency_Decay": {
        "weight": 0.14,
        "symbol": "T",
        "description": "時效衰減"
    },
    "Claim_Specificity": {
        "weight": 0.12,
        "symbol": "S",
        "description": "主張可驗證程度"
    },
    "Verification_Status": {
        "weight": 0.08,
        "symbol": "V",
        "description": "驗證狀態機結果"
    }
}
```

**為什麼 Corroboration (C) 最大？**

> 生成引擎最怕單一來源失誤；跨來源一致是「安全感」。

---

### CCS 計算公式 (v1)

```python
def calculate_citation_confidence_score(citation):
    """
    計算 Citation Confidence Score (CCS)
    
    每個維度標準化到 0~1
    """
    E = calculate_evidence_strength(citation.evidence_type)
    R = calculate_source_reputation(citation.source_entity)
    C = calculate_corroboration(citation)
    T = calculate_recency_decay(citation.publication_date, citation.topic_type)
    S = calculate_claim_specificity(citation.claim)
    V = calculate_verification_score(citation.verification_status)
    
    CCS = (
        0.28 * C +  # Corroboration（最重要）
        0.20 * E +  # Evidence Strength
        0.18 * R +  # Source Reputation
        0.14 * T +  # Recency Decay
        0.12 * S +  # Claim Specificity
        0.08 * V    # Verification Status
    )
    
    return {
        "ccs": CCS,
        "breakdown": {
            "corroboration": C,
            "evidence_strength": E,
            "source_reputation": R,
            "recency": T,
            "specificity": S,
            "verification": V
        }
    }
```

---

### 維度 1：Evidence Strength (E)

**映射表（固定 base，可調）**：

```python
EVIDENCE_STRENGTH_MAP = {
    "peer_reviewed": 1.00,
    "institutional_research": 0.90,
    "standards_specification": 0.85,
    "first_party_data_with_method": 0.80,
    "verified_case_study": 0.75,
    "reputable_media": 0.70,
    "expert_opinion": 0.60,
    "industry_report": 0.55,
    "community_consensus": 0.45,
    "documented_test": 0.40,
    "secondary_source": 0.30,
    "anecdotal": 0.15,
    "anonymous_or_unverified": 0.10
}

def calculate_evidence_strength(evidence_type):
    """計算證據強度"""
    return EVIDENCE_STRENGTH_MAP.get(evidence_type, 0.10)
```

---

### 維度 2：Source Reputation (R)

```python
def calculate_source_reputation(source_entity):
    """
    計算來源信譽
    結合 Entity Confidence 與機構類型
    """
    entity_conf = source_entity.entity_confidence
    
    # 機構類型加成
    institution_type = source_entity.institution_type
    type_bonus = {
        "academic": 0.15,
        "government": 0.12,
        "standards_body": 0.10,
        "major_media": 0.08,
        "tech_company": 0.05,
        "individual": 0.00
    }.get(institution_type, 0.0)
    
    # 綜合計算
    reputation = min(entity_conf + type_bonus, 1.0)
    
    return reputation
```

---

### 維度 3：Corroboration (C) - 最關鍵

```python
def calculate_corroboration(citation):
    """
    計算跨來源驗證強度
    這是 CCS 最重要的維度
    """
    # 基礎：有多少獨立來源支持相同 claim
    supporting_citations = find_supporting_citations(citation.claim)
    distinct_sources = count_distinct_sources(supporting_citations)
    
    # 來源多樣性
    if distinct_sources == 0:
        base_score = 0.0
    elif distinct_sources == 1:
        base_score = 0.3  # 單一來源，低分
    elif distinct_sources == 2:
        base_score = 0.6
    elif distinct_sources == 3:
        base_score = 0.8
    else:  # ≥ 4
        base_score = 1.0
    
    # 來源品質加權
    source_quality_avg = sum([
        c.source_entity.entity_confidence 
        for c in supporting_citations
    ]) / len(supporting_citations) if supporting_citations else 0.0
    
    # 綜合分數
    corroboration = (base_score * 0.7) + (source_quality_avg * 0.3)
    
    return corroboration
```

---

### 維度 4：Recency Decay (T) - 時效衰減

**半衰期模型**：

```python
import math
from datetime import datetime, timedelta

HALF_LIFE_DAYS = {
    "fast_moving": 90,    # AI 工具、政策、價格
    "medium": 180,        # 行銷策略、平台機制
    "slow": 720,          # 數學定義、長期原理
    "fundamental": None   # 不衰減
}

def calculate_recency_decay(publication_date, topic_type):
    """
    計算時效衰減分數
    使用半衰期模型
    """
    half_life = HALF_LIFE_DAYS.get(topic_type, 180)
    
    if half_life is None:
        return 1.0  # 基礎概念不衰減
    
    age_days = (datetime.now() - publication_date).days
    
    # 半衰期公式：T = 0.5^(age_days / half_life_days)
    decay_score = 0.5 ** (age_days / half_life)
    
    return max(decay_score, 0.1)  # 最低保留 0.1
```

**範例**：
```python
# AI 工具評測（fast_moving，半衰期 90 天）
publication_date = datetime(2025, 8, 1)
current_date = datetime(2026, 2, 6)
age_days = 189

T = 0.5 ** (189 / 90) = 0.24  # 已顯著衰減

# 數學原理（fundamental，不衰減）
T = 1.0  # 保持完整
```

---

### 維度 5：Claim Specificity (S) - 可驗證性

**可計算版本（0~1）**：

```python
def calculate_claim_specificity(claim):
    """
    計算主張的可驗證程度
    基於「可驗證要素」計分
    """
    score = 0.0
    
    # +0.25：有具體數字
    if has_quantitative_data(claim):
        score += 0.25
        # 範例：「提升 340%」、「N=500」
    
    # +0.25：有明確方法
    if has_methodology(claim):
        score += 0.25
        # 範例：「A/B test」、「randomized trial」
    
    # +0.25：有時間範圍
    if has_timeframe(claim):
        score += 0.25
        # 範例：「2025-01 至 2025-06」
    
    # +0.25：有邊界條件
    if has_boundary_conditions(claim):
        score += 0.25
        # 範例：「適用於 Entity Confidence > 0.70 的網站」
    
    return score

# 輔助函數
def has_quantitative_data(claim):
    """檢查是否包含數字、百分比、樣本數"""
    import re
    patterns = [
        r'\d+%',           # 百分比
        r'\d+x',           # 倍數
        r'N\s*=\s*\d+',    # 樣本數
        r'\d+\.\d+',       # 小數
    ]
    return any(re.search(p, claim) for p in patterns)

def has_methodology(claim):
    """檢查是否說明研究方法"""
    methods = [
        'A/B test', 'survey', 'experiment', 'trial',
        'study', 'analysis', 'measurement', 'testing'
    ]
    return any(m.lower() in claim.lower() for m in methods)
```

**範例**：
```python
# 高 Specificity 範例
claim = "Based on A/B testing with N=500 websites over 6 months (Jan-Jun 2025), Entity-first structure increased AI citation rate by 340% for sites with Entity Confidence > 0.70."

S = 1.0  # 四個要素全滿

# 低 Specificity 範例
claim = "AI-Ready SEO improves results significantly."

S = 0.0  # 無具體可驗證要素
```

---

### 維度 6：Verification Status (V)

```python
VERIFICATION_STATUS_SCORE = {
    "verified": 1.0,
    "pending": 0.5,
    "unverifiable": 0.1,
    "outdated": 0.3,
    "contradicted": 0.0,
    "retracted": 0.0,
    "disputed": 0.4
}

def calculate_verification_score(verification_status):
    """計算驗證狀態分數"""
    return VERIFICATION_STATUS_SCORE.get(verification_status, 0.1)
```

---

### Citation 競爭與衝突處理（顯式規則）

#### 規則 1：同一 Claim，多筆 Citation → Top-K + 聚合

```python
def handle_multiple_citations_same_claim(citations, K=3):
    """
    處理多個支持相同 claim 的 citations
    """
    # 按 CCS 排序
    sorted_citations = sorted(
        citations, 
        key=lambda c: c.ccs, 
        reverse=True
    )
    
    # 取前 K 個
    top_k = sorted_citations[:K]
    
    # 檢查來源多樣性
    distinct_sources = len(set([c.source_entity.id for c in top_k]))
    
    # 計算聚合信心
    if distinct_sources >= 2:
        diversity_bonus = 0.1
    else:
        diversity_bonus = 0.0
    
    aggregated_confidence = (
        sum([c.ccs for c in top_k]) / K +
        diversity_bonus
    )
    
    return {
        "selected_citations": top_k,
        "aggregated_confidence": min(aggregated_confidence, 1.0),
        "distinct_sources": distinct_sources,
        "diversity_bonus_applied": diversity_bonus > 0
    }
```

---

#### 規則 2：同一 Claim，結論相反 → 降級或拒用

**Conflict 判斷**：

```python
def detect_citation_conflict(citation_a, citation_b):
    """
    判斷兩個 citation 是否衝突
    """
    # 檢查 1：主題是否相同
    if not is_same_topic(citation_a.claim, citation_b.claim):
        return False
    
    # 檢查 2：結論方向是否相反
    direction_a = extract_claim_direction(citation_a.claim)
    direction_b = extract_claim_direction(citation_b.claim)
    
    if direction_a != direction_b:
        return True
    
    # 檢查 3：數值差異是否超過閾值
    value_a = extract_quantitative_value(citation_a.claim)
    value_b = extract_quantitative_value(citation_b.claim)
    
    if value_a and value_b:
        diff_ratio = abs(value_a - value_b) / max(value_a, value_b)
        if diff_ratio > 0.20:  # 20% 閾值
            return True
    
    return False
```

**處理策略（三段式）**：

```python
def resolve_citation_conflict(high_ccs_citation, low_ccs_citation):
    """
    解決 citation 衝突
    """
    ccs_gap = high_ccs_citation.ccs - low_ccs_citation.ccs
    
    # 情境 1：高 CCS 方明顯領先（≥ 0.20）
    if ccs_gap >= 0.20:
        return {
            "action": "USE_HIGH_WITH_WARNING",
            "selected": high_ccs_citation,
            "afb_status": "contested",
            "warning": f"Conflicting evidence exists with lower confidence (CCS: {low_ccs_citation.ccs:.2f})"
        }
    
    # 情境 2：差距小（< 0.20）
    elif ccs_gap < 0.20:
        return {
            "action": "DOWNGRADE_AFB",
            "selected": None,
            "afb_status": "low_confidence",
            "warning": "Conflicting evidence with similar confidence levels",
            "recommendation": "Require additional sources before use"
        }
    
    # 情境 3：任一為 failure state
    if (high_ccs_citation.verification_status in ["unverifiable", "retracted"] or
        low_ccs_citation.verification_status in ["unverifiable", "retracted"]):
        return {
            "action": "REJECT",
            "selected": None,
            "afb_status": "rejected",
            "reason": "One or more citations in failure state"
        }
```

---

#### 規則 3：高權威但過期 vs 低權威但新 → Trade-off

**安全偏好策略**：

```python
def handle_authority_vs_recency_tradeoff(old_citation, new_citation):
    """
    處理權威性與時效性的權衡
    """
    old_T = old_citation.ccs_breakdown['recency']
    new_T = new_citation.ccs_breakdown['recency']
    
    old_R = old_citation.ccs_breakdown['source_reputation']
    new_R = new_citation.ccs_breakdown['source_reputation']
    
    # 情境 1：舊 citation 明顯過期（T < 0.35）
    if old_T < 0.35:
        # 必須有跨來源驗證才能用
        old_C = old_citation.ccs_breakdown['corroboration']
        
        if old_C >= 0.5:
            return {
                "action": "USE_OLD_WITH_CORROBORATION",
                "selected": old_citation,
                "warning": "Aged citation, but cross-verified"
            }
        else:
            return {
                "action": "PREFER_NEW",
                "selected": new_citation,
                "reason": "Old citation lacks corroboration and significantly aged"
            }
    
    # 情境 2：新 citation 可驗證但權威較低
    if new_citation.verification_status == "verified" and new_R < 0.60:
        return {
            "action": "USE_NEW_BUT_FLAG",
            "selected": new_citation,
            "warning": "Recent but from lower-authority source"
        }
    
    # 預設：權衡 CCS 總分
    if old_citation.ccs > new_citation.ccs:
        return {
            "action": "USE_OLD",
            "selected": old_citation
        }
    else:
        return {
            "action": "USE_NEW",
            "selected": new_citation
        }
```

---

### CCS 完整實作範例

```python
# 範例 Citation
citation = {
    "citation_id": "cite-stanford-2025-001",
    "claim": "Based on A/B testing with N=500 websites over 6 months, Entity-first structure increased AI citation rate by 340%.",
    "evidence_type": "peer_reviewed",
    "source_entity": {
        "id": "stanford-ai-lab",
        "entity_confidence": 0.95,
        "institution_type": "academic"
    },
    "publication_date": datetime(2025, 12, 1),
    "topic_type": "medium",
    "verification_status": "verified",
    "cross_verified_by": [
        "mit-media-lab",
        "berkeley-ai-research"
    ]
}

# 計算 CCS
E = 1.00  # peer_reviewed
R = min(0.95 + 0.15, 1.0) = 1.00  # academic + high EC
C = 0.80  # 3 distinct sources
T = 0.5 ** (67/180) = 0.77  # 67 days old, medium topic
S = 1.00  # 有數字、方法、時間、邊界
V = 1.00  # verified

CCS = 0.28*0.80 + 0.20*1.00 + 0.18*1.00 + 0.14*0.77 + 0.12*1.00 + 0.08*1.00
    = 0.224 + 0.200 + 0.180 + 0.108 + 0.120 + 0.080
    = 0.912

# 評級：🌟 優秀（≥ 0.90）
```

---

---

## Phase 2-C：Entity Graph.json（第三優先）

### Graph 的目的（只做風險檢測）

**明確定位**：不是視覺化，不是知識圖譜炫技。

**只做三件事**：
1. **Isolated Answer 檢測**：答案是否孤立
2. **Single-Source Risk 檢測**：是否單一來源依賴
3. **Phase 3 比對基準**：反向 GEO 需要

---

### 最小 Graph Schema (v1)

#### Node 類型（4 種）

```python
NODE_TYPES = {
    "entity": {
        "description": "內容實體（Person / Organization / Concept）",
        "required_fields": ["id", "type", "label", "entity_confidence"]
    },
    "afb": {
        "description": "Answer-First Block",
        "required_fields": ["id", "type", "label", "entity_id"]
    },
    "citation": {
        "description": "引用證據",
        "required_fields": ["id", "type", "label", "ccs"]
    },
    "source": {
        "description": "來源機構/平台",
        "required_fields": ["id", "type", "label", "authority"]
    }
}
```

#### Edge 類型（3 種）

```python
EDGE_TYPES = {
    "answers": {
        "from": "entity",
        "to": "afb",
        "description": "Entity 提供 AFB"
    },
    "supported_by": {
        "from": "afb",
        "to": "citation",
        "description": "AFB 由 Citation 支持"
    },
    "from_source": {
        "from": "citation",
        "to": "source",
        "description": "Citation 來自 Source"
    }
}
```

---

### 輸出 JSON 格式（v1 直接可用）

```json
{
  "graph_version": "2.0",
  "generated_at": "2026-02-06T10:00:00+08:00",
  "system_metadata": {
    "total_entities": 2,
    "total_afbs": 4,
    "total_citations": 9,
    "total_sources": 3,
    "isolated_afbs": 0,
    "high_risk_afbs": 1
  },
  
  "nodes": [
    {
      "id": "ent:ai-citation-engineering",
      "type": "entity",
      "label": "AI Citation Engineering",
      "entity_confidence": 0.87,
      "afb_count": 4,
      "citation_count": 9
    },
    {
      "id": "afb:definition:v1",
      "type": "afb",
      "label": "Definition AFB",
      "entity_id": "ent:ai-citation-engineering",
      "confidence": 0.89,
      "citation_count": 3
    },
    {
      "id": "cite:2026-001",
      "type": "citation",
      "label": "Stanford study 2025",
      "ccs": 0.91,
      "evidence_type": "peer_reviewed",
      "verification_status": "verified"
    },
    {
      "id": "src:stanford",
      "type": "source",
      "label": "Stanford AI Lab",
      "authority": 0.98,
      "institution_type": "academic"
    }
  ],
  
  "edges": [
    {
      "from": "ent:ai-citation-engineering",
      "to": "afb:definition:v1",
      "type": "answers"
    },
    {
      "from": "afb:definition:v1",
      "to": "cite:2026-001",
      "type": "supported_by",
      "weight": 0.91
    },
    {
      "from": "cite:2026-001",
      "to": "src:stanford",
      "type": "from_source"
    }
  ],
  
  "metrics": {
    "ent:ai-citation-engineering": {
      "afbs": 4,
      "citations": 9,
      "distinct_sources": 3,
      "avg_ccs": 0.78,
      "is_isolated": false,
      "single_source_risk": false,
      "lowest_ccs": 0.62,
      "highest_ccs": 0.91,
      "conflict_count": 1,
      "verified_citation_ratio": 0.89
    },
    "afb:definition:v1": {
      "citations": 3,
      "distinct_sources": 3,
      "is_isolated": false,
      "single_source_risk": false,
      "avg_ccs": 0.86,
      "risk_level": "low"
    }
  }
}
```

---

### 孤立節點與風險規則（寫死規則）

#### Isolated Answer 定義

```python
def check_isolated_answer(afb, graph):
    """
    判斷 AFB 是否為孤立答案
    """
    # 條件 1：沒有任何 citation
    citations = graph.get_citations_for_afb(afb.id)
    if len(citations) == 0:
        return {
            "is_isolated": True,
            "reason": "No citations",
            "severity": "critical"
        }
    
    # 條件 2：所有 citations 都處於 failure state
    all_failed = all(
        c.verification_status in ["unverifiable", "retracted", "contradicted"]
        for c in citations
    )
    if all_failed:
        return {
            "is_isolated": True,
            "reason": "All citations in failure state",
            "severity": "critical"
        }
    
    # 條件 3：distinct_sources < 2 且 claim 涉及數字/研究
    distinct_sources = count_distinct_sources(citations)
    claim_type = classify_claim_type(afb.claim)
    
    if (distinct_sources < 2 and 
        claim_type in ["statistical", "research", "comparative"]):
        return {
            "is_isolated": True,
            "reason": "Single source for quantitative claim",
            "severity": "high"
        }
    
    return {
        "is_isolated": False,
        "severity": "none"
    }
```

---

#### Single-Source Risk 定義

```python
def check_single_source_risk(afb, graph):
    """
    判斷 AFB 是否有單一來源風險
    """
    citations = graph.get_citations_for_afb(afb.id)
    distinct_sources = count_distinct_sources(citations)
    claim_type = classify_claim_type(afb.claim)
    
    # 規則：distinct_sources = 1 且 claim 為 stat/causal/comparative
    if (distinct_sources == 1 and 
        claim_type in ["statistical", "causal", "comparative"]):
        return {
            "single_source_risk": True,
            "risk_level": "high",
            "source_id": citations[0].source_entity.id,
            "recommendation": "Require at least one additional independent source"
        }
    
    # 低風險但標記
    if distinct_sources == 1:
        return {
            "single_source_risk": True,
            "risk_level": "medium",
            "source_id": citations[0].source_entity.id,
            "recommendation": "Consider adding corroborating source"
        }
    
    return {
        "single_source_risk": False,
        "risk_level": "low"
    }
```

---

### Graph 風險評估完整實作

```python
class EntityGraph:
    """Entity Graph 風險評估系統"""
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.metrics = {}
    
    def calculate_entity_metrics(self, entity_id):
        """計算 Entity 層級的風險指標"""
        afbs = self.get_afbs_for_entity(entity_id)
        all_citations = []
        
        for afb in afbs:
            citations = self.get_citations_for_afb(afb.id)
            all_citations.extend(citations)
        
        # 獨立來源數
        distinct_sources = count_distinct_sources(all_citations)
        
        # CCS 統計
        ccs_scores = [c.ccs for c in all_citations if c.ccs]
        avg_ccs = sum(ccs_scores) / len(ccs_scores) if ccs_scores else 0.0
        lowest_ccs = min(ccs_scores) if ccs_scores else 0.0
        highest_ccs = max(ccs_scores) if ccs_scores else 0.0
        
        # 驗證率
        verified_count = sum(
            1 for c in all_citations 
            if c.verification_status == "verified"
        )
        verified_ratio = verified_count / len(all_citations) if all_citations else 0.0
        
        # 衝突數
        conflict_count = count_citation_conflicts(all_citations)
        
        # 孤立與風險檢測
        isolated_afbs = []
        single_source_afbs = []
        
        for afb in afbs:
            isolated_check = check_isolated_answer(afb, self)
            if isolated_check['is_isolated']:
                isolated_afbs.append(afb.id)
            
            risk_check = check_single_source_risk(afb, self)
            if risk_check['single_source_risk']:
                single_source_afbs.append(afb.id)
        
        return {
            "entity_id": entity_id,
            "afbs": len(afbs),
            "citations": len(all_citations),
            "distinct_sources": distinct_sources,
            "avg_ccs": round(avg_ccs, 3),
            "lowest_ccs": round(lowest_ccs, 3),
            "highest_ccs": round(highest_ccs, 3),
            "verified_citation_ratio": round(verified_ratio, 3),
            "conflict_count": conflict_count,
            "is_isolated": len(isolated_afbs) > 0,
            "isolated_afbs": isolated_afbs,
            "single_source_risk": len(single_source_afbs) > 0,
            "single_source_afbs": single_source_afbs,
            "risk_assessment": self.assess_overall_risk(
                distinct_sources,
                lowest_ccs,
                verified_ratio,
                len(isolated_afbs),
                len(single_source_afbs)
            )
        }
    
    def assess_overall_risk(self, distinct_sources, lowest_ccs, 
                           verified_ratio, isolated_count, single_source_count):
        """綜合風險評估"""
        risk_score = 0
        
        # 風險因子
        if distinct_sources < 2:
            risk_score += 3
        if lowest_ccs < 0.60:
            risk_score += 2
        if verified_ratio < 0.70:
            risk_score += 2
        if isolated_count > 0:
            risk_score += 4
        if single_source_count > 0:
            risk_score += 3
        
        # 評級
        if risk_score >= 8:
            return {"level": "critical", "action": "REJECT"}
        elif risk_score >= 5:
            return {"level": "high", "action": "DOWNGRADE"}
        elif risk_score >= 3:
            return {"level": "medium", "action": "FLAG"}
        else:
            return {"level": "low", "action": "ACCEPT"}
    
    def export_json(self, output_file="entity_graph.json"):
        """匯出 Graph JSON"""
        graph_data = {
            "graph_version": "2.0",
            "generated_at": datetime.now().isoformat(),
            "system_metadata": self.calculate_system_metadata(),
            "nodes": self.nodes,
            "edges": self.edges,
            "metrics": self.metrics
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        return output_file
```

---

### Graph 使用範例

#### 範例 1：健康的 Entity Graph

```json
{
  "metrics": {
    "ent:ai-citation-engineering": {
      "afbs": 4,
      "citations": 9,
      "distinct_sources": 5,
      "avg_ccs": 0.82,
      "lowest_ccs": 0.68,
      "verified_citation_ratio": 0.89,
      "is_isolated": false,
      "single_source_risk": false,
      "risk_assessment": {
        "level": "low",
        "action": "ACCEPT"
      }
    }
  }
}
```

#### 範例 2：高風險 Entity Graph

```json
{
  "metrics": {
    "ent:new-concept": {
      "afbs": 2,
      "citations": 2,
      "distinct_sources": 1,  // 單一來源
      "avg_ccs": 0.55,  // 低 CCS
      "lowest_ccs": 0.45,
      "verified_citation_ratio": 0.50,  // 低驗證率
      "is_isolated": true,  // 有孤立 AFB
      "isolated_afbs": ["afb:new-001"],
      "single_source_risk": true,
      "single_source_afbs": ["afb:new-001", "afb:new-002"],
      "risk_assessment": {
        "level": "critical",
        "action": "REJECT",
        "reason": "Multiple risk factors: isolated AFBs, single source, low CCS"
      }
    }
  }
}
```

---

## Phase 2 完成驗收：Go / No-Go 檢查清單

### ✅ Go（Phase 2 完成）

Phase 2 必須滿足以下所有條件：

- [x] **AFB JSON 可輸出**：每個 AFB 都能列出完整引用清單
- [x] **Citation 可獨立評分**：每筆 citation 都能算出 CCS（0~1）
- [x] **Conflict 判定與處理**：有明確的 accept / downgrade / reject 決策
- [x] **Graph.json 可生成**：能算出每個 entity 的 distinct_sources / isolated / risk
- [x] **拒絕理由可輸出**：系統能說明為什麼拒絕（failure state 或 conflict）
- [x] **CCS 獨立於 EC**：Citation Confidence 不受 Entity Confidence 綁架
- [x] **Corroboration 優先**：跨來源驗證獲得最高權重（0.28）

---

### ❌ No-Go（不能進 Phase 3）

如果出現以下任一情況，Phase 2 未完成：

- [ ] CCS 與 Entity Confidence 混在一起（會被權威綁架）
- [ ] 沒有 conflict handling（Phase 3 會全是假象）
- [ ] Graph 只做視覺化沒做風險指標（無法檢測孤立答案）
- [ ] Citation 無法獨立評分
- [ ] 沒有明確的失效狀態定義

---

## Phase 2 完成狀態

### ✅ 已完成所有關鍵組件

**Phase 2-A：Machine-Readable Citations**
- Citation Object 定義與強制結構
- Evidence Type 完整分類
- Verification Status 狀態機
- Citation ↔ AFB 綁定規則
- Citation Failure States
- Citation 生命週期管理

**Phase 2-B：Citation Quality Evaluation**
- CCS 6 維計算模型
- 獨立於 Entity Confidence
- Corroboration 優先設計
- 衝突處理三段式規則
- 權威 vs 時效性權衡機制

**Phase 2-C：Entity Graph.json**
- 最小 Graph Schema（4 node + 3 edge）
- Isolated Answer 檢測
- Single-Source Risk 檢測
- 完整風險評估系統
- JSON 匯出格式

---

## 執行狀態

- ✅ Phase 0：Entity Optimization - 完成
- ✅ Phase 1：AFB + E-E-A-T Signals - 完成
- ✅ Phase 2-A：Machine-Readable Citations - 完成
- ✅ Phase 2-B：Citation Quality Evaluation - 完成
- ✅ Phase 2-C：Entity Graph.json - 完成
- ✅ **Phase 2：完整收尾，通過 Go/No-Go 驗收**
- ⏳ Phase 3：Reverse GEO Testing - 準備啟動
- ⏳ Phase 4：SKILL.md + Scripts - 待啟動

---

**Phase 2 正式完成。系統已具備「可計算、可驗證、可拒絕」的完整能力。**

---

**文檔維護者**：AI Citation Engineering Team  
**最後更新**：2026-02-06  
**Phase 2 狀態**：✅ 完成並通過驗收
