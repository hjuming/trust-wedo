# Trust WEDO API Worker

Cloudflare Worker for the Trust WEDO API gateway.

## Cloudflare Worker 設定

在 Cloudflare Workers 建立 `trust-wedo-api`，Git 連結本 repo 後設定：

| 項目 | 設定 |
|------|------|
| Root directory | `apps/api-worker` |
| Build command | `npm install` |
| Deploy command | `npx wrangler deploy` |
| Node.js version | `>=22` |

## Variables and Secrets

| 名稱 | 類型 | 說明 |
|------|------|------|
| `TWINKLE_HUB_API_KEY` | Secret | Twinkle Hub API key，不可提交到 repo |
| `TWINKLE_HUB_API_ENDPOINT` | Variable | 預設 `https://api.twinkleai.tw/mcp/` |
| `ALLOWED_ORIGIN` | Variable | 前端網址，例如 `https://trust-wedo.pages.dev` |
| `NODE_VERSION` | Variable | 建議設 `22`，符合 Wrangler 4 的 Node 版本需求 |

## 本地檢查

```bash
npm install
npm run typecheck
```

## 端點

- `GET /health`
- `GET /api/mcp/health`
- `GET /api/mcp/domains`
- `GET /api/mcp/tools`
- `POST /api/mcp/search`
- `POST /api/mcp/query`
- `GET /api/research/modules`
- `GET /api/research/modules/:id`
- `POST /api/research/path`
