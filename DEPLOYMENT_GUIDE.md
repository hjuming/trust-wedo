# Trust WEDO Cloudflare 部署指南

## 部署結論

Trust WEDO 正式部署分成兩個 Cloudflare 服務：

| 服務 | Cloudflare 類型 | 用途 | Root directory |
|------|-----------------|------|----------------|
| `trust-wedo` | Pages | React/Vite 前端 | `apps/landing` |
| `trust-wedo-api` | Workers | API gateway / Twinkle Hub proxy | repo root |

> 重要：Cloudflare Workers 目前會在 repo root 執行 build/deploy。repo root 已提供 `package.json` 與 `wrangler.jsonc`，Worker 程式碼仍集中在 `apps/api-worker`。

## 前端：Cloudflare Pages

Cloudflare Pages 專案設定如下：

| 項目 | 設定 |
|------|------|
| Cloudflare project | `trust-wedo` |
| Production branch | `main` |
| Root directory | `apps/landing` |
| Build command | `npm install && npm run build` |
| Build output directory | `dist` |
| Build system version | `3` |
| Auto deploy | Enabled |

> 注意：Cloudflare Pages 此設定只會建置 `apps/landing` 前端。`apps/backend` FastAPI 服務不會被這個 Pages 專案部署。

## API：Cloudflare Workers

Cloudflare Workers 專案設定如下：

| 項目 | 設定 |
|------|------|
| Cloudflare Worker | `trust-wedo-api` |
| Root directory | 留空或 repo root |
| Build command | `npm install` |
| Deploy command | `npx wrangler deploy` |
| Wrangler config | `wrangler.jsonc` |
| Node.js version | `>=22` |

Worker 端點：

| Endpoint | 用途 |
|----------|------|
| `GET /health` | Worker 健康檢查 |
| `GET /api/mcp/health` | Twinkle Hub endpoint 健康檢查 |
| `GET /api/mcp/domains` | 列舉資料領域 |
| `GET /api/mcp/tools` | 列舉 MCP tools |
| `POST /api/mcp/search` | 搜尋資料集 |
| `POST /api/mcp/query` | 查詢資料列 |
| `GET /api/research/modules` | 列舉研究模組 |
| `GET /api/research/modules/{id}` | 取得單一研究模組 |
| `POST /api/research/path` | 生成研究路徑 |

## 前端環境變數

Cloudflare Pages 的 `Settings -> Variables and Secrets` 需設定：

| 變數 | 用途 | 安全性 |
|------|------|--------|
| `VITE_SUPABASE_URL` | 前端連接 Supabase | 可公開 |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key | 可公開，但需搭配 RLS |
| `VITE_API_URL` | 前端呼叫 API 的 base URL，例如 `https://trust-wedo-api.<account>.workers.dev` | 可公開 |

## Worker 環境變數與 Secrets

Cloudflare Workers `trust-wedo-api` 的 `Settings -> Variables and Secrets` 需設定：

| 名稱 | 類型 | 用途 |
|------|------|------|
| `TWINKLE_HUB_API_KEY` | Secret | 後端呼叫 Twinkle Hub 的 API key |
| `TWINKLE_HUB_API_ENDPOINT` | Variable | 預設 `https://api.twinkleai.tw/mcp/` |
| `ALLOWED_ORIGIN` | Variable | 前端 Pages URL，例如 `https://trust-wedo.pages.dev` |
| `NODE_VERSION` | Variable | 建議設 `22`，符合 Wrangler 4 的 Node 版本需求 |

不要在 Cloudflare Pages 前端設定：

| 禁止放在前端的變數 | 原因 |
|-------------------|------|
| `SUPABASE_SERVICE_KEY` | service role key 具高權限 |
| `DATABASE_URL` | 資料庫連線字串 |
| `TWINKLE_HUB_API_KEY` | 外部 API 金鑰 |
| `SECRET_KEY` | 後端簽章密鑰 |

目前 `trust-wedo-api` Worker 第一版不需要設定：

| 暫不需要 | 原因 |
|----------|------|
| `SUPABASE_SERVICE_KEY` | Worker 尚未直接存取 Supabase |
| `DATABASE_URL` | Worker 尚未直接連接資料庫 |
| `SECRET_KEY` | Worker 尚未簽發或驗證自有 JWT |

## Git 部署流程

Cloudflare Pages 已啟用 Git integration 與 main 分支自動部署。

```bash
git status
git add <changed-files>
git commit -m "docs: align deployment docs with cloudflare pages"
git push origin main
```

推送到 `main` 後，Cloudflare Pages 會自動觸發 production deployment。

若 `trust-wedo-api` Worker 也已連 Git integration，推送到 `main` 後會由 Worker 專案各自觸發部署。

## 本地部署前檢查：前端

```bash
cd apps/landing
npm install
npm run build
```

成功時應產生：

```text
apps/landing/dist
```

## 本地部署前檢查：Worker

```bash
npm install
npm run typecheck
```

## Cloudflare 部署後驗證

部署完成後請檢查：

| 檢查項目 | 方法 |
|----------|------|
| 首頁載入 | 開啟 Cloudflare Pages production URL |
| SPA 路由 | 直接開啟 `/dashboard`、`/entity-check` 等路由 |
| Supabase env | 登入 / 查詢功能是否正常 |
| API env | 需要後端 API 的頁面是否呼叫正確 `VITE_API_URL` |
| Console | Browser console 無舊平台 URL 或 mixed-content 錯誤 |

Worker 部署完成後請檢查：

```bash
curl https://trust-wedo-api.<account>.workers.dev/health
curl https://trust-wedo-api.<account>.workers.dev/api/research/modules
curl https://trust-wedo-api.<account>.workers.dev/api/mcp/health
```

## SPA 路由設定

React Router 在 Cloudflare Pages 需要 fallback 到 `index.html`。

本專案使用：

```text
apps/landing/public/_redirects
```

內容：

```text
/* /index.html 200
```

## 文件維護規則

- 本 repo 的正式部署文件以本檔為準。
- 不再保留舊平台作為 Trust WEDO 正式部署指引。
- Cloudflare Workers 後端以 `apps/api-worker/README.md` 與本檔為準。
