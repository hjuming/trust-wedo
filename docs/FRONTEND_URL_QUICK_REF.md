# Trust WEDO - Frontend URL 設定

## 你的域名

- **Cloudflare Pages 預設**: `https://trust-wedo.pages.dev`
- **自定義域名** (推薦): `https://trust.wedopr.com`

## 環境變數設定

### 本地開發
```bash
# apps/backend/.env
FRONTEND_URL=http://localhost:5173
```
✅ 已設定

### 生產環境
```bash
# 在後端部署平台設定
FRONTEND_URL=https://trust.wedopr.com
```

## 後端部署平台設定步驟

### Railway
1. 進入 https://railway.app
2. 選擇 backend project
3. Settings → Variables
4. 添加:
   ```
   FRONTEND_URL = https://trust.wedopr.com
   ```
5. Deploy

### Render
1. 進入 https://dashboard.render.com
2. 選擇 backend service
3. Environment → Add Environment Variable
4. 添加:
   ```
   Key: FRONTEND_URL
   Value: https://trust.wedopr.com
   ```
5. Save Changes

### Zeabur (你的後端部署平台)
1. 登入 https://dash.zeabur.com
2. 選擇你的 Project
3. 點擊 Backend Service (`trust-wedo`)
4. 進入 **Variables** 標籤
5. 添加變數:
   ```
   Key: FRONTEND_URL
   Value: https://trust.wedopr.com
   ```
6. 點擊 Add 並確認服務重新部署

**注意**: 你的後端網址是 `https://trust-wedo.zeabur.app/`
但 `FRONTEND_URL` 是指**前端**的網址 (`https://trust.wedopr.com`)
後端需要知道前端在哪裡,才能生成 PDF。

### Cloudflare Workers / Pages Functions
1. 進入 Cloudflare Dashboard
2. Workers & Pages → backend
3. Settings → Variables
4. 添加:
   ```
   FRONTEND_URL = https://trust.wedopr.com
   ```

### Docker / Docker Compose
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - FRONTEND_URL=https://trust.wedopr.com
```

或

```bash
# Dockerfile / 啟動命令
docker run -e FRONTEND_URL=https://trust.wedopr.com ...
```

## 驗證

### 測試前端可訪問性
```bash
curl -I https://trust.wedopr.com/pdf-report/test
# 應該返回 HTTP 200
```

### 測試 PDF 生成
1. 完成一次網站掃描
2. 點擊「下載 PDF」
3. 檢查 PDF 是否正確生成

## 雙向連結設定 (重要！)

系統運作需要 **前端** 與 **後端** 互相知道對方的網址：

1. **後端 (Zeabur)** 需要 `FRONTEND_URL` → 用來生成 PDF
2. **前端 (Cloudflare)** 需要 `VITE_API_URL` → 用來呼叫 API

### Cloudflare Pages (你的前端部署平台)

請確保在 **Settings** → **Environment variables** 中設定：

| Variable Name | Value |
|--------------|-------|
| `VITE_API_URL` | `https://trust-wedo.zeabur.app` |
| `VITE_SUPABASE_URL` | *(參考本地 .env)* |
| `VITE_SUPABASE_ANON_KEY` | *(參考本地 .env)* |

**注意**: Cloudflare Pages 設定變數後，必須 **Redeploy** (重新構建) 才會生效！

## 故障排除

### 問題: PDF 生成失敗
```
Error: Failed to navigate to https://trust.wedopr.com/pdf-report/xxx
```

**解決**:
- 檢查 `FRONTEND_URL` 是否正確設定
- 確認前端已部署且可公開訪問
- 重新部署後端服務

### 問題: PDF 內容為空
**解決**:
- 檢查 `/pdf-report/:scanId` 路由是否正常
- 在瀏覽器訪問 `https://trust.wedopr.com/pdf-report/test-id` 確認頁面可載入

## 完成檢查清單

- [ ] 本地 `.env` 已設定 `FRONTEND_URL=http://localhost:5173`
- [ ] 生產環境已設定 `FRONTEND_URL=https://trust.wedopr.com`
- [ ] 前端 URL 可訪問 (curl 測試返回 200)
- [ ] 後端服務已重新部署
- [ ] PDF 生成功能測試通過

---

**最後更新**: 2026-02-15  
**狀態**: ✅ 本地已設定 | ⏳ 生產環境待設定
