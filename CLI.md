# Trust WEDO CLI

CLI 名稱：`tw`

---

## 指令一覽

```bash
tw scan <url>
→ output/site.json

tw entity score <site.json>
→ output/entity_profile.json

tw afb build <page.html> --entity <entity_profile.json>
→ output/afb.json

tw citation eval <afb.json>
→ output/citation_eval.json

tw graph build <bundle/>
→ output/entity_graph.json

tw report <bundle/>
→ output/trust-wedo-report.md
→ output/trust-wedo-report.json
```

---

## 詳細說明

### 1. `tw scan` - 站點掃描

**用途**：掃描網站內容，抓取頁面結構與基礎資訊

**語法**：
```bash
tw scan <url> [options]
```

**參數**：
- `<url>`：要掃描的網站 URL（必填）
- `--output, -o`：輸出目錄（預設：`output/`）
- `--max-pages`：最大掃描頁面數（預設：10）

**範例**：
```bash
tw scan https://example.com
tw scan https://example.com --output ./results --max-pages 20
```

**輸出**：`output/site.json`

```json
{
  "site": "https://example.com",
  "pages": [
    {
      "url": "https://example.com/page-1",
      "fetched": true,
      "has_jsonld": false,
      "has_meta": true
    }
  ],
  "checks": {
    "robots_ok": true,
    "sitemap_ok": true
  }
}
```

---

### 2. `tw entity score` - Entity 信任評分

**用途**：計算實體的信任評分

**語法**：
```bash
tw entity score <site.json> [options]
```

**參數**：
- `<site.json>`：站點掃描結果（必填）
- `--output, -o`：輸出目錄（預設：`output/`）

**範例**：
```bash
tw entity score output/site.json
tw entity score results/site.json --output ./results
```

**輸出**：`output/entity_profile.json`

```json
{
  "entity_id": "ent:example",
  "entity_confidence": 0.78,
  "signals": {
    "consistency": 0.8,
    "authority": 0.7,
    "citation": 0.6,
    "frequency": 0.9,
    "social": 0.7
  },
  "eligibility": "pass"
}
```

**評分規則**：
- EC ≥ 0.60 → `eligibility: "pass"`
- EC < 0.60 → `eligibility: "fail"`（不會產生 AFB）

---

### 3. `tw afb build` - AFB 產生

**用途**：產生 Answer-First Block（核心功能）

**語法**：
```bash
tw afb build <page.html> --entity <entity_profile.json> [options]
```

**參數**：
- `<page.html>`：要處理的 HTML 頁面（必填）
- `--entity`：實體信任檔案（必填）
- `--output, -o`：輸出目錄（預設：`output/`）

**範例**：
```bash
tw afb build samples/sample_page.html --entity output/entity_profile.json
tw afb build page.html --entity entity.json --output ./results
```

**輸出**：`output/afb.json`

```json
{
  "afb_id": "afb:page-1:definition",
  "entity_id": "ent:example",
  "ai_quick_answer": "Trust WEDO 是一套讓內容可被 AI 安全使用的信任系統。",
  "context_fit": {
    "use_when": ["definition"],
    "do_not_use_when": ["legal_advice"]
  },
  "confidence_signals": {
    "entity_confidence": 0.78,
    "citation_count": 2
  },
  "payload": {
    "@type": "AnswerObject",
    "answer": "Trust WEDO 是一套讓內容可被 AI 安全使用的信任系統。",
    "entity_id": "ent:example"
  }
}
```

**前置條件**：
- Entity Confidence ≥ 0.60（否則不產生 AFB）

---

### 4. `tw citation eval` - Citation 評估

**用途**：評估引用的可信度

**語法**：
```bash
tw citation eval <afb.json> [options]
```

**參數**：
- `<afb.json>`：AFB 檔案（必填）
- `--output, -o`：輸出目錄（預設：`output/`）

**範例**：
```bash
tw citation eval output/afb.json
tw citation eval afb.json --output ./results
```

**輸出**：`output/citation_eval.json`

```json
{
  "afb_id": "afb:page-1:definition",
  "citations": [
    {
      "citation_id": "cite:001",
      "ccs": 0.82,
      "status": "accept",
      "failure_states": []
    }
  ],
  "decision": "accept",
  "reasons": []
}
```

**評估規則**：
- CCS ≥ 0.60 → `status: "accept"`
- CCS < 0.60 → `status: "reject"`

---

### 5. `tw graph build` - 風險圖

**用途**：建立實體關係圖，檢測風險

**語法**：
```bash
tw graph build <bundle/> [options]
```

**參數**：
- `<bundle/>`：包含所有 JSON 檔案的目錄（必填）
- `--output, -o`：輸出目錄（預設：`output/`）

**範例**：
```bash
tw graph build output/
tw graph build ./results --output ./final
```

**輸出**：`output/entity_graph.json`

```json
{
  "entity": "ent:example",
  "metrics": {
    "distinct_sources": 2,
    "is_isolated": false,
    "single_source_risk": false
  }
}
```

**風險檢測**：
- `distinct_sources = 1` → `single_source_risk: true`
- `distinct_sources = 0` → `is_isolated: true`

---

### 6. `tw report` - 最終報告

**用途**：產生人類可讀的最終報告

**語法**：
```bash
tw report <bundle/> [options]
```

**參數**：
- `<bundle/>`：包含所有 JSON 檔案的目錄（必填）
- `--output, -o`：輸出目錄（預設：`output/`）
- `--format`：報告格式（`md` / `json` / `both`，預設：`both`）

**範例**：
```bash
tw report output/
tw report ./results --format md
```

**輸出**：
- `output/trust-wedo-report.md`（Markdown 格式）
- `output/trust-wedo-report.json`（JSON 格式）

---

## 完整流程範例

```bash
# Step 1: 掃描網站
tw scan https://example.com

# Step 2: 計算實體信任評分
tw entity score output/site.json

# Step 3: 產生 AFB
tw afb build samples/sample_page.html --entity output/entity_profile.json

# Step 4: 評估引用
tw citation eval output/afb.json

# Step 5: 建立關係圖
tw graph build output/

# Step 6: 產生報告
tw report output/
```

---

## 全域選項

所有指令都支援以下全域選項：

- `--verbose, -v`：顯示詳細日誌
- `--quiet, -q`：只顯示錯誤訊息
- `--help, -h`：顯示說明
- `--version`：顯示版本號

**範例**：
```bash
tw scan https://example.com --verbose
tw entity score output/site.json --quiet
```
