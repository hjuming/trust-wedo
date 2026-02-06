# Trust WEDO 工程開發藍圖

> **v0.2 開發指南 - 從初始化到可交付 MVP**

---

## 📋 快速導覽

- **[MVP_BEHAVIOR.md](MVP_BEHAVIOR.md)** - 每個指令的最小行為規格
- **[ISSUES.md](ISSUES.md)** - 詳細的 Issue 清單（7 個獨立任務）
- **[scripts/verify_mvp.sh](scripts/verify_mvp.sh)** - 一鍵驗收腳本
- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** - CI/CD 配置

---

## 🎯 核心原則

> **這階段的正確性來自「輸出契約」，不是來自「算法更聰明」。**
> **先讓 pipeline 產出穩定、可驗證的 JSON，再談聰明。**

---

## 🚀 開始開發

### 1. 環境設定

```bash
# Clone 專案
git clone <repo-url>
cd Trust-WEDO

# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝套件
pip install -e ".[dev]"

# 驗證安裝
tw --version
```

### 2. 開發順序（已調整）

```
scan → afb (固定模板) → entity → citation → graph → report
```

**為什麼這樣調整？**
- 可以先用 `sample_entity.json` 讓 afb 跑起來
- 更快得到「產出 AFB JSON」的可用閉環
- entity score 再補上 gate（EC < 0.6 不產生）即可

### 3. 開發流程

每個 Issue 的開發流程：

```bash
# 1. 建立功能分支
git checkout -b feature/issue-1-scan

# 2. 實作功能
# 參考 ISSUES.md 中的 Definition of Done

# 3. 撰寫測試
# 單元測試：tests/unit/
# 整合測試：tests/integration/

# 4. 執行測試
pytest tests/unit -v
pytest tests/integration -v

# 5. 執行驗收腳本
./scripts/verify_mvp.sh

# 6. 提交程式碼
git add .
git commit -m "feat: implement tw scan"
git push origin feature/issue-1-scan

# 7. 建立 Pull Request
```

---

## 📝 Issue 清單

### Issue #1 — Implement `tw scan`
**優先級：最高** | **預估時間：2-3 天**

實作站點掃描功能，抓取網站內容並產出結構化資料。

**關鍵檔案：**
- `src/trust_wedo/commands/scan.py`
- `src/trust_wedo/parsers/html_parser.py`
- `src/trust_wedo/utils/http_client.py`

