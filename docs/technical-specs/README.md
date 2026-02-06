# Trust WEDO 技術規範參考指南

> **Trust WEDO 是 AI Citation Engineering 的 CLI 實作版本**

---

## 📚 文件結構

```
docs/technical-specs/
├── README.md                          # 本文件（快速參考）
├── AI_CITATION_ENGINEERING.md         # 完整 SKILL 文檔
├── PHASE0_1_SPECS.md                  # Phase 0-1 規範（3,625 行）
├── PHASE2_SPECS.md                    # Phase 2 規範（1,127 行）
├── templates/                         # JSON 模板
└── examples/                          # 實作範例
```

---

## 🎯 核心原則

> **照著做，不要自己發明。**

### ✅ DO（必須做）

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

### ❌ DON'T（禁止做）

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

## 🔢 核心公式（必須實作）

### 1. Entity Confidence (EC)

```python
EC = Consistency(0.30) + Authority(0.25) + Citation(0.20) 
     + Frequency(0.15) + Social(0.10)
```

**門檻：**
- ≥ 0.90：🌟 權威
- ≥ 0.70：🟢 及格
- **< 0.60：🔴 不及格（不生成 AFB）**

**詳細規範：** `PHASE0_1_SPECS.md` - Entity Confidence Model

---

### 2. Citation Confidence Score (CCS)

```python
CCS = Corroboration(0.28) + Evidence(0.20) + Reputation(0.18) 
      + Recency(0.14) + Specificity(0.12) + Verification(0.08)
```

**門檻：**
- ≥ 0.90：🌟 優秀
- ≥ 0.70：🟢 可用
- **< 0.60：🔴 拒絕**

**關鍵：** CCS 獨立於 EC（避免被權威綁架）

**詳細規範：** `PHASE2_SPECS.md`

---

### 3. E-E-A-T Score

```python
EEAT = Experience(0.20) + Expertise(0.30) 
       + Authoritativeness(0.25) + Trust(0.25)
```

**門檻：**
- ≥ 0.70：專業
- ≥ 0.90：權威

---

## 📋 AFB 四層強制結構

### 1. AI Quick Answer（≤30 字）
```markdown
什麼是 Trust WEDO？
Trust WEDO 是一套讓內容可被 AI 安全使用的信任系統。
```

### 2. Context Fit（適用/不適用）
```json
{
  "use_when": ["definition", "how_to"],
  "do_not_use_when": ["medical_advice", "legal_advice"]
}
```

### 3. Confidence Signals（JSON）
```json
{
  "entity_confidence": 0.87,
  "citation_count": 3,
  "last_verified": "2026-02-06"
}
```

### 4. Machine-Readable Payload（JSON-LD）
```json
{
  "@type": "Answer",
  "text": "...",
  "author": {"@id": "entity_uri"}
}
```

**詳細規範：** `PHASE0_1_SPECS.md` - 策略 1

---

## 🚨 Citation Failure States（5 種）

### 1. Conflict（衝突）
- 多個來源提供矛盾資訊
- **處理：** 標記 `conflict` 並列出所有來源

### 2. Outdated（過時）
- 資訊發布時間過久
- **門檻：** 依主題而定（科技 < 1 年，歷史 < 10 年）

### 3. Unverifiable（無法驗證）
- 來源不可訪問或無法驗證
- **處理：** 降級或拒絕

### 4. Low Reputation（低信譽）
- Source Entity EC < 0.60
- **處理：** 拒絕或標記警告

### 5. Insufficient Corroboration（交叉驗證不足）
- 統計聲明缺乏多來源驗證
- **門檻：** 至少 2 個獨立來源

**詳細規範：** `PHASE2_SPECS.md` - Citation Failure States

---

## 🗺️ CLI 指令 ↔ 技術規範對應表

