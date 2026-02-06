# Trust WEDO – MVP

## 一句話目標

把網站內容轉換為「AI 可評估、可拒絕、可引用」的答案物件。

---

## MVP 範圍（必做）

1. ✅ 掃描網站內容並抽取基礎結構
2. ✅ 建立 Entity Profile 並計算 Entity Confidence
3. ✅ 產生 Answer-First Block（AFB）
4. ✅ 評估 Citation 並計算 Citation Confidence
5. ✅ 輸出風險檢測結果（isolated / single-source）

---

## 明確不做（v1 不做）

- ❌ Dashboard / UI
- ❌ 自動提問 AI
- ❌ 視覺化 Graph
- ❌ 權重調參

---

## 成功定義

### 功能完整性
- ✅ 能輸出完整 JSON 報告
- ✅ 系統能給出 accept / downgrade / reject
- ✅ 失敗理由可被解釋

### 資料品質
- ✅ 所有輸出符合 JSON Schema
- ✅ 信任評分計算邏輯正確
- ✅ 拒絕邏輯正確觸發

### 可維護性
- ✅ CLI 指令清晰易用
- ✅ 文件完整可執行
- ✅ 測試覆蓋核心邏輯

---

## 核心設計原則

### 1. 可驗證性優先
每個步驟都必須有明確的信任評分，不能有「黑箱」判斷。

### 2. 拒絕優於降級
當信任度不足時，寧可拒絕也不要產生低品質答案。

### 3. 結構化輸出
所有結果都以 JSON 格式輸出，方便後續處理與整合。

### 4. 最小可行
MVP 階段專注於核心功能，不做額外優化。

---

## 技術決策

### 技術棧
- **語言**：Python 3.10+
- **CLI 框架**：Click
- **Schema 驗證**：jsonschema
- **HTML 解析**：BeautifulSoup4
- **HTTP 請求**：httpx

### 為什麼選擇 Python？
1. 豐富的資料處理生態系
2. 易於整合 AI/ML 工具
3. 簡潔的 CLI 開發體驗
4. 強大的 HTML/JSON 處理能力

---

## 未來規劃（v2+）

- 🔮 Web Dashboard
- 🔮 自動化 AI 提問與答案生成
- 🔮 視覺化實體關係圖
- 🔮 可調整的信任評分權重
- 🔮 批次處理多個網站
- 🔮 API 服務模式
