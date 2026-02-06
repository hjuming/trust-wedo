---
name: ai-citation-engineering
description: Answer Trust Infrastructure for Generative Systems. Engineering your content to become part of AI-generated answers. Use when optimizing content for AI search engines (ChatGPT, Perplexity, Google AI), building Entity trust, creating Answer-First Blocks, or implementing machine-readable citations. This is not advanced SEO - it's Answer-Layer Engineering.
license: MIT
metadata:
  version: 0.5.0
  author: AI Citation Engineering Team
  category: ai-optimization
  domain: answer-trust-infrastructure
  updated: 2026-02-06
  status: Phase 3 - Testing
  tech-stack: Entity-Optimization, AFB, Citation-System, JSON-LD, Schema.org
---

# AI Citation Engineering

> **Answer Trust Infrastructure for Generative Systems**

Engineering your content to become part of AI-generated answers.

---

## 關鍵詞

ai citation engineering, ai-ready seo, geo, generative engine optimization, entity optimization, answer-first block, afb, citation confidence score, entity confidence, machine-readable citations, ai search, chatgpt seo, perplexity optimization, google ai overview, answer layer, trust infrastructure, e-e-a-t signals, schema markup, knowledge graph

---

## 核心定位

**這不是「進階 SEO」，而是 AI 答案層工程（Answer-Layer Engineering）的實作規範。**

### 本質區別

- ❌ 傳統 SEO：優化「搜尋結果頁」排名
- ✅ Citation Engineering：進入「答案生成層」，成為 AI 的知識來源

**一句話定位**：

> 我不是幫你排第一名，我是幫你進 AI 的答案層。

---

## 何時使用此技能

### ✅ 應該使用

當用戶提到以下任何關鍵字或場景：
- AI 搜尋引擎優化、GEO、AI-Ready SEO
- ChatGPT、Perplexity、Google AI Overview、Claude 搜尋
- Entity 優化、Entity Confidence
- 被 AI 引用、AI 引用率
- Answer-First Block、AFB
- Machine-readable citations
- 結構化資料優化（針對 AI）
- 如何讓 AI 引用我的內容
- 零點擊搜尋策略
- Knowledge Graph 優化

### ❌ 不應使用

- 傳統 Google SEO 優化（使用 `seo-audit`）
- 關鍵字研究（使用 `seo-content-writer`）
- 文案撰寫（使用 `copywriting`）
- 單純的 Schema 標記（屬於技術 SEO）

---

## 快速開始

### 步驟 1：評估適用性（5 分鐘）

回答三個問題：
1. 你的目標客戶會使用 AI 搜尋嗎？
2. 你願意投資建立長期權威嗎？
3. 你能提供可驗證的專業內容嗎？

**如果都是 Yes** → 繼續  
**如果有 No** → 閱讀 `docs/EXECUTIVE_SUMMARY.md` 評估 ROI

---

### 步驟 2：建立 Entity（第一優先）

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://yoursite.com/entity/your-name",
  "name": "你的名字",
  "jobTitle": "你的職稱",
  "sameAs": [
    "https://linkedin.com/in/you",
    "https://twitter.com/you",
    "https://github.com/you",
    "https://scholar.google.com/citations?user=xxx"
  ]
}
```

**目標**：Entity Confidence ≥ 0.70

**檢查**：跨平台一致性 ≥ 0.95

---

### 步驟 3：創建 Answer-First Block

```markdown
## Answer-First Block

### AI Quick Answer
[30 字以內的完整答案]

### Context Fit
**適用問題類型**：
- `definition` - "什麼是 X？"
- `how_to` - "如何做 Y？"

**不適用情境**：
- ⚠️ [明確列出不適用場景]

### Confidence Signals
```json
{
  "entity_confidence": 0.87,
  "citation_sources": 3,
  "last_verified": "2026-02-06"
}
```

### Machine-Readable Payload
```json
{
  "@type": "Answer",
  "text": "...",
  "author": {"@id": "entity_uri"}
}
```
```

---

### 步驟 4：添加 Machine-Readable Citations

```json
{
  "@type": "Citation",
  "citation_id": "cite-001",
  "source_entity": {...},
  "claim": "具體聲明",
  "evidence_type": "peer_reviewed",
  "confidence": 0.92,
  "verification_status": "verified"
}
```

**目標**：Citation Confidence Score ≥ 0.70

---

## 核心概念

### 1. Entity Confidence Score (EC)

**公式**：
```
EC = Consistency(0.30) + Authority(0.25) + Citation(0.20) 
     + Frequency(0.15) + Social(0.10)