**詳細規格：** [ISSUES.md#issue-1](ISSUES.md#issue-1--implement-tw-scan)

---

### Issue #2 — Implement `tw afb build` (template version)
**優先級：最高** | **預估時間：2-3 天**

實作 AFB 產生功能，使用固定模板產生答案物件。

**關鍵檔案：**
- `src/trust_wedo/commands/afb.py`
- `src/trust_wedo/core/afb_builder.py`
- `src/trust_wedo/parsers/content_extractor.py`

**詳細規格：** [ISSUES.md#issue-2](ISSUES.md#issue-2--implement-tw-afb-build-template-version)

---

### Issue #3 — Implement `tw entity score` (heuristics)
**優先級：高** | **預估時間：2-3 天**

實作實體信任評分功能，使用 heuristics 計算五個信號。

**關鍵檔案：**
- `src/trust_wedo/core/scoring.py`
- `src/trust_wedo/core/signals.py`

**詳細規格：** [ISSUES.md#issue-3](ISSUES.md#issue-3--implement-tw-entity-score-heuristics)

---

### Issue #4 — Implement `tw citation eval` (CCS + conflict)
**優先級：中** | **預估時間：2-3 天**

實作引用評估功能，計算 Citation Confidence Score 並判定狀態。

**關鍵檔案：**
- `src/trust_wedo/core/citation_scorer.py`
- `src/trust_wedo/core/citation_evaluator.py`

**詳細規格：** [ISSUES.md#issue-4](ISSUES.md#issue-4--implement-tw-citation-eval-ccs--conflict)

---

### Issue #5 — Implement `tw graph build` (risk only)
**優先級：中** | **預估時間：1-2 天**

實作實體關係圖建立功能，專注於風險檢測。

**關鍵檔案：**
- `src/trust_wedo/core/graph_builder.py`

**詳細規格：** [ISSUES.md#issue-5](ISSUES.md#issue-5--implement-tw-graph-build-risk-only)

---

### Issue #6 — Implement `tw report`
**優先級：低** | **預估時間：1-2 天**

實作報告產生功能，聚合所有結果並產出人類可讀的報告。

**關鍵檔案：**
- `src/trust_wedo/commands/report.py`

**詳細規格：** [ISSUES.md#issue-6](ISSUES.md#issue-6--implement-tw-report)

---

### Issue #7 — Add CI/CD with GitHub Actions
**優先級：中** | **預估時間：0.5-1 天**

建立 CI/CD 流程，自動執行測試與驗收。

**關鍵檔案：**
- `.github/workflows/ci.yml`（已建立）

**詳細規格：** [ISSUES.md#issue-7](ISSUES.md#issue-7--add-cicd-with-github-actions)

---

## 🧪 測試策略

### 單元測試（unit）

**測試契約，不測 UI**

```python
# tests/unit/test_ec.py
def test_entity_confidence_calculation():
    """給固定 signals，驗證固定 EC"""
    signals = {
        "consistency": 0.8,
        "authority": 0.7,
        "citation": 0.6,
        "frequency": 0.9,
        "social": 0.7
    }
    ec = calculate_entity_confidence(signals)
    assert 0.75 <= ec <= 0.80  # 允許小誤差

# tests/unit/test_gates.py
def test_ec_gate():
    """EC < 0.6 禁止產生 AFB"""
    entity = {"entity_confidence": 0.55}
    with pytest.raises(ValueError):
        build_afb(page, entity)
```

### 整合測試（integration）

```python
# tests/integration/test_full_pipeline.py
def test_full_pipeline():
    """執行完整 CLI 流程"""
    # 1. scan
    result = subprocess.run(["tw", "scan", "..."])
    assert result.returncode == 0
    
    # 2. entity score
    result = subprocess.run(["tw", "entity", "score", "..."])
    assert result.returncode == 0
    
    # ... 其他指令
```

### 驗收測試

```bash
# 一鍵執行完整驗收
./scripts/verify_mvp.sh

# 驗證內容：
# 1. 所有 CLI 指令都能執行
# 2. 所有輸出都通過 JSON Schema 驗證
# 3. 拒絕邏輯正確觸發
```

---

## 📊 驗收標準

### 必須通過

- ✅ 所有 CLI 指令都能執行
- ✅ 所有輸出都通過對應的 JSON Schema 驗證
- ✅ `scripts/verify_mvp.sh` 執行成功
- ✅ EC < 0.60 時不產生 AFB（或產生帶 fail 標記的 AFB）
- ✅ CCS < 0.60 時 reject citation
- ✅ 單一來源時 `single_source_risk = true`
- ✅ 所有單元測試通過
- ✅ 所有整合測試通過
- ✅ CI/CD 在 GitHub Actions 上執行成功

---

## 🛠️ 工具與指令

### 開發工具

```bash
# 執行測試
pytest tests/unit -v
pytest tests/integration -v

# 執行 linting
ruff check src/ tests/
black src/ tests/

# 執行 type checking
mypy src/

# 執行驗收
./scripts/verify_mvp.sh
```

### Schema 驗證

```bash
# 驗證單一檔案
python -m trust_wedo.validators.schema_validator output/

# 或使用驗收腳本（包含 schema 驗證）
./scripts/verify_mvp.sh
```

---

## 📚 參考文件

### 核心文件
- [README.md](README.md) - 專案簡介
- [PRODUCT.md](PRODUCT.md) - 產品定義
- [CLI.md](CLI.md) - CLI 指令規格
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md) - 驗收測試標準

### 開發文件
- [MVP_BEHAVIOR.md](MVP_BEHAVIOR.md) - MVP 行為規格
- [ISSUES.md](ISSUES.md) - Issue 清單
- [CHANGELOG.md](CHANGELOG.md) - 變更記錄

### Schema 定義
- [schemas/site_scan.schema.json](schemas/site_scan.schema.json)
- [schemas/entity_profile.schema.json](schemas/entity_profile.schema.json)
- [schemas/afb.schema.json](schemas/afb.schema.json)
- [schemas/citation_eval.schema.json](schemas/citation_eval.schema.json)
- [schemas/entity_graph.schema.json](schemas/entity_graph.schema.json)

---

## 🎓 重要提醒

### 開發原則

1. **契約優先**：輸出必須符合 JSON Schema
2. **簡單優先**：先用 heuristics，不要等外部 API
3. **測試優先**：先寫測試，再寫實作
4. **閉環優先**：先讓 pipeline 跑通，再優化

### 常見陷阱

❌ **不要做：**
- 過度優化算法
- 等待 LLM API 整合
- 實作複雜的機器學習模型
- 追求完美的準確度

✅ **應該做：**
- 產出穩定的 JSON
- 使用簡單的 heuristics
- 確保 schema 驗證通過
- 讓 CI/CD 跑通

---

## 📅 時程規劃

### 第一週（Issue #1-2）
- Day 1-3: Issue #1 (scan)
- Day 4-6: Issue #2 (afb)
- Day 7: 整合測試與修正

### 第二週（Issue #3-5）
- Day 1-3: Issue #3 (entity)
- Day 4-6: Issue #4 (citation)
- Day 7: Issue #5 (graph)

### 第三週（Issue #6-7 + 驗收）
- Day 1-2: Issue #6 (report)
- Day 3: Issue #7 (CI/CD)
- Day 4-5: 完整驗收與修正
- Day 6-7: 文件完善與交付

---

## ✅ 交付清單

### v0.2 MVP 交付物

- [ ] 6 個 CLI 指令都能執行
- [ ] 所有輸出都通過 schema 驗證
- [ ] `scripts/verify_mvp.sh` 執行成功
- [ ] 所有測試通過
- [ ] CI/CD 在 GitHub Actions 上執行成功
- [ ] 文件完整更新

### 驗收方式

```bash
# 1. Clone 專案
git clone <repo-url>
cd Trust-WEDO

# 2. 設定環境
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 3. 執行驗收
./scripts/verify_mvp.sh

# 4. 檢查 CI
# 前往 GitHub Actions 確認所有測試通過
```

---

## 🎉 完成標準

當以下條件都滿足時，v0.2 MVP 即可交付：

1. ✅ 所有 Issue 都已完成
2. ✅ `scripts/verify_mvp.sh` 執行成功
3. ✅ CI/CD 全綠
4. ✅ 文件完整更新
5. ✅ Code review 通過

**恭喜！Trust WEDO v0.2 MVP 完成！** 🎊
