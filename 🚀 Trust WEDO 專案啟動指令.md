## **一句話說清楚這個專案是什麼**  

> **Trust WEDO 是一個 CLI 工具，**
> **把網站內容轉成「AI 可評估、可拒絕、可引用」的答案資料結構。**

沒有 UI、沒有魔法、沒有 SEO 技巧。
**只有可執行的 pipeline 與固定的 JSON 輸出。**

---

## **一、專案啟動指令

> **「先把 CLI 跑起來，能輸出 JSON 就算成功，不用漂亮、不用優化。」**

---

## **二、Repo 初始化指令

```
# 建立專案
git init trust-wedo
cd trust-wedo

# 基本結構
mkdir -p schemas samples/expected_outputs src

touch README.md
touch PRODUCT.md
touch CLI.md
touch ACCEPTANCE_TESTS.md

# Git 初始提交
git add .
git commit -m "init: Trust WEDO MVP scaffold"
```


## **📁 Repo 結構（MVP 版）**
```
trust-wedo/
├── PRODUCT.md
├── CLI.md
├── ACCEPTANCE_TESTS.md
├── schemas/
│   ├── site_scan.schema.json
│   ├── entity_profile.schema.json
│   ├── afb.schema.json
│   ├── citation_eval.schema.json
│   └── entity_graph.schema.json
├── samples/
│   ├── sample_page.html
│   ├── sample_entity.json
│   └── expected_outputs/
└── README.md
```

---

## **三、工程師第一週要完成的「可跑指令」**

### **CLI 名稱：**

### **Trust WEDO**

> 語言不限制（Node / Python 都可）
> **但一定要是 CLI-first**

---

## **1️⃣ 指令一：站點掃描（最低可行）**

```
tw scan https://example.com
```

### **輸出（必須）**

```
output/site.json
```

### **site.json 最小結構**

```
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

## **2️⃣ 指令二：Entity 信任評分**

```
tw entity score output/site.json
```

### **輸出**

```
output/entity_profile.json
```

### **entity_profile.json（最小）**

```
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

---

## **3️⃣ 指令三：AFB 產生（核心）**

```
tw afb build samples/sample_page.html \
  --entity output/entity_profile.json
```

### **輸出**

```
output/afb.json
```

### **afb.json（最小）**

```
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

> ⚠️ 規則：

> **Entity Confidence < 0.60 → 不產生 AFB**

---

## **4️⃣ 指令四：Citation 評估**

```
tw citation eval output/afb.json
```

### **輸出**

```
output/citation_eval.json
```

### **citation_eval.json（最小）**

```
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

> ⚠️ 規則：

> **CCS < 0.60 → reject**

---

## **5️⃣ 指令五：風險圖（Graph）**

```
tw graph build output/
```

### **輸出**

```
output/entity_graph.json
```

### **entity_graph.json（最小）**

```
{
  "entity": "ent:example",
  "metrics": {
    "distinct_sources": 2,
    "is_isolated": false,
    "single_source_risk": false
  }
}
```

---

## **6️⃣ 指令六：最終報告（給人看）**

```
tw report output/
```

### **輸出**

```
output/trust-wedo-report.md
output/trust-wedo-report.json
```

---

## **四、要交給工程師的「文件清單」**

請你把下面這 **6 個檔案** 丟給工程師即可：

---

### **① README.md（對外）**

```
# Trust WEDO

Answer Trust Infrastructure for Generative Systems.

This tool converts content into verifiable,
rejectable, and AI-usable answer objects.

This is not SEO.
This is trust engineering for answers.
```

---

### **② PRODUCT.md（做什麼 / 不做什麼）**

```
# Trust WEDO – MVP

## 一句話目標
把網站內容轉換為「AI 可評估、可拒絕、可引用」的答案物件。

## MVP 範圍（必做）
1. 掃描網站內容並抽取基礎結構
2. 建立 Entity Profile 並計算 Entity Confidence
3. 產生 Answer-First Block（AFB）
4. 評估 Citation 並計算 Citation Confidence
5. 輸出風險檢測結果（isolated / single-source）

## 明確不做（v1 不做）
- Dashboard / UI
- 自動提問 AI
- 視覺化 Graph
- 權重調參

## 成功定義
- 能輸出完整 JSON 報告
- 系統能給出 accept / downgrade / reject
- 失敗理由可被解釋
```

---

### **③ CLI.md（指令規格）**
```
# Trust WEDO CLI

CLI 名稱：`tw`

## 指令一覽

tw scan <url>
→ site.json

tw entity score <site.json>
→ entity_profile.json

tw afb build <page.html> --entity entity_profile.json
→ afb.json

tw citation eval <afb.json>
→ citation_eval.json

tw graph build <bundle/>
→ entity_graph.json

tw report <bundle/>
→ trust-wedo-report.md
→ trust-wedo-report.json
```
  
---

### **④ schemas/（資料契約，最重要）**

至少放這 5 個：

```
schemas/
├── site_scan.schema.json
├── entity_profile.schema.json
├── afb.schema.json
├── citation_eval.schema.json
└── entity_graph.schema.json
```

> 工程師可以先不完全符合 schema

> **但欄位名稱與結構不能亂改**

### **schemas/afb.schema.json（精簡版）**
```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["afb_id", "entity_id", "ai_quick_answer", "payload"],
  "properties": {
    "afb_id": { "type": "string" },
    "entity_id": { "type": "string" },
    "ai_quick_answer": { "type": "string" },
    "context_fit": { "type": "object" },
    "confidence_signals": { "type": "object" },
    "payload": {
      "type": "object",
      "required": ["@type", "answer", "entity_id"]
    }
  }
}
```
其他 schema 你可以照這個密度補齊

---

### **⑤ ACCEPTANCE_TESTS.md（驗收標準）**

```
# Acceptance Tests

## 必須成功
- CLI 全部能跑完
- 產出 5 份 JSON
- 出現 accept / reject 判斷

## 必須拒絕
- EC < 0.60 → 不產生 AFB
- CCS < 0.60 → reject citation
- 單一來源 → single_source_risk = true
```

---

### **⑥ samples/（範例資料）**

```
samples/
├── sample_page.html
├── sample_entity.json
└── expected_outputs/
```

---

## **五、你現在對工程師只需要說這一句話**

> **「不要優化，不要補功能，**
> **只要讓 CLI 能跑完，輸出對的 JSON。」**

---