```

**門檻**：
- ≥ 0.90：🌟 權威
- ≥ 0.70：🟢 及格
- < 0.60：🔴 不及格（不生成 AFB）

**詳細文檔**：`docs/AI_READY_SEO_PLANNING.md` - Entity Confidence Model

---

### 2. Answer-First Block (AFB)

**定義**：在生成過程中可以被單獨拉走、不需要上下文的 Answer Object

**四層強制結構**：
1. AI Quick Answer（≤30 字）
2. Context Fit（適用/不適用）
3. Confidence Signals（JSON）
4. Machine-Readable Payload（JSON-LD）

**資格門檻**：Entity Confidence ≥ 0.60

**詳細文檔**：`docs/AI_READY_SEO_PLANNING.md` - 策略 1

---

### 3. Citation Confidence Score (CCS)

**公式**：
```
CCS = Corroboration(0.28) + Evidence(0.20) + Reputation(0.18) 
      + Recency(0.14) + Specificity(0.12) + Verification(0.08)
```

**關鍵**：CCS 獨立於 Entity Confidence（避免被權威綁架）

**門檻**：
- ≥ 0.90：🌟 優秀
- ≥ 0.70：🟢 可用
- < 0.60：🔴 拒絕

**詳細文檔**：`docs/AI_CITATION_ENGINEERING_PHASE2.md`

---

## 核心工作流程

### Workflow 1：新內容創建（完整流程）

```
1. 建立/驗證 Entity（Entity Confidence ≥ 0.70）
   ↓
2. 創建內容初稿
   ↓
3. 重組為 AFB 格式（四層結構）
   ↓
4. 添加高品質 Citations（CCS ≥ 0.70）
   ↓
5. 生成 Entity Graph（風險檢測）
   ↓
6. 發布 + 驗證（Reverse GEO Testing）
```

---

### Workflow 2：現有內容 AI 優化

```
1. 評估 Entity Confidence
   ↓（如果 < 0.60）
   ├─ 先提升 Entity（建立跨平台一致性）
   ↓（如果 ≥ 0.60）
2. 選擇核心頁面（5-10 頁）
   ↓
3. 重組為 AFB 格式
   ↓
4. 添加/優化 Citations
   ↓
5. 驗證風險（Isolated Answer, Single-Source Risk）
   ↓
6. 發布更新
```

---

## 關鍵原則

### 設計原則（不可妥協）

1. **Entity First, Content Second**  
   先建立可信的 Entity，再產出內容

2. **Signals > Claims**  
   可驗證的信號比聲明重要

3. **可計算 > 可讀**  
   機器可計算比人類可讀重要

4. **系統可以拒絕自己**  
   條件不足時，不生成 AFB / 不使用 Citation

5. **驗證 > 優化**  
   先驗證預測準確度，再調整參數

---

### 執行原則

1. **不要跳過 Entity 建立**  
   沒有 Entity，你連被考慮的資格都沒有

2. **不要省略 Machine-Readable Payload**  
   這是 AFB 的核心，不是裝飾

3. **不要忽視 Failure States**  
   系統能說「為什麼不該用」比說「可以用」更重要

4. **不要在 Phase 3 之前調參數**  
   先收集 30-50 個真實樣本

5. **不要混淆 EC 與 CCS**  
   Entity 信任度 ≠ Citation 信任度

---

## 檢查清單

### Entity 檢查清單

```bash
✅ Entity 建立檢查：

□ 有唯一的 @id（URI）？
□ 跨平台一致性 ≥ 0.95？
□ 至少 5 個 sameAs 連結？
□ 包含 LinkedIn + 1 個權威平台？
□ Entity Confidence ≥ 0.70？
□ 有 Entity 專屬頁面？
```

---

### AFB 檢查清單

```bash
✅ AFB 品質檢查：

□ AI Quick Answer ≤ 30 字？
□ 可獨立理解，無需上下文？
□ Context Fit 明確（適用 + 不適用）？
□ Confidence Signals 為 JSON 格式？
□ Machine-Readable Payload 完整？
□ 通過 Schema.org 驗證？
□ Entity Confidence ≥ 0.60？
```

---

### Citation 檢查清單

```bash
✅ Citation 品質檢查：

