# Trust WEDO Cloudflare Pages 部署指南

## 部署結論

Trust WEDO 目前以 **Cloudflare Pages** 作為正式前端部署平台。

目前 Cloudflare Pages 專案設定如下：

| 項目 | 設定 |
|------|------|
| Cloudflare project | `trust-wedo` |
| Production branch | `main` |
| Root directory | `apps/landing` |
| Build command | `npm install && npm run build` |
| Build output directory | `dist` |
| Build system version | `3` |
| Auto deploy | Enabled |

> 注意：Cloudflare Pages 此設定只會建置 `apps/landing` 前端。`apps/backend` FastAPI 服務不會被這個 Pages 專案部署。若未來需要後端 API 上 Cloudflare，應另建 Cloudflare Workers / Pages Functions 服務，不要使用舊平台文件作為部署依據。

## 環境變數

Cloudflare Pages 的 `Settings -> Variables and Secrets` 需設定：

| 變數 | 用途 | 安全性 |
|------|------|--------|
| `VITE_SUPABASE_URL` | 前端連接 Supabase | 可公開 |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key | 可公開，但需搭配 RLS |
| `VITE_API_URL` | 前端呼叫 API 的 base URL | 可公開 |

不要在 Cloudflare Pages 前端設定：

| 禁止放在前端的變數 | 原因 |
|-------------------|------|
| `SUPABASE_SERVICE_KEY` | service role key 具高權限 |
| `DATABASE_URL` | 資料庫連線字串 |
| `TWINKLE_HUB_API_KEY` | 外部 API 金鑰 |
| `SECRET_KEY` | 後端簽章密鑰 |

## Git 部署流程

Cloudflare Pages 已啟用 Git integration 與 main 分支自動部署。

```bash
git status
git add <changed-files>
git commit -m "docs: align deployment docs with cloudflare pages"
git push origin main
```

推送到 `main` 後，Cloudflare Pages 會自動觸發 production deployment。

## 本地部署前檢查

```bash
cd apps/landing
npm install
npm run build
```

成功時應產生：

```text
apps/landing/dist
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
- 若新增 Cloudflare Workers / Pages Functions 後端，需另建獨立文件，並明確標示服務名稱、root directory、build command 與 secrets。
