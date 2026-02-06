# Trust WEDO Phase 3 規劃：tw capture 指令

> **v0.3 準備：開始累積 AI 輸出資料，為 Diff Analysis 做準備**

---

## 目標

建立 `tw capture` 指令，提供「貼上 AI 輸出」的容器，開始累積 Phase 3 的第一批實測資料。

**核心原則：**
- 不需要自動提問 AI
- 只提供資料容器
- 為後續 Diff Analysis 準備

---

## CLI 指令規格

### `tw capture <afb_id> --ai-output <text> [--source <name>]`

**參數：**
- `<afb_id>`：關聯的 AFB ID（必填）
- `--ai-output <text>`：AI 的回答內容（必填）
- `--source <name>`：AI 來源名稱（選填，預設 "unknown"）

**範例：**
```bash
# 貼上 ChatGPT 的回答
tw capture afb:page-1:definition \
  --ai-output "Trust WEDO 是一個信任工程系統..." \
  --source "chatgpt-4"

# 貼上 Claude 的回答
tw capture afb:page-1:definition \
  --ai-output "Trust WEDO 提供可驗證的答案物件..." \
  --source "claude-3.5"
```

---

## 輸出格式

### capture.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AI Output Capture",
  "description": "捕獲的 AI 輸出資料",
  "type": "object",
  "required": ["capture_id", "afb_id", "ai_output", "captured_at", "meta"],
  "properties": {
    "capture_id": {
      "type": "string",
      "pattern": "^cap:",
      "description": "捕獲 ID，格式：cap:001"
    },
    "afb_id": {
      "type": "string",
      "pattern": "^afb:",
      "description": "關聯的 AFB ID"
    },
    "ai_output": {
      "type": "string",
      "description": "AI 的回答內容"
    },
    "source": {
      "type": "string",
      "description": "AI 來源（chatgpt-4, claude-3.5, gemini-pro 等）"
    },
    "captured_at": {
      "type": "string",
      "format": "date-time",
      "description": "捕獲時間（ISO 8601）"
    },
    "meta": {
      "type": "object",
      "required": ["generated_at", "tool_version", "input_source"],
      "properties": {
        "generated_at": { "type": "string", "format": "date-time" },
        "tool_version": { "type": "string" },
        "input_source": { "type": "string" }
      }
    }
  }
}
```

### 輸出範例

```json
{
  "capture_id": "cap:001",
  "afb_id": "afb:page-1:definition",
  "ai_output": "Trust WEDO 是一套讓內容可被 AI 安全使用的信任系統。它透過建立可驗證、可拒絕、可引用的答案物件（Answer-First Block, AFB），為生成式 AI 系統提供信任基礎設施。",
  "source": "chatgpt-4",
  "captured_at": "2024-01-15T10:30:00Z",
  "meta": {
    "generated_at": "2024-01-15T10:30:00Z",
    "tool_version": "0.3.0",
    "input_source": "cli:manual"
  }
}
```

---

## 實作規格

### MVP 行為

✅ **必須做：**
- 接收 AFB ID 與 AI 輸出文字
- 產生唯一的 capture_id（格式：`cap:001`, `cap:002`...）
- 記錄捕獲時間（ISO 8601）
- 儲存到 `output/captures/` 目錄
- 檔名格式：`capture_<afb_id>_<source>_<timestamp>.json`
- 輸出符合 `capture.schema.json`
- 包含一致的 `meta` 欄位

❌ **不必做：**
- 自動提問 AI
- 驗證 AI 輸出品質
- 與 AFB 內容做比對
- 計算相似度分數

### Definition of Done

- [ ] CLI 指令可執行
- [ ] 產生的 JSON 通過 schema 驗證
- [ ] 檔案正確儲存到 `output/captures/`
- [ ] capture_id 自動遞增
- [ ] 包含完整的 meta 欄位

---

## 檔案結構

### 新增檔案

```
Trust-WEDO/
├── schemas/
│   └── capture.schema.json          # 新增：Capture Schema
├── src/trust_wedo/
│   ├── commands/
│   │   └── capture.py               # 新增：Capture 指令
│   └── core/
│       └── capture_manager.py       # 新增：Capture 管理邏輯
├── output/
│   └── captures/                    # 新增：Capture 輸出目錄
│       ├── capture_afb-page-1-definition_chatgpt-4_20240115.json
│       └── capture_afb-page-1-definition_claude-3.5_20240115.json
└── tests/
    ├── unit/
    │   └── test_capture.py          # 新增：Capture 單元測試
    └── integration/
        └── test_capture_flow.py     # 新增：Capture 整合測試