□ Citation ID 唯一？
□ Source Entity 存在且有效？
□ Claim 清晰具體？
□ Evidence Type 已分類？
□ Source URL 可訪問？
□ Verification Status 明確？
□ CCS ≥ 0.60？
□ 至少 1 個交叉驗證來源？（統計聲明）
```

---

## 參考文檔

### 完整技術規範

- **主規劃文檔**：`docs/AI_READY_SEO_PLANNING.md` (3,625 行)
  - Phase 0: Entity Optimization
  - Phase 1: AFB + E-E-A-T Signals
  - 六大技術檢測指標
  - 與現有 Skills 整合

- **Phase 2 實作**：`docs/AI_CITATION_ENGINEERING_PHASE2.md` (1,127 行)
  - Machine-Readable Citations
  - Citation Confidence Score (CCS)
  - Entity Graph.json

- **Phase 3 測試**：`docs/AI_CITATION_ENGINEERING_PHASE3.md` (700 行)
  - Reverse GEO Testing
  - Question Matrix
  - Diff Analysis

### 快速參考

- **執行狀態**：`AI_CITATION_ENGINEERING_STATUS.md`
- **文檔索引**：`AI_CITATION_ENGINEERING_INDEX.md`
- **執行摘要**：`docs/EXECUTIVE_SUMMARY.md`
- **README**：`README.md`

---

## 工具與腳本

### Phase 0 工具（待開發）
- `scripts/entity_confidence_calculator.py` - Entity 信任度計算
- `scripts/entity_optimizer.py` - Entity 優化建議

### Phase 1 工具（待開發）
- `scripts/afb_generator.py` - AFB 自動生成
- `scripts/eeat_signal_calculator.py` - E-E-A-T 信號計算

### Phase 2 工具（待開發）
- `scripts/citation_confidence_calculator.py` - CCS 計算
- `scripts/entity_graph_generator.py` - Entity Graph 生成
- `scripts/citation_conflict_resolver.py` - 衝突解決

### Phase 3 工具（待開發）
- `scripts/reverse_geo_tester.py` - 反向 GEO 測試
- `scripts/output_capture.py` - AI 輸出捕獲
- `scripts/diff_analyzer.py` - 差異分析

---

## 使用範例

### 範例 1：建立個人 Entity

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/entity/zhang-expert",
  "name": "張專家",
  "jobTitle": "SEO 架構師",
  "description": "專注於 AI 搜尋引擎優化，10 年內容工程經驗",
  "sameAs": [
    "https://linkedin.com/in/zhang-expert",
    "https://twitter.com/zhangexpert",
    "https://github.com/zhangexpert",
    "https://scholar.google.com/citations?user=zhang123"
  ],
  "knowsAbout": ["AI Citation Engineering", "SEO", "Content Strategy"]
}
```

---

### 範例 2：創建 AFB

詳見 `templates/afb_template.json` 和 `examples/afb_example_definition.json`

---

### 範例 3：添加 Citation

詳見 `templates/citation_template.json` 和 `examples/citation_example_peer_reviewed.json`

---

## 最佳實踐

### DO（必須做）

1. **始終從 Entity 開始**  
   Entity Confidence 是一切的基礎

2. **AFB 四層結構不可省略**  
   特別是 Machine-Readable Payload

3. **確保 CCS 獨立於 EC**  
   同一 Entity 可以有高低不同的 CCS

4. **記錄 Failure States**  
   系統能說「為什麼不該用」

5. **先驗證再優化**  
   Phase 3 數據收集後再調參數

---

### DON'T（禁止做）

1. **不要跳過 Entity 建立**  
   沒有 Entity = 沒有資格

2. **不要在數據不足時調參數**  
   至少需要 30-50 個樣本

3. **不要混淆 EC 與 CCS**  
   這會導致被權威綁架

4. **不要省略「不適用情境」**  
   Context Fit 的負面清單同等重要

5. **不要把 Graph 當視覺化**  
   它是風險檢測工具

---

## 系統架構

```
Answer Trust Infrastructure

├─ Layer 0: Entity Trust（實體信任層）
│   └─ Entity Confidence Score（5 維）
│
├─ Layer 1: Answer Packaging（答案封裝層）
│   └─ Answer-First Block (AFB)
│
├─ Layer 2: Citation Trust（引用信任層）
│   └─ Citation Confidence Score（6 維）
│
└─ Layer 3: Risk Detection（風險檢測層）
    └─ Entity Graph（Isolated + Single-Source）
```

**詳細架構**：見 `README.md`

---

## 關鍵指標

### 門檻值