| CLI 指令 | 對應規範 | 核心概念 |
|---------|---------|---------|
| `tw scan` | PHASE0_1_SPECS.md - Phase 0 | Entity 建立與驗證 |
| `tw entity score` | PHASE0_1_SPECS.md - Entity Confidence Model | EC 計算公式 |
| `tw afb build` | PHASE0_1_SPECS.md - 策略 1 | AFB 四層結構 |
| `tw citation eval` | PHASE2_SPECS.md - Citation System | CCS 計算 + Failure States |
| `tw graph build` | PHASE2_SPECS.md - Entity Graph | 風險檢測（Isolated + Single-Source） |
| `tw report` | PHASE0_1_SPECS.md - 六大技術檢測指標 | 整合報告 |
| `tw capture` | PHASE3（未封版） | AI 輸出捕獲 |

---

## 📖 快速查找

### Entity 相關
- **Entity Confidence 計算**：`PHASE0_1_SPECS.md` - Entity Confidence Model
- **Entity 建立檢查清單**：`AI_CITATION_ENGINEERING.md` - Entity 檢查清單
- **Entity 範例**：`examples/entity_example_person.json`

### AFB 相關
- **AFB 四層結構**：`PHASE0_1_SPECS.md` - 策略 1
- **AFB 檢查清單**：`AI_CITATION_ENGINEERING.md` - AFB 檢查清單
- **AFB 模板**：`templates/afb_template.json`
- **AFB 範例**：`examples/afb_example_definition.json`

### Citation 相關
- **CCS 計算公式**：`PHASE2_SPECS.md` - Citation Confidence Score
- **Failure States**：`PHASE2_SPECS.md` - Citation Failure States
- **Citation 檢查清單**：`AI_CITATION_ENGINEERING.md` - Citation 檢查清單
- **Citation 模板**：`templates/citation_template.json`
- **Citation 範例**：`examples/citation_example_peer_reviewed.json`

### Graph 相關
- **Entity Graph 規範**：`PHASE2_SPECS.md` - Entity Graph
- **風險檢測邏輯**：`PHASE2_SPECS.md` - Isolated Answer + Single-Source Risk
- **Graph 模板**：`templates/entity_graph_template.json`

---

## 🎓 工程師必讀

### 第一次接觸

1. **閱讀本文件**（5 分鐘）
2. **閱讀 AI_CITATION_ENGINEERING.md**（15 分鐘）
3. **查看對應的 Schema**（10 分鐘）
4. **參考 templates/ 和 examples/**（10 分鐘）

### 實作前

1. **確認公式與門檻值**（從本文件複製）
2. **檢查 Failure States**（不要遺漏）
3. **參考模板與範例**（不要自己發明格式）

### 實作中

1. **遵循 DO/DON'T 原則**
2. **使用正確的權重與門檻**
3. **記錄所有 Failure States**

### 實作後

1. **驗證輸出符合 Schema**
2. **檢查門檻邏輯正確觸發**
3. **確認 meta 欄位完整**

---

## 🔗 相關文件

### Trust WEDO 專案文件
- [README.md](../../README.md) - 專案簡介
- [MVP_BEHAVIOR.md](../../MVP_BEHAVIOR.md) - MVP 行為規格
- [ENGINEERING_DECISIONS.md](../../ENGINEERING_DECISIONS.md) - 工程決策
- [PHASE3_PLANNING.md](../../PHASE3_PLANNING.md) - Phase 3 規劃

### AI Citation Engineering 原始文件
- 專案路徑：`/Users/MING/Sites/skills/skills/ai-citation-engineering/`
- 完整文檔清單：`FILE_LIST.md`
- 專案狀態：`AI_CITATION_ENGINEERING_STATUS.md`

---

## ⚠️ 重要提醒

### 版本狀態

- ✅ **Phase 0-2 已完成且封版**
- ✅ **所有公式、門檻值、Failure States 都已定義**
- ✅ **不要修改核心公式與門檻值**

### 實作原則

> **Trust WEDO 是 AI Citation Engineering 的 CLI 實作版本。**
> **所有規範、公式、門檻值都在專案資料夾裡。**
> **照著做，不要自己發明。**

---

## 📞 需要幫助？

1. **查找公式/門檻**：本文件 - 核心公式
2. **查找規範**：CLI 指令對應表
3. **查找範例**：templates/ 和 examples/
4. **查找詳細說明**：PHASE0_1_SPECS.md 或 PHASE2_SPECS.md

---

**最後更新：** 2026-02-06  
**狀態：** ✅ 可用於 Trust WEDO v0.2-v0.3 開發
