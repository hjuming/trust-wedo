# Development Status

> Last updated: 2026-05-15
> Current production target: Cloudflare Pages + Cloudflare Workers

## 產品定位

WEDO 資料查核 Agent Lab 是一個公開資料查核與研究工作流入口。現階段重點是讓使用者可以用最小輸入完成企業實體初查，並把 Twinkle Hub MCP 的公開資料能力包成安全的 Worker API。

## 目前狀態

| Area | Status | 說明 |
|------|--------|------|
| Cloudflare Pages 前台 | Production | `trust.wedopr.com` 已上線，首頁已改為 WEDO 資料查核 Agent Lab。 |
| Entity Check | Production Beta | `/entity-check` 已改版並可查到公司登記公開資料。 |
| Pricing | Production Beta | `/pricing` 已恢復 Beta 測試版免費方案內容。 |
| Cloudflare Worker API | Production Beta | `trust-wedo-api` 已上線，提供 MCP proxy、研究模組、企業實體查核。 |
| Twinkle Hub MCP | Connected | Worker 使用 MCP JSON-RPC / SSE protocol 呼叫 Twinkle Hub。 |
| Research Modules | Available | 已提供 12 個研究模組供首頁與研究路徑使用。 |
| Supabase | Reserved | 前端 env 保留，尚未成為 Worker 查核流程的必要依賴。 |
| Legacy FastAPI Backend | Archived / Reference | `apps/backend` 保留為原型參考，正式部署以 Cloudflare Worker 為準。 |

## 已完成成果

### Phase 1: MCP 與研究模組原型

- 建立 Twinkle MCP 客戶端與 FastAPI route 原型。
- 設計 `/api/mcp/*`、`/api/research/*` 基礎端點。
- 建立 12 個研究模組種子資料。
- 產出初版遷移與部署策略文件。

### Phase 2: Cloudflare Worker 遷移

- 建立 `apps/api-worker` 作為正式 API gateway。
- 以 `wrangler.jsonc` 管理 `trust-wedo-api` 部署。
- 修正 Cloudflare Workers compatibility date 與 root package 設定。
- 確認 Worker `/health` 與 `/api/research/modules` 可在 production 存取。

### Phase 3: Twinkle Hub MCP 接通

- 修正 MCP protocol 呼叫流程。
- 支援 Twinkle Hub stateless session。
- 正規化 MCP 查詢結果數量與錯誤訊息。
- 透過 Worker secret 保存 `TWINKLE_HUB_API_KEY`，前端不直接接觸外部 API key。

### Phase 4: 前台 Agent Lab 改版

- 首頁改為 WEDO 資料查核 Agent Lab。
- 保留頁首、頁尾、定價方案與可用產品資訊。
- 首頁串接研究模組與 MCP domains。
- 補齊 Cloudflare Pages 環境變數與 Worker CORS 設定。

### Phase 5: 企業實體查核與定價頁完善

- `/entity-check` 已套用首頁一致的深色 hero 與白色報告卡片風格。
- 查核表單支援公司名稱、統一編號與公司網站 URL。
- 查核結果分為 Verification Report、Registry Data、Risk Signals、Website Signal、Sources 與免責聲明。
- 已確認線上可查到公司登記資料。
- `/pricing` 已建立獨立頁面並放回前一版 Beta 免費方案內容。

## 目前 API Surface

| Endpoint | Method | Status | 說明 |
|----------|--------|--------|------|
| `/health` | GET | Live | Worker 健康檢查 |
| `/api/mcp/health` | GET | Live | Twinkle Hub endpoint 健康檢查 |
| `/api/mcp/domains` | GET | Live | 列舉資料領域 |
| `/api/mcp/tools` | GET | Live | 列舉 MCP tools |
| `/api/mcp/search` | POST | Live | 搜尋資料集 |
| `/api/mcp/query` | POST | Live | 查詢資料列 |
| `/api/trust/entity-check` | POST | Live | 企業實體查核 |
| `/api/research/modules` | GET | Live | 研究模組列表 |
| `/api/research/modules/:id` | GET | Live | 單一研究模組 |
| `/api/research/path` | POST | Live | 研究路徑生成 |

