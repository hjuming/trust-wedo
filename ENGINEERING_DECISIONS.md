# Trust WEDO v0.2 工程決策記錄

> **釘死的工程決策，避免後續返工**

---

## 決策 #1：Gate 行為統一

### 問題
原規格允許兩種 Gate 行為：
1. 直接退出（不產生檔案）
2. 產出帶 `fail` 標記的 JSON

### 決策
**v0.2 統一採用：永遠產出 JSON（即使 fail）**

### 理由
- Phase 3 的 capture/diff 可以直接讀結果
- 不會因為指令退出而少一筆資料
- 更容易追蹤失敗原因

### 實作規範

#### Entity Profile（EC < 0.60）
```json
{
  "entity_id": "ent:example",
  "entity_confidence": 0.55,
  "signals": { ... },
  "eligibility": "fail",
  "meta": { ... }
}
```

#### AFB（EC < 0.60）
```json
{
  "afb_id": "afb:page-1:definition",
  "entity_id": "ent:example",
  "ai_quick_answer": "",
  "eligibility": "fail",
  "reasons": ["Entity confidence below threshold: 0.55 < 0.60"],
  "payload": {},
  "meta": { ... }
}
```

#### Citation Eval（CCS < 0.60）
```json
{
  "afb_id": "afb:page-1:definition",
  "citations": [
    {
      "citation_id": "cite:001",
      "ccs": 0.45,
      "status": "reject",
      "failure_states": ["CCS below threshold: 0.45 < 0.60"]
    }
  ],
  "decision": "reject",
  "reasons": ["All citations rejected due to low CCS"]
}
```

---

## 決策 #2：所有輸出 JSON 都要有一致的 meta

### 問題
Phase 3 需要做 Diff Analysis，但無法追蹤資料是哪次跑出來的。

### 決策
**所有輸出 JSON 都必須包含 `meta` 欄位**

### 實作規範

```json
{
  "meta": {
    "generated_at": "2024-01-15T10:30:00Z",
    "tool_version": "0.2.0",
    "input_source": "file:///path/to/sample_page.html"
  },
  // ... 其他欄位
}
```

### 必填欄位
- `generated_at`：產生時間（ISO 8601 格式）
- `tool_version`：工具版本（從 `trust_wedo.__version__` 讀取）
- `input_source`：輸入來源（檔案路徑或 URL）

### 適用範圍
- `site.json`
- `entity_profile.json`
- `afb.json`
- `citation_eval.json`
- `entity_graph.json`

---

## 決策 #3：工程 KPI 明確化

### 問題
「scan 完成」、「citation 完成」等主觀描述無法量化。

### 決策
**v0.2 交付標準只有一句話：**

> 跑通一鍵驗收腳本 + 所有輸出符合 JSON Schema

### 量化指標

#### 必須達成
- ✅ `./scripts/verify_mvp.sh` exit code = 0
- ✅ `output/` 產出以下檔案：
  - `site.json`
  - `entity_profile.json`
  - `afb.json`
  - `citation_eval.json`
  - `entity_graph.json`
  - `trust-wedo-report.md`
  - `trust-wedo-report.json`
- ✅ 所有 JSON 都通過對應的 Schema 驗證
- ✅ Gate 邏輯可被測試觸發：
  - EC < 0.60 → `eligibility: "fail"`
  - CCS < 0.60 → `status: "reject"`
  - distinct_sources = 1 → `single_source_risk: true`

#### PR 合併規則
**任何 PR 沒讓 `./scripts/verify_mvp.sh` 更接近全綠，就不合併。**

---

## 決策 #4：唯一真理文件

### 問題
工程師不確定以哪份文件為準，導致會議時間浪費。

### 決策
**指定三份文件為唯一規格來源**

1. **[DEVELOPMENT_BLUEPRINT.md](DEVELOPMENT_BLUEPRINT.md)** - 流程與驗收入口
2. **[MVP_BEHAVIOR.md](MVP_BEHAVIOR.md)** - 每個指令的最小行為規格
3. **[ISSUES.md](ISSUES.md)** - 工程任務拆分與 DoD

### 規則
PR 討論若與這三份文件衝突，以這三份為準。

### 預期效果
消滅 80% 的會議時間。

---

## 決策 #5：第一週優先級

### 問題
6 個指令都重要，但資源有限。

### 決策
**第一週只完成 Issue #1 + Issue #2**

#### Issue #1: `tw scan`
- 輸出 `site.json` 並通過 schema
- 不求完美解析，先求能跑

#### Issue #2: `tw afb build`
- 用固定模板產出 `afb.json`
- EC gate 生效（< 0.60 產出 fail）

### 理由
這兩個完成，代表「內容 → 答案物件」的主幹已經通了。

---

## 未來規劃（v0.3）

### Phase 3 準備：`tw capture` 指令

**目標：**
不改核心，只加一個能力：提供「貼上 AI 輸出」的容器。

**實作：**
```bash
tw capture --afb-id afb:page-1:definition --ai-output "AI 的回答內容"
```

**輸出：**
```json
{
  "capture_id": "cap:001",
  "afb_id": "afb:page-1:definition",
  "ai_output": "AI 的回答內容",
  "captured_at": "2024-01-15T10:30:00Z",
  "meta": { ... }
}
```

**價值：**
開始累積 Phase 3 的第一批實測資料，不需要自動提問 AI。

---

## 變更記錄

- 2024-01-15: 初始版本，釘死 5 個關鍵決策
