# Trust WEDO MVP 行為規格

> **核心原則：這階段的正確性來自「輸出契約」，不是來自「算法更聰明」。**
> **先讓 pipeline 產出穩定、可驗證的 JSON，再談聰明。**

---

## 開發順序（已調整）

```
scan → afb (固定模板) → entity → citation → graph → report
```

**調整理由：**
- 可以先用 `sample_entity.json` 讓 afb 跑起來
- 更快得到「產出 AFB JSON」的可用閉環
- entity score 再補上 gate（EC < 0.6 不產生）即可

---

## 2.1 `tw scan <url>`

### MVP 行為

✅ **必須做：**
- 抓取 `<url>` HTML（使用 `httpx`）
- 若找到 `<link rel="sitemap">` 或 `sitemap.xml`，解析最多 `--max-pages` 頁
- 每頁抽取：
  - `title`
  - `meta description`
  - 是否有 JSON-LD
  - 抓到的時間戳
- 輸出 `output/site.json` 並通過 schema 驗證

❌ **不必做：**
- robots 深度解析（先做存在性與可訪問性）
- sitemap 多格式容錯（先支援 XML）

### Definition of Done

- [ ] 能成功抓取指定 URL 的 HTML
- [ ] 能解析 sitemap.xml（如果存在）
- [ ] 輸出的 `site.json` 通過 `site_scan.schema.json` 驗證
- [ ] 包含所有必要欄位（url, title, meta, has_jsonld, timestamp）

---

## 2.2 `tw afb build <page.html> --entity <entity.json>`

### MVP 行為

✅ **必須做：**
- 讀取 HTML，抽取正文（先用簡單 heuristic：`<article>` 或 `<main>` 或 `<body>` text）
- 檢查 `entity_confidence < 0.60`：
  - 如果是 → 直接退出並輸出 error（或產出 `afb.json` 帶 `eligibility=fail`）
- 產出 AFB JSON：
  - `ai_quick_answer`：先用模板（例如取前 1–2 句摘要 + entity label）
  - `context_fit`：先固定 mapping（definition / how_to / comparison）
  - `payload`：固定 `@type`, `answer`, `entity_id`
- 輸出 `output/afb.json` 並通過 schema 驗證

❌ **不必做：**
- LLM 摘要（先模板）
- 多語言判斷（先 zh/en 都當作 text）

### Definition of Done

- [ ] 能讀取 HTML 並抽取正文
- [ ] 實作 EC < 0.60 的拒絕邏輯
- [ ] 使用模板產生 `ai_quick_answer`
- [ ] 輸出的 `afb.json` 通過 `afb.schema.json` 驗證

---

## 2.3 `tw entity score <site.json>`

### MVP 行為

✅ **必須做：**
- 從 `site.json` 算出 signals（簡化版本）：
  - **consistency**：同一站 meta/title 是否缺失率低（缺失越少分越高）
  - **authority**：先用「是否有 about/author」頁或 organization schema（有則加分）
  - **citation**：先用「出現外部連結數量」近似
  - **frequency**：用 sitemap lastmod 或抓取時間做近似（有更新跡象加分）
  - **social**：先用「是否有 sameAs / social links」近似
- 計算 EC（依封版公式權重）
- 判定 eligibility：
  - `EC < 0.60` → `fail`
  - `EC >= 0.60` → `pass`
- 輸出 `output/entity_profile.json` 並通過 schema 驗證

❌ **不必做：**
- 等外部 API（先用 heuristics）
- 複雜的機器學習模型

### Definition of Done

- [ ] 實作 5 個信號的 heuristic 計算
- [ ] 實作 EC 計算公式
- [ ] 實作 eligibility 判定邏輯
- [ ] 輸出的 `entity_profile.json` 通過 `entity_profile.schema.json` 驗證

---

## 2.4 `tw citation eval <afb.json>`

### MVP 行為

✅ **必須做：**
- 讀取 `afb.json` 內的 citations（或讀旁邊 `citations.json`）
- 對每筆 citation 計算 CCS（依封版 6 維 + 半衰期）
- 產出：
  - `accept` / `downgrade` / `reject`
  - `failure_states`
  - `decision`（總結）
- 輸出 `output/citation_eval.json` 並通過 schema 驗證

❌ **不必做：**
- 自動抓引用來源（先用 sample）
- 真的去驗證 URL 可用性（先用 `status=verified` / `unverified` 模擬）

### Definition of Done

- [ ] 實作 CCS 計算邏輯
- [ ] 實作 accept/downgrade/reject 判定
- [ ] 實作 failure_states 記錄
- [ ] 輸出的 `citation_eval.json` 通過 `citation_eval.schema.json` 驗證

---

## 2.5 `tw graph build <bundle/>`

### MVP 行為

✅ **必須做：**
- 讀取 bundle 內的 `entity_profile.json`、`afb.json`、`citation_eval.json`
- 計算：
  - `distinct_sources`
  - `is_isolated`
  - `single_source_risk`
  - `conflict_count`（如果有）
- 輸出 `output/entity_graph.json` 並通過 schema 驗證

### Definition of Done

- [ ] 能讀取 bundle 內的所有 JSON 檔案
- [ ] 實作 distinct_sources 計算
- [ ] 實作 is_isolated 檢測
- [ ] 實作 single_source_risk 檢測
- [ ] 輸出的 `entity_graph.json` 通過 `entity_graph.schema.json` 驗證

---

## 2.6 `tw report <bundle/>`

### MVP 行為

✅ **必須做：**
- 聚合以上所有 JSON
- 產出：
  - `report.md`：一頁摘要（分數、風險、拒絕理由、下一步）
  - `report.json`：machine-readable 版本
- 先不用漂亮，能讀就行

### Definition of Done

- [ ] 能讀取並聚合所有 JSON 檔案
- [ ] 產生 Markdown 格式報告
- [ ] 產生 JSON 格式報告
- [ ] 報告包含所有關鍵資訊（分數、風險、決策）

---

## 測試策略

### 單元測試（unit）

**測試契約，不測 UI**

- `test_ccs.py`：給固定 citation，算出固定 CCS（可容許小誤差）
- `test_ec.py`：固定 signals，算出固定 EC
- `test_gates.py`：EC<0.6 禁 AFB、CCS<0.6 reject

### 整合測試（integration）

- 跑 `scripts/verify_mvp.sh`
- 比對 output 是否與 `samples/expected_outputs/*.json` 相容
- **不要求完全相同，但欄位與邏輯要一致**

---

## 驗收標準

### 必須通過

1. ✅ 所有 CLI 指令都能執行
2. ✅ 所有輸出都通過對應的 JSON Schema 驗證
3. ✅ `scripts/verify_mvp.sh` 執行成功
4. ✅ EC < 0.60 時不產生 AFB（或產生帶 fail 標記的 AFB）
5. ✅ CCS < 0.60 時 reject citation
6. ✅ 單一來源時 `single_source_risk = true`

### CI 驗證

- GitHub Actions 能跑通 `scripts/verify_mvp.sh`
- 所有單元測試通過
- 所有整合測試通過