```

---

## 使用場景

### 場景 1：手動測試 AI 回答品質

```bash
# 1. 產生 AFB
tw afb build samples/sample_page.html --entity output/entity_profile.json

# 2. 複製 ai_quick_answer 去問 ChatGPT
# （手動操作）

# 3. 貼上 ChatGPT 的回答
tw capture afb:page-1:definition \
  --ai-output "ChatGPT 的回答內容..." \
  --source "chatgpt-4"

# 4. 貼上 Claude 的回答
tw capture afb:page-1:definition \
  --ai-output "Claude 的回答內容..." \
  --source "claude-3.5"
```

### 場景 2：累積多個 AI 來源的回答

```bash
# 對同一個 AFB，收集不同 AI 的回答
tw capture afb:page-1:definition --ai-output "..." --source "chatgpt-4"
tw capture afb:page-1:definition --ai-output "..." --source "claude-3.5"
tw capture afb:page-1:definition --ai-output "..." --source "gemini-pro"
tw capture afb:page-1:definition --ai-output "..." --source "llama-3"
```

### 場景 3：為 Diff Analysis 準備資料

```bash
# 累積一段時間後，可以分析：
# - 哪個 AI 的回答最接近 AFB 的 ai_quick_answer
# - 哪個 AI 最常引用正確的來源
# - 哪個 AI 最容易產生幻覺
```

---

## Phase 3 完整流程（未來）

### v0.3：tw capture（本次實作）
- 提供資料容器
- 開始累積 AI 輸出

### v0.4：tw diff（未來規劃）
- 比對 AFB 與 Capture 的差異
- 計算相似度分數
- 識別幻覺內容

### v0.5：tw analyze（未來規劃）
- 聚合多個 Capture 的分析
- 產生 AI 品質報告
- 識別最佳 AI 來源

---

## 驗收標準

### 功能驗收

- ✅ `tw capture` 指令可執行
- ✅ 產生的 JSON 通過 `capture.schema.json` 驗證
- ✅ 檔案正確儲存到 `output/captures/`
- ✅ capture_id 自動遞增（cap:001, cap:002...）
- ✅ 包含完整的 meta 欄位

### 測試驗收

- ✅ 單元測試：`tests/unit/test_capture.py`
- ✅ 整合測試：`tests/integration/test_capture_flow.py`
- ✅ Schema 驗證測試

### 文件驗收

- ✅ 更新 `CLI.md` 加入 `tw capture` 說明
- ✅ 更新 `README.md` 加入使用範例
- ✅ 建立 `schemas/capture.schema.json`

---

## 時程規劃

### 第一天：Schema 與文件
- 建立 `capture.schema.json`
- 更新 `CLI.md` 與 `README.md`

### 第二天：核心實作
- 實作 `capture_manager.py`
- 實作 `commands/capture.py`
- 整合到 CLI

### 第三天：測試與驗收
- 撰寫單元測試
- 撰寫整合測試
- 執行驗收腳本

---

## 下一步行動

### 工程師可以立即開始

```bash
# 1. 建立 Schema
cat > schemas/capture.schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AI Output Capture",
  ...
}
EOF

# 2. 建立核心模組
touch src/trust_wedo/core/capture_manager.py
touch src/trust_wedo/commands/capture.py

# 3. 建立測試
touch tests/unit/test_capture.py
touch tests/integration/test_capture_flow.py

# 4. 開始實作
git checkout -b feature/issue-8-capture
```

---

## 總結

✅ **v0.3 目標：開始累積 AI 輸出資料**

**核心價值：**
- 不需要自動提問 AI（降低複雜度）
- 提供簡單的資料容器（手動貼上）
- 為 Phase 3 Diff Analysis 做準備

**預期成果：**
- 工程師可以手動測試不同 AI 的回答品質
- 累積真實的 AI 輸出資料
- 為後續自動化分析打下基礎

🎯 **Trust WEDO v0.3 準備就緒！**
