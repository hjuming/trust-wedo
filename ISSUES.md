# Trust WEDO 開發 Issue 清單

> **交付給工程師的任務單**
> 每個 Issue 都是獨立可執行的工作項目

---

## Issue #1 — Implement `tw scan`

### 目標
實作站點掃描功能，抓取網站內容並產出結構化資料

### 技術需求
- 使用 `httpx` 抓取 HTML
- 使用 `BeautifulSoup` 解析 HTML
- 支援 sitemap.xml 解析（最多 N 頁）
- 產出符合 `site_scan.schema.json` 的 JSON

### Definition of Done
- [ ] 能成功抓取指定 URL 的 HTML
- [ ] 能解析 sitemap.xml（如果存在）
- [ ] 抽取每頁的 title、meta description、JSON-LD、timestamp
- [ ] 輸出 `output/site.json` 並通過 schema 驗證
- [ ] 單元測試覆蓋核心邏輯
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#21-tw-scan-url) - 行為規格
- [schemas/site_scan.schema.json](schemas/site_scan.schema.json) - 輸出格式
- [samples/expected_outputs/site.json](samples/expected_outputs/site.json) - 預期輸出

### 建議實作檔案
```
src/trust_wedo/
├── commands/
│   └── scan.py          # scan 指令實作
├── parsers/
│   └── html_parser.py   # HTML 解析器
└── utils/
    └── http_client.py   # HTTP 請求工具
```

---

## Issue #2 — Implement `tw afb build` (template version)

### 目標
實作 AFB 產生功能，使用固定模板產生答案物件

### 技術需求
- 讀取 HTML 並抽取正文（`<article>` / `<main>` / `<body>`）
- 檢查 Entity Confidence 門檻（< 0.60 拒絕）
- 使用模板產生 `ai_quick_answer`
- 產出符合 `afb.schema.json` 的 JSON

### Definition of Done
- [ ] 能讀取 HTML 並抽取正文
- [ ] 實作 EC < 0.60 的拒絕邏輯
- [ ] 使用模板產生 `ai_quick_answer`（取前 1-2 句 + entity label）
- [ ] 固定 `context_fit` mapping
- [ ] 輸出 `output/afb.json` 並通過 schema 驗證
- [ ] 單元測試覆蓋核心邏輯
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#22-tw-afb-build-pagehtml---entity-entityjson) - 行為規格
- [schemas/afb.schema.json](schemas/afb.schema.json) - 輸出格式
- [samples/expected_outputs/afb.json](samples/expected_outputs/afb.json) - 預期輸出

### 建議實作檔案
```
src/trust_wedo/
├── commands/
│   └── afb.py           # afb 指令實作
├── core/
│   └── afb_builder.py   # AFB 建構器
└── parsers/
    └── content_extractor.py  # 內容抽取器
```

---

## Issue #3 — Implement `tw entity score` (heuristics)

### 目標
實作實體信任評分功能，使用 heuristics 計算五個信號

### 技術需求
- 從 `site.json` 計算五個信號（consistency, authority, citation, frequency, social）
- 計算 Entity Confidence（EC）
- 判定 eligibility（pass/fail）
- 產出符合 `entity_profile.schema.json` 的 JSON

### Definition of Done
- [ ] 實作 5 個信號的 heuristic 計算
- [ ] 實作 EC 計算公式（加權平均）
- [ ] 實作 eligibility 判定邏輯（EC >= 0.60 → pass）
- [ ] 輸出 `output/entity_profile.json` 並通過 schema 驗證
- [ ] 單元測試覆蓋評分邏輯
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#23-tw-entity-score-sitejson) - 行為規格
- [schemas/entity_profile.schema.json](schemas/entity_profile.schema.json) - 輸出格式
- [samples/expected_outputs/entity_profile.json](samples/expected_outputs/entity_profile.json) - 預期輸出

### 建議實作檔案
```
src/trust_wedo/
└── core/
    ├── scoring.py       # 評分邏輯
    └── signals.py       # 信號計算
```

---

## Issue #4 — Implement `tw citation eval` (CCS + conflict)

### 目標
實作引用評估功能，計算 Citation Confidence Score 並判定狀態

### 技術需求
- 讀取 `afb.json` 內的 citations
- 計算 CCS（6 維 + 半衰期）
- 判定 accept/downgrade/reject
- 記錄 failure_states
- 產出符合 `citation_eval.schema.json` 的 JSON

