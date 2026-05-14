# WEDO 資料查核 Agent Lab

WEDO 資料查核 Agent Lab 是一個部署在 Cloudflare 的公開資料查核產品入口。它把 Twinkle Hub MCP、研究模組與企業實體查核流程整合成可追溯、可引用、適合 AIO 工作流的查核介面。

目前正式站點：

| 項目 | URL |
|------|-----|
| 前台 | https://trust.wedopr.com |
| 實體查核 | https://trust.wedopr.com/entity-check |
| 定價方案 | https://trust.wedopr.com/pricing |
| API Worker | https://trust-wedo-api.hjuming.workers.dev |

> 查核結果僅供公開資料整理與研究參考，不構成法律、財務、醫療或投資建議。所有結論仍需人工複核。

---

## 目前狀態

| 模組 | 狀態 | 說明 |
|------|------|------|
| 首頁 | 已上線 | 已改版為 WEDO 資料查核 Agent Lab 風格，保留頁首、頁尾、定價方案與研究模組入口。 |
| 企業實體查核 | 已上線 | `/entity-check` 可輸入公司名稱、統一編號與網站 URL，串接 Worker 查詢公開資料。 |
| 定價方案 | 已上線 | `/pricing` 已恢復 Beta 測試版免費方案內容。 |
| API Worker | 已上線 | `trust-wedo-api` 提供 Twinkle Hub MCP proxy、研究模組與實體查核端點。 |
| Twinkle Hub MCP | 已接通 | Worker 透過 MCP JSON-RPC / SSE 流程呼叫 Twinkle Hub，不讓前端直接持有 API key。 |
| Supabase | 前端 env 已保留 | 現階段主要保留帳號與後續資料儲存能力，Worker 尚未直接連接資料庫。 |

---

## 核心功能

### 1. 企業實體查核

- 驗證統一編號格式。
- 查詢公司登記公開資料。
- 顯示公司名稱、登記狀態、地址、登記機關、資本額與資料來源。
- 產出初步信任評分、風險訊號與網站訊號。
- 於報告底部標示資料來源與免責聲明。

### 2. WEDO 資料查核 Agent Lab 首頁

- 展示資料查核流程與 Agent Lab 定位。
- 呼叫 `/api/research/modules` 載入 12 個研究模組。
- 呼叫 `/api/mcp/domains` 載入 Twinkle Hub 可用資料領域。
- 保留頁首導航、頁尾資訊、CTA 與 Beta 定價方案。

### 3. MCP API Proxy

前端不直接呼叫 Twinkle Hub。所有 MCP 查詢都經由 Cloudflare Worker：

| Endpoint | 用途 |
|----------|------|
| `GET /health` | Worker 健康檢查 |
| `GET /api/mcp/health` | Twinkle Hub endpoint 健康檢查 |
| `GET /api/mcp/domains` | 列舉可用資料領域 |
| `GET /api/mcp/tools` | 列舉 MCP tools |
| `POST /api/mcp/search` | 搜尋資料集 |
| `POST /api/mcp/query` | 查詢資料列 |
| `POST /api/trust/entity-check` | 企業實體查核 |
| `GET /api/research/modules` | 列舉研究模組 |
| `GET /api/research/modules/:id` | 取得單一研究模組 |
| `POST /api/research/path` | 生成研究路徑 |

---

## 技術架構

| Layer | Technology | Location | 說明 |
|-------|------------|----------|------|
| Frontend | React 19, Vite, Tailwind CSS | `apps/landing` | Cloudflare Pages 前台、定價頁與實體查核頁。 |
| API Gateway | Cloudflare Workers, TypeScript, Wrangler | `apps/api-worker` | Twinkle Hub MCP proxy、研究模組與查核 API。 |
| Legacy Backend | FastAPI, Python | `apps/backend` | 保留早期後端原型與遷移參考，目前正式部署不使用。 |
| Database | Supabase | external | 前端環境變數已保留，後續可用於帳號、查核紀錄與專案資料。 |
| Deployment | Cloudflare Pages + Workers | Cloudflare | Git push 到 `main` 觸發部署。 |

---

## 本地開發

### 前置需求

- Node.js 22+
- npm 10+
- Cloudflare Wrangler 4+

### Frontend

```bash
cd apps/landing
npm install
npm run dev
```

本地預設網址：

```text
http://localhost:5173
```

### API Worker

```bash
npm install
npm run typecheck
npx wrangler dev
```

---

## 環境變數

### Cloudflare Pages: `trust-wedo`

| 變數 | 用途 | 是否可公開 |
|------|------|------------|
| `VITE_API_URL` | 前端呼叫 API Worker 的 base URL | 是 |
| `VITE_SUPABASE_URL` | Supabase project URL | 是 |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key，需搭配 RLS | 是 |
| `ALLOWED_ORIGIN` | 前端正式網域，供部署紀錄與 CORS 對齊 | 是 |

### Cloudflare Worker: `trust-wedo-api`

| 變數 | 類型 | 用途 |
|------|------|------|
| `TWINKLE_HUB_API_ENDPOINT` | Variable | Twinkle Hub MCP endpoint |
| `TWINKLE_HUB_API_KEY` | Secret | Twinkle Hub API key，不可提交到 repo |
| `ALLOWED_ORIGIN` | Variable | 允許呼叫 Worker 的前端 origin |

禁止把下列值放進前端或提交到 repo：

| 禁止項目 | 原因 |
|----------|------|
| `SUPABASE_SERVICE_KEY` | 高權限 service role key |
| `DATABASE_URL` | 資料庫連線字串 |
| `TWINKLE_HUB_API_KEY` | 外部 API 金鑰 |
| `SECRET_KEY` | 後端簽章密鑰 |

---

## 部署

### Cloudflare Pages

| 項目 | 設定 |
|------|------|
| Project | `trust-wedo` |
| Production branch | `main` |
| Root directory | `apps/landing` |
| Build command | `npm install && npm run build` |
| Build output directory | `dist` |

### Cloudflare Worker

| 項目 | 設定 |
|------|------|
| Worker | `trust-wedo-api` |
| Root directory | repo root |
| Build command | `npm install` |
| Deploy command | `npx wrangler deploy` |
| Config | `wrangler.jsonc` |

更多細節見 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)。

---

## 驗證指令

```bash
# Frontend build
cd apps/landing
npm run build

# Worker typecheck
cd ../..
npm run typecheck

# Production smoke checks
curl https://trust-wedo-api.hjuming.workers.dev/health
curl https://trust-wedo-api.hjuming.workers.dev/api/research/modules
```

---

## 文件索引

- [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md): 目前進度、已完成項目與下一階段建議。
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md): Cloudflare Pages / Workers 部署設定。
- [apps/landing/README.md](apps/landing/README.md): 前台開發與頁面結構。
- [apps/api-worker/README.md](apps/api-worker/README.md): Worker API gateway 設定。
- [PRODUCT.md](PRODUCT.md): 早期 Trust WEDO MVP 產品定義，保留作為歷史參考。
- [docs/technical-specs/README.md](docs/technical-specs/README.md): AI Citation / Entity Confidence 技術規格。

---

## 下一階段摘要

1. 建立查核紀錄儲存與查詢歷史。
2. 將實體查核報告升級為可下載、可引用的 PDF/Markdown。
3. 將風險訊號拆成可解釋的 evidence blocks。
4. 補齊 Worker 與前端的單元測試、E2E 測試與 CI。
5. 設計使用者登入後的 Agent Lab 工作台。

---

MIT © Trust WEDO Team