```
Entity Confidence:     ≥ 0.70（及格），≥ 0.90（權威）
AFB Eligibility:       ≥ 0.60（可生成）
Citation Confidence:   ≥ 0.70（可用），≥ 0.90（優先）
E-E-A-T Score:         ≥ 0.70（專業），≥ 0.90（權威）
```

### 計算公式

```python
# Entity Confidence
EC = Consistency(0.30) + Authority(0.25) + Citation(0.20) 
     + Frequency(0.15) + Social(0.10)

# Citation Confidence Score
CCS = Corroboration(0.28) + Evidence(0.20) + Reputation(0.18) 
      + Recency(0.14) + Specificity(0.12) + Verification(0.08)

# E-E-A-T Score
EEAT = Experience(0.20) + Expertise(0.30) 
       + Authoritativeness(0.25) + Trust(0.25)
```

---

## 與現有 Skills 的整合

### 協作流程

```
seo-audit → 確保技術基礎健康
   ↓
content-creator → 產生內容初稿
   ↓
ai-citation-engineering → 重組為 AFB + Citations
   ↓
analytics-tracking → 追蹤引用與品牌搜尋
```

### Skill 組合建議

**組合 A：內容網站**
```
1. seo-audit（技術檢查）
2. content-creator（內容產出）
3. ai-citation-engineering（AI 優化）
4. analytics-tracking（成效追蹤）
```

**組合 B：SaaS 產品**
```
1. seo-audit（基礎檢查）
2. copywriting（產品文案）
3. ai-citation-engineering（提升引用價值）
4. analytics-tracking（品牌搜尋追蹤）
```

---

## 成功案例（待 Phase 3 完成後補充）

Phase 3 完成後，將在 `examples/case_studies/` 中補充實際測試數據。

---

## 常見問題

### Q: 這與傳統 SEO 有什麼不同？

**A**: 傳統 SEO 優化「排名」，AI Citation Engineering 優化「被引用」。成功指標從「點擊率」變成「引用頻率」。

---

### Q: 需要多久才能看到效果？

**A**: 
- 1 個月：Entity 建立，基礎就位
- 3 個月：開始被 AI 引用
- 6 個月：成為特定主題的 Default Source
- 12 個月：形成權威，新內容自動獲得信任

---

### Q: 零點擊不會影響流量嗎？

**A**: 零點擊建立權威 → 品牌搜尋增長 → 間接流量提升。ROI 延遲但更穩定。

---

### Q: 如何測量 AI 引用率？

**A**: Phase 3 的 Reverse GEO Testing 提供完整方法論。包括 Question Matrix、Output Capture、Diff Analysis。

---

## 技術要求

### 必要條件

- ✅ 網站可編輯 HTML head
- ✅ 可添加 JSON-LD Schema
- ✅ 能建立 Entity 專屬頁面
- ✅ Robots.txt 可配置

### 建議條件

- ✅ 有 API 端點
- ✅ 有 RSS/Atom Feed
- ✅ 內容管理系統支援結構化資料
- ✅ 有技術團隊支援

---

## 專案狀態

**版本**：v0.5.0  
**階段**：Phase 3（Reverse GEO Testing）  
**成熟度**：75%

**完成**：
- ✅ Phase 0：Entity Optimization
- ✅ Phase 1：AFB + E-E-A-T Signals
- ✅ Phase 2：Citation System（封版）

**進行中**：
- 🚧 Phase 3：Reverse GEO Testing

**待完成**：
- ⏳ Phase 4：SKILL.md + Scripts

---

## 相關 Skills

- **seo-audit**: 技術 SEO 基礎檢查
- **content-creator**: 內容創作與品牌聲音
- **seo-content-writer**: 傳統 SEO 內容優化
- **copywriting**: 轉換導向文案
- **programmatic-seo**: 規模化 SEO 策略
- **analytics-tracking**: 追蹤與測量框架

---

## 聯絡與貢獻

**專案維護**：Answer Trust Infrastructure Team  
**最後更新**：2026-02-06  
**狀態**：🟢 活躍開發

---

## 重要聲明

**這不是一個 SEO 技巧清單。**

**這是面向 AI 搜尋時代的內容工程規範（Content Engineering Spec）。**

**核心目標不是讓你排第一名，而是讓你進入 AI 的答案層。**

---

**開始使用**：閱讀 `README.md` 獲得快速概覽，然後查看 `AI_CITATION_ENGINEERING_INDEX.md` 選擇適合的閱讀路徑。
