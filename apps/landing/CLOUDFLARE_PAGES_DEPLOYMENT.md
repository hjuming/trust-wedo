# Cloudflare Pages 部署指南

## 目前正式設定

Trust WEDO landing app 由 Cloudflare Pages 專案 `trust-wedo` 部署。

| 項目 | 設定 |
|------|------|
| Project name | `trust-wedo` |
| Production branch | `main` |
| Root directory | `apps/landing` |
| Build command | `npm install && npm run build` |
| Build output directory | `dist` |
| Build watch paths | `*` |
| Auto deploy | Enabled |

## 必要環境變數

在 Cloudflare Pages `Settings -> Variables and Secrets` 設定：

| 變數 | 說明 |
|------|------|
| `VITE_SUPABASE_URL` | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key |
| `VITE_API_URL` | API base URL。如果尚未部署 API，可暫時不設定；前端會避免使用舊平台 fallback。 |

不要在 Cloudflare Pages 前端放入 service role key、database URL、Twinkle Hub API key 或任何後端密鑰。

## Git 自動部署

Cloudflare Pages 已連接 GitHub repository。推送到 `main` 會觸發 production deployment。

```bash
git push origin main
```

## 本地建置驗證

```bash
cd apps/landing
npm install
npm run build
```

成功後會產生：

```text
dist/
```

## SPA 路由

Cloudflare Pages 需要 `_redirects` 讓 React Router 的深層路由可直接開啟。

```text
public/_redirects
```

內容：

```text
/* /index.html 200
```

## GitHub Actions

`.github/workflows/deploy-landing.yml` 仍可作為手動部署備援，但目前主要部署來源是 Cloudflare Pages Git integration。

如果使用 GitHub Actions，需要 GitHub Secrets：

| Secret | 說明 |
|--------|------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare Pages edit token |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |
| `VITE_SUPABASE_URL` | Supabase URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key |
| `VITE_API_URL` | API base URL |

## 部署後檢查

- Production URL 可載入首頁。
- 直接開啟 `/dashboard` 等 SPA route 不會 404。
- Browser console 不應出現舊平台 API URL。
- 需要 API 的頁面需確認 `VITE_API_URL` 指向目前使用的 Cloudflare API 服務。
