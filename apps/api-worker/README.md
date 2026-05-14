# Trust WEDO API Worker

`apps/api-worker` 是正式部署使用的 Cloudflare Worker API gateway。它負責保護 Twinkle Hub API key，並提供前端需要的 MCP proxy、研究模組與企業實體查核端點。

正式 Worker：

```text
https://trust-wedo-api.hjuming.workers.dev
```

## 部署設定

Cloudflare Workers 專案 `trust-wedo-api` 設定：

| 項目 | 設定 |
|------|------|
| Root directory | repo root |
| Build command | `npm install` |
| Deploy command | `npx wrangler deploy` |
| Wrangler config | `wrangler.jsonc` |
| Node.js version | `>=22` |

repo root 的 `wrangler.jsonc` 指向：

```text
apps/api-worker/src/index.ts
```

## Variables and Secrets

| 名稱 | 類型 | 說明 |
|------|------|------|
| `TWINKLE_HUB_API_KEY` | Secret | Twinkle Hub API key，不可提交到 repo |
| `TWINKLE_HUB_API_ENDPOINT` | Variable | Twinkle Hub MCP endpoint |
| `ALLOWED_ORIGIN` | Variable | 前端網址，例如 `https://trust.wedopr.com` 或 Pages URL |

目前 Worker 不需要：

- `SUPABASE_SERVICE_KEY`
- `DATABASE_URL`
- `SECRET_KEY`

## 端點

| Endpoint | Method | 說明 |
|----------|--------|------|
| `/health` | GET | Worker 健康檢查 |
| `/api/mcp/health` | GET | Twinkle Hub endpoint 健康檢查 |
| `/api/mcp/domains` | GET | 列舉資料領域 |
| `/api/mcp/tools` | GET | 列舉 MCP tools |
| `/api/mcp/search` | POST | 搜尋資料集 |
| `/api/mcp/query` | POST | 查詢資料列 |
| `/api/trust/entity-check` | POST | 企業實體查核 |
| `/api/research/modules` | GET | 列舉研究模組 |
| `/api/research/modules/:id` | GET | 取得特定研究模組 |
| `/api/research/path` | POST | 生成研究路徑 |

## 本地檢查

```bash
npm install
npm run typecheck
npx wrangler dev
```

## Production smoke checks

```bash
curl https://trust-wedo-api.hjuming.workers.dev/health
curl https://trust-wedo-api.hjuming.workers.dev/api/research/modules
curl https://trust-wedo-api.hjuming.workers.dev/api/mcp/domains
```

Entity Check 範例請勿把真實客戶資料或私有資料提交到 repo。測試時以公開公司登記資料為限。

## 下一階段建議

- 補 Worker route tests。
- Mock Twinkle Hub responses，避免測試依賴外部服務。
- 將 entity-check scoring 拆成獨立純函式。
- 加入查核紀錄儲存流程前，先完成 Supabase RLS 設計。