### Definition of Done
- [ ] 實作 CCS 計算邏輯
- [ ] 實作 accept/downgrade/reject 判定（CCS >= 0.60 → accept）
- [ ] 實作 failure_states 記錄
- [ ] 產出整體 decision
- [ ] 輸出 `output/citation_eval.json` 並通過 schema 驗證
- [ ] 單元測試覆蓋評分邏輯
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#24-tw-citation-eval-afbjson) - 行為規格
- [schemas/citation_eval.schema.json](schemas/citation_eval.schema.json) - 輸出格式
- [samples/expected_outputs/citation_eval.json](samples/expected_outputs/citation_eval.json) - 預期輸出

### 建議實作檔案
```
src/trust_wedo/
└── core/
    ├── citation_scorer.py   # CCS 計算
    └── citation_evaluator.py  # 評估邏輯
```

---

## Issue #5 — Implement `tw graph build` (risk only)

### 目標
實作實體關係圖建立功能，專注於風險檢測

### 技術需求
- 讀取 bundle 內的所有 JSON 檔案
- 計算 distinct_sources
- 檢測 is_isolated
- 檢測 single_source_risk
- 產出符合 `entity_graph.schema.json` 的 JSON

### Definition of Done
- [ ] 能讀取 bundle 內的所有 JSON 檔案
- [ ] 實作 distinct_sources 計算
- [ ] 實作 is_isolated 檢測（無外部引用）
- [ ] 實作 single_source_risk 檢測（只有一個來源）
- [ ] 輸出 `output/entity_graph.json` 並通過 schema 驗證
- [ ] 單元測試覆蓋檢測邏輯
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#25-tw-graph-build-bundle) - 行為規格
- [schemas/entity_graph.schema.json](schemas/entity_graph.schema.json) - 輸出格式
- [samples/expected_outputs/entity_graph.json](samples/expected_outputs/entity_graph.json) - 預期輸出

### 建議實作檔案
```
src/trust_wedo/
└── core/
    └── graph_builder.py   # 關係圖建構器
```

---

## Issue #6 — Implement `tw report`

### 目標
實作報告產生功能，聚合所有結果並產出人類可讀的報告

### 技術需求
- 讀取並聚合所有 JSON 檔案
- 產生 Markdown 格式報告
- 產生 JSON 格式報告
- 包含分數、風險、決策、下一步建議

### Definition of Done
- [ ] 能讀取並聚合所有 JSON 檔案
- [ ] 產生 `output/trust-wedo-report.md`
- [ ] 產生 `output/trust-wedo-report.json`
- [ ] 報告包含所有關鍵資訊（分數、風險、決策）
- [ ] 報告格式清晰易讀
- [ ] 整合測試通過

### 參考檔案
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md#26-tw-report-bundle) - 行為規格

### 建議實作檔案
```
src/trust_wedo/
└── commands/
    └── report.py   # 報告產生器
```

---

## Issue #7 — Add CI/CD with GitHub Actions

### 目標
建立 CI/CD 流程，自動執行測試與驗收

### 技術需求
- 建立 GitHub Actions workflow
- 執行 `scripts/verify_mvp.sh`
- 執行所有單元測試
- 執行所有整合測試

### Definition of Done
- [ ] 建立 `.github/workflows/ci.yml`
- [ ] CI 能自動執行 `scripts/verify_mvp.sh`
- [ ] CI 能執行所有測試
- [ ] CI 在 PR 時自動觸發
- [ ] CI 在 main branch push 時自動觸發
- [ ] 所有測試都通過

### 建議實作檔案
```
.github/
└── workflows/
    └── ci.yml
```

---

## 開發順序建議

按照以下順序執行 Issue，確保最快閉環：

1. **Issue #1** (scan) - 建立基礎資料來源
2. **Issue #2** (afb) - 快速得到可用閉環（使用 sample_entity.json）
3. **Issue #3** (entity) - 補上 EC gate
4. **Issue #4** (citation) - 評估引用
5. **Issue #5** (graph) - 風險檢測
6. **Issue #6** (report) - 整合報告
7. **Issue #7** (CI/CD) - 自動化驗收

---

## 重要提醒

> **這階段的正確性來自「輸出契約」，不是來自「算法更聰明」。**
> **先讓 pipeline 產出穩定、可驗證的 JSON，再談聰明。**

### 測試原則
- **測試契約，不測 UI**
- 給固定輸入，驗證固定輸出
- 允許小誤差，但邏輯必須正確

### 驗收標準
- 所有 CLI 指令都能執行
- 所有輸出都通過 JSON Schema 驗證
- `scripts/verify_mvp.sh` 執行成功
- 所有單元測試通過
- 所有整合測試通過
