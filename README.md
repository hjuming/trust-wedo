# Trust WEDO

**Answer Trust Infrastructure for Generative Systems.**

This tool converts content into verifiable, rejectable, and AI-usable answer objects.

**This is not SEO. This is trust engineering for answers.**

---

## 📌 唯一真理文件（工程規格來源）

> **PR 討論若與以下文件衝突，以這三份為準。**

1. **[DEVELOPMENT_BLUEPRINT.md](DEVELOPMENT_BLUEPRINT.md)** - 流程與驗收入口
2. **[MVP_BEHAVIOR.md](MVP_BEHAVIOR.md)** - 每個指令的最小行為規格
3. **[ISSUES.md](ISSUES.md)** - 工程任務拆分與 DoD

**工程 KPI（v0.2 最小成功定義）：**
- ✅ `./scripts/verify_mvp.sh` exit code = 0
- ✅ `output/` 產出所有必要 JSON 檔案
- ✅ EC gate / CCS gate / single_source_risk 都能被測試觸發

**硬規則：任何 PR 沒讓 `./scripts/verify_mvp.sh` 更接近全綠，就不合併。**

---


---

## 快速開始

### 安裝

```bash
# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝套件
pip install -e .
```

### 基本使用

```bash
# 1. 掃描網站
tw scan https://example.com

# 2. 計算實體信任評分
tw entity score output/site.json

# 3. 產生 Answer-First Block
tw afb build samples/sample_page.html --entity output/entity_profile.json

# 4. 評估引用可信度
tw citation eval output/afb.json

# 5. 建立實體關係圖
tw graph build output/

# 6. 產生最終報告
tw report output/
```

---

## CLI 指令

| 指令 | 說明 | 輸出 |
|------|------|------|
| `tw scan <url>` | 掃描網站內容 | `output/site.json` |
| `tw entity score <site.json>` | 計算實體信任評分 | `output/entity_profile.json` |
| `tw afb build <page.html> --entity <entity.json>` | 產生答案物件 | `output/afb.json` |
| `tw citation eval <afb.json>` | 評估引用可信度 | `output/citation_eval.json` |
| `tw graph build <bundle/>` | 建立實體關係圖 | `output/entity_graph.json` |
| `tw report <bundle/>` | 產生最終報告 | `output/trust-wedo-report.md` |

---

## 專案結構

```
trust-wedo/
├── schemas/              # JSON Schema 定義
├── samples/              # 範例資料
├── src/                  # 原始碼
│   ├── commands/         # CLI 指令實作
│   ├── core/             # 核心邏輯
│   ├── parsers/          # 內容解析器
│   ├── validators/       # Schema 驗證器
│   └── utils/            # 工具函式
├── tests/                # 測試檔案
└── output/               # CLI 輸出目錄
```

---

## 核心概念

### Entity Confidence (EC)
實體信任評分，基於以下信號計算：
- **Consistency**：內容一致性
- **Authority**：權威性
- **Citation**：引用品質
- **Frequency**：出現頻率
- **Social**：社群信號

**規則**：EC < 0.60 → 不產生 AFB

### Citation Confidence Score (CCS)
引用可信度評分

**規則**：CCS < 0.60 → reject citation

### Answer-First Block (AFB)
可被 AI 安全使用的答案物件，包含：
- AI 快速答案
- 使用情境限制
- 信任信號
- 結構化 payload

---

## 文件

- [PRODUCT.md](PRODUCT.md) - 產品定義與範圍
- [CLI.md](CLI.md) - CLI 指令詳細規格
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md) - 驗收測試標準

---

## License

MIT
