# WEDO Data Verification Agent Lab Frontend

`apps/landing` 是 Cloudflare Pages 前台，包含首頁、定價資訊、研究模組入口與企業實體查核頁。

正式網址：

```text
https://trust.wedopr.com
https://trust.wedopr.com/entity-check
https://trust.wedopr.com/pricing
```

## 目前頁面

| Route | 狀態 | 說明 |
|-------|------|------|
| `/` | Production | WEDO 資料查核 Agent Lab 首頁，串接研究模組與 MCP domains。 |
| `/entity-check` | Production Beta | 企業實體查核，呼叫 Worker `/api/trust/entity-check`。 |
| `/pricing` | Production Beta | Beta 測試版免費方案，保留前一版定價內容。 |
| `/login`, `/signup`, `/dashboard` | Beta / Reserved | 保留 Supabase Auth 與後續工作台入口。 |

## 本地開發

```bash
npm install
npm run dev
```

預設網址：

```text
http://localhost:5173
```

## 建置

```bash
npm run build
npm run preview
```

## 技術棧

- Vite
- React 19
- React Router 7
- TypeScript
- Tailwind CSS
- Supabase client

## Cloudflare Pages 設定

| 項目 | 設定 |
|------|------|
| Project | `trust-wedo` |
| Production branch | `main` |
| Root directory | `apps/landing` |
| Build command | `npm install && npm run build` |
| Build output directory | `dist` |

## 環境變數

| 變數 | 用途 |
|------|------|
| `VITE_API_URL` | API Worker base URL，例如 `https://trust-wedo-api.hjuming.workers.dev` |
| `VITE_SUPABASE_URL` | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key，需搭配 RLS |

不要在前端環境變數放入：

- `TWINKLE_HUB_API_KEY`
- `SUPABASE_SERVICE_KEY`
- `DATABASE_URL`
- `SECRET_KEY`

## 主要結構

```text
apps/landing/
├── src/
│   ├── components/
│   │   ├── EntityCheck/
│   │   ├── Footer.tsx
│   │   ├── Navigation.tsx
│   │   └── PricingSection.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── EntityCheck.tsx
│   │   ├── Pricing.tsx
│   │   └── Dashboard.tsx
│   ├── contexts/
│   ├── i18n/
│   └── main.tsx
├── public/
│   └── _redirects
└── package.json
```

## Entity Check Flow

1. 使用者輸入公司名稱、統一編號與網站 URL。
2. 前端驗證統一編號格式。
3. 前端呼叫 `${VITE_API_URL}/api/trust/entity-check`。
4. Worker 查詢 Twinkle Hub 公開資料。
5. 前端顯示查核報告、風險訊號、網站訊號與資料來源。

## 驗收標準

- 首頁可載入研究模組與資料領域。
- `/entity-check` 可完成查核流程。
- `/pricing` 可直接看到 Beta 免費方案。
- 報告在 mobile / desktop 都不溢位。
- Browser console 不出現 CORS、mixed content 或缺少 env 的錯誤。
- 不在前端 bundle 內出現任何 secret。

## 下一階段建議

- 將 Entity Check 報告支援 PDF / Markdown export。
- 補 Playwright E2E：首頁 smoke、實體查核 happy path、API fail state、定價頁 smoke。
- 整理 i18n namespace，讓 `entityCheck` 文案集中維護。