## 已知限制

| Priority | Issue | Impact | 建議處理 |
|----------|-------|--------|----------|
| P0 | 查核結果尚未儲存 | 使用者無法回看歷史查核 | 建立 Supabase `entity_checks` table 與 RLS。 |
| P0 | 實體查核信任分數仍是初版 heuristic | 分數可解釋性不足 | 拆出 scoring model 與 evidence blocks。 |
| P1 | Worker 測試覆蓋不足 | API regression 風險較高 | 補 Vitest / Miniflare 測試。 |
| P1 | 前端 E2E 尚未建立 | 部署後需人工驗證 | 補 Playwright smoke tests。 |
| P2 | i18n 結構有歷史殘留 | 文案維護成本上升 | 整理 `entityCheck` 與首頁文案 namespace。 |
| P2 | Legacy FastAPI 文件仍需標註歷史狀態 | 新開發者可能混淆正式後端 | 已於 README 標註，後續可移至 archive docs。 |

## 下一階段開發建議

### Phase 6: 查核紀錄與報告保存

目標：讓 Entity Check 從一次性工具變成可追溯的查核工作台。

- 建立 Supabase tables：`entity_checks`、`entity_check_sources`、`entity_check_events`。
- Worker 新增 authenticated save flow。
- 前端新增查核歷史列表。
- 報告頁支援 stable URL。

驗收標準：

- 使用者可登入後保存查核紀錄。
- 每筆查核都保留來源、查詢時間、輸入條件與輸出版本。
- 未登入使用者仍可執行一次性查核。

### Phase 7: Evidence-based Scoring

目標：讓信任分數從單一數字變成可解釋的評估結果。

- 將分數拆為 Registration Match、Registry Status、Website Consistency、Source Completeness、Risk Signals。
- 每個維度輸出 evidence、confidence、limitation。
- 報告 UI 顯示分數來源，而不是只顯示總分。

驗收標準：

- 每個扣分都有可讀理由。
- 每個加分都有資料來源。
- 報告可被人工複核與引用。

### Phase 8: Report Export

目標：讓查核報告可交付給客戶或內部團隊。

- 產出 Markdown 報告。
- 產出列印友善 PDF。
- 補「資料來源與限制」固定段落。
- 增加報告版本與產生時間。

驗收標準：

- 同一筆查核可下載 PDF。
- PDF 與網頁內容一致。
- 不含任何 secret 或內部 debug 資訊。

### Phase 9: Test and CI Hardening

目標：降低 Cloudflare 自動部署風險。

- Worker route tests 與 mocked Twinkle Hub responses。
- Frontend production build、entity-check E2E、homepage smoke test。
- GitHub Actions PR check 與 main branch deploy preflight。

驗收標準：

- 每次 push 前至少跑過 frontend build 與 Worker typecheck。
- 主要 API route 有 regression tests。
- Cloudflare deploy 失敗時文件有 rollback 指引。

## 當前 Sprint 建議

1. 先做 Phase 6 的資料表設計與儲存流程。
2. 同步補 Worker route tests，避免 MCP 與 CORS regression。
3. 再做報告 evidence model，避免先做漂亮 UI 但分數不可解釋。
4. 最後補 PDF/Markdown export，讓成果可交付。

## 維護原則

- 正式 API 以 `apps/api-worker` 為準。
- 正式前台以 `apps/landing` 為準。
- `apps/backend` 為歷史原型，不作為 Cloudflare production backend。
- 不在文件、commit、PR 或 issue 中揭露 API key、service role key、database URL。
- 查核結果需附資料來源、查詢時間與限制說明。
