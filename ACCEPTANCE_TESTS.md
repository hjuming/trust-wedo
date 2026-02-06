# Acceptance Tests

## 必須成功

### 基本功能
- [ ] CLI 全部指令都能跑完
- [ ] 產出 5 份 JSON 檔案
- [ ] 出現 accept / reject 判斷
- [ ] 所有 JSON 輸出符合對應的 Schema

### 信任評分
- [ ] Entity Confidence 計算正確
- [ ] 五個信號（consistency, authority, citation, frequency, social）都有數值
- [ ] EC ≥ 0.60 時 eligibility = "pass"
- [ ] EC < 0.60 時 eligibility = "fail"

### AFB 產生
- [ ] EC ≥ 0.60 時成功產生 AFB
- [ ] AFB 包含 ai_quick_answer
- [ ] AFB 包含 context_fit（use_when / do_not_use_when）
- [ ] AFB 包含 confidence_signals
- [ ] AFB 包含 payload

### Citation 評估
- [ ] CCS 計算正確
- [ ] CCS ≥ 0.60 時 status = "accept"
- [ ] CCS < 0.60 時 status = "reject"
- [ ] decision 反映整體評估結果

### 風險檢測
- [ ] distinct_sources 計算正確
- [ ] distinct_sources = 1 時 single_source_risk = true
- [ ] distinct_sources = 0 時 is_isolated = true

### 報告產生
- [ ] 產生 Markdown 報告
- [ ] 產生 JSON 報告
- [ ] 報告包含所有關鍵資訊

---

## 必須拒絕

### Entity Confidence 門檻
- [ ] EC < 0.60 → 不產生 AFB
- [ ] EC < 0.60 → 在 entity_profile.json 中 eligibility = "fail"

### Citation Confidence 門檻
- [ ] CCS < 0.60 → citation status = "reject"
- [ ] CCS < 0.60 → decision = "reject" 或 "downgrade"

### 風險檢測
- [ ] 單一來源 → single_source_risk = true
- [ ] 孤立實體 → is_isolated = true

---

## 測試案例

### 案例 1：正常流程（高信任度）

**輸入**：
- 網站：https://example.com
- 頁面：包含完整 meta tags 與 JSON-LD
- 引用：多個可靠來源

**預期輸出**：
- EC ≥ 0.60
- eligibility = "pass"
- 成功產生 AFB
- CCS ≥ 0.60
- citation status = "accept"
- decision = "accept"
- single_source_risk = false

---

### 案例 2：低信任度（應拒絕）

**輸入**：
- 網站：新網站，無權威性
- 頁面：缺少 meta tags
- 引用：無引用或低品質引用

**預期輸出**：
- EC < 0.60
- eligibility = "fail"
- **不產生 AFB**（指令應提前終止或跳過）

---

### 案例 3：單一來源風險

**輸入**：
- 網站：只有一個頁面
- 引用：所有引用都來自同一來源

**預期輸出**：
- distinct_sources = 1
- single_source_risk = true
- decision = "downgrade" 或 "reject"

---

### 案例 4：孤立實體

**輸入**：
- 網站：完全沒有外部引用
- 頁面：自我引用

**預期輸出**：
- distinct_sources = 0
- is_isolated = true
- decision = "reject"

---

## Schema 驗證

所有輸出都必須通過 JSON Schema 驗證：

```bash
# 驗證 site.json
jsonschema -i output/site.json schemas/site_scan.schema.json

# 驗證 entity_profile.json
jsonschema -i output/entity_profile.json schemas/entity_profile.schema.json

# 驗證 afb.json
jsonschema -i output/afb.json schemas/afb.schema.json

# 驗證 citation_eval.json
jsonschema -i output/citation_eval.json schemas/citation_eval.schema.json

# 驗證 entity_graph.json
jsonschema -i output/entity_graph.json schemas/entity_graph.schema.json
```

---

## 整合測試腳本

```bash
#!/bin/bash
set -e

echo "=== Trust WEDO Acceptance Tests ==="

# 清理舊輸出
rm -rf output/
mkdir -p output/

# 執行完整流程
echo "Step 1: Scanning site..."
tw scan https://example.com

echo "Step 2: Scoring entity..."
tw entity score output/site.json

echo "Step 3: Building AFB..."
tw afb build samples/sample_page.html --entity output/entity_profile.json

echo "Step 4: Evaluating citations..."
tw citation eval output/afb.json

echo "Step 5: Building graph..."
tw graph build output/

echo "Step 6: Generating report..."
tw report output/

# 驗證輸出
echo "Validating outputs..."
jsonschema -i output/site.json schemas/site_scan.schema.json
jsonschema -i output/entity_profile.json schemas/entity_profile.schema.json
jsonschema -i output/afb.json schemas/afb.schema.json
jsonschema -i output/citation_eval.json schemas/citation_eval.schema.json
jsonschema -i output/entity_graph.json schemas/entity_graph.schema.json

echo "=== All tests passed! ==="
```

---

## 驗收標準總結

### 功能完整性 ✅
- 6 個 CLI 指令都能執行
- 產生所有必要的輸出檔案

### 資料品質 ✅
- 所有 JSON 符合 Schema
- 信任評分邏輯正確

### 拒絕邏輯 ✅
- EC < 0.60 不產生 AFB
- CCS < 0.60 拒絕引用
- 風險檢測正確觸發

### 可維護性 ✅
- CLI 指令清晰易用
- 錯誤訊息明確
- 文件完整可執行
