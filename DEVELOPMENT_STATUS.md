# Development Status & Roadmap

> Last Updated: 2026-02-11

## 🟢 目前狀態 (Current Status)

**Phase 4 (Production) - Completed**
系統已成功部署至生產環境,核心功能(掃描、評分、AFB 建構)皆已穩定運作。

**Phase 5 (評分引擎重構) - Planning**
已診斷出評分邏輯錯誤,正在規劃全面優化方案。

---

## ✅ 已完成階段 (Completed Phases)

### Phase 1: MVP Core (v0.1)
- [x] **CLI Tool**: 實作 `tw scan`, `entity score`, `afb build` 等核心指令。
- [x] **Core Algorithm**: 實作 EC (Entity Confidence) 與 CCS (Citation Confidence) 評分邏輯。
- [x] **Schema Definition**: 定義標準化的 JSON Schema (Site, Entity, AFB)。

### Phase 2: Backend API (v0.2)
- [x] **FastAPI Framework**: 建立 RESTful API 服務。
- [x] **Supabase Integration**: 整合 Auth 與 Database。
- [x] **Asynchronous Processing**: 實作背景任務處理掃描請求。

## Phase 3: 視覺化與互動 (COMPLETED)
- [x] Backend API 擴充 (`/api/reports/{scan_id}/dimensions`)
- [x] Frontend 視覺化元件 (`ReportRadarChart`, `DimensionProgressBars`)
- [x] 快速勝利建議模組 (`QuickWins`)
- [x] 整合至報告頁面

## Bug Fixes (COMPLETED)
- [x] Schema.org 解析錯誤 (Apple.com 0分問題)
- [x] `site_parser.py` UnboundLocalError & ImportError 修復
- [x] 外部連結計算邏輯修正 (Domain comparison)

### Phase 4: Production & Optimization (v1.0)
- [x] **Report Engine Upgrade**: 擴充 Schema.org 檢測與加權評分。
- [x] **Deployment**: Zeabur (Backend) + Cloudflare (Frontend) 全自動部署。
- [x] **Stability Fixes**: 解決 CORS, Redirects, RLS Recursion 等關鍵問題。

---

## 🗺️ 未來開發計劃 (Future Roadmap)

### Phase 5: 評分引擎重構與 UX 提升 (2026-Q1, 🔴 最高優先級)

> **背景**: 使用者回饋發現 Apple.com 僅獲得 35/100 分 (D 級),診斷後確認評分引擎存在邏輯錯誤。

**核心問題**:
1. **Schema.org 解析失敗**: `site_parser.py` 只偵測 JSON-LD 存在但未解析內容 → `schema_types` 永遠為空
2. **評分粒度不足**: 無法讓使用者理解差異
3. **缺乏視覺化**: 報告全是文字,無優先級指示
4. **文案太技術**: `<title>` 等術語嚇跑非技術人員

**優化計劃**:
- [ ] **修復 Schema.org 解析邏輯 (P0)**
    - [ ] 新增 `_parse_jsonld()` 方法解析 JSON-LD 內容
    - [ ] 支援 `@graph` 巢狀格式
    - [ ] 回傳完整 `schema_types` 陣列
- [ ] **重構評分系統為 100 分制 (P0)**
    - [ ] 五大維度:AI 可發現性 (20)、身分可信度 (25)、內容結構化 (25)、社群信任 (15)、技術基礎 (15)
    - [ ] 每個維度獨立計分並回傳明細
- [ ] **視覺化儀表板 (P1)**
    - [ ] 雷達圖顯示五大維度 (Recharts)
    - [ ] 維度進度條 (🟢🟡🔴)
    - [ ] 歷史分數趨勢圖
- [ ] **報告文案重寫 (P1)**
    - [ ] 去除技術術語,改用類比故事
    - [ ] 新增「快速勝利」區塊
    - [ ] 提供可複製的程式碼範例

**驗證標準**:
- ✅ Apple.com 評分達 85+ 分 (A 級)
- ✅ 與 Google Rich Results Test 對照一致
- ✅ 非技術人員能理解報告內容

---

### Phase 6: Deep Analysis & AI Integration (Q2 2026)
- [ ] **LLM 分析增強**:
    - [ ] 整合 GPT-4/Claude 3.5 進行語意驗證
    - [ ] 自動生成引用建議與反駁論點
- [ ] **多頁面深度掃描**:
    - [ ] 支援 Sitemap 自動爬取與全站分析
    - [ ] 建立網站級信任指紋

### Phase 7: Ecosystem & API Economy (Q3 2026)
- [ ] **Public API**: 開放 `api.trust-wedo.com` 供開發者串接
- [ ] **Browser Extension**: Chrome/Edge 插件即時查看信任分數
- [ ] **Trust Badge**: 可信度標章供網站嵌入

---

## 🐛 已知問題與技術債 (Known Issues)

| Priority | Issue | Description | Target Phase |
|----------|-------|-------------|--------------|
| **P0** | **Schema.org 解析失敗** | 掃描器未解析 JSON-LD 內容,導致評分錯誤 (Apple.com 僅 35 分) | Phase 5 |
| **P0** | **評分邏輯不合理** | 缺少 Schema 直接扣 20 分,無法反映真實品質 | Phase 5 |
| **P1** | **Dependency Sync** | Root `pyproject.toml` 與 Backend `requirements.txt` 需手動同步 | Phase 5 |
| **P2** | **Test Coverage** | 核心庫測試覆蓋率需提升至 80% 以上 | Phase 5 |
| **P2** | **Mobile UX** | 報告頁面手機版優化 | Phase 5 |

---

## 🎯 Next Sprint Focus (Phase 5 優先項目)

1. **修復 Schema.org 解析**: 在 `site_parser.py` 新增 `_parse_jsonld()` 方法
2. **重構評分系統**: 實作 100 分制五大維度評分
3. **視覺化元件**: 雷達圖與維度進度條
4. **文案優化**: 去技術化,加入快速勝利建議

**詳細計劃**: 請參閱專案診斷報告與實施計劃 (artifacts)
