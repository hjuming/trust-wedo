# Frontend URL 設定指南

## 概述

`FRONTEND_URL` 是後端用來生成 PDF 時訪問前端 PDF Template 的 URL。

## 為什麼需要這個變數?

PDF 生成流程:
1. 後端接收 PDF 下載請求
2. 使用 Playwright 啟動 headless browser
3. **訪問 `{FRONTEND_URL}/pdf-report/:scanId`**
4. 渲染頁面並轉換為 PDF
5. 返回 PDF 給客戶端

## 如何設定

### 本地開發環境

在 `apps/backend/.env` 添加:
```bash
FRONTEND_URL=http://localhost:5173
```

**注意**: 確保前端開發服務器正在運行 (`npm run dev`)

### 生產環境 (Cloudflare Pages + Railway/Render)

#### 步驟 1: 確認前端 URL

你的前端部署在 Cloudflare Pages,URL 可能是:
- `https://trust-wedo.pages.dev` (Cloudflare 預設域名)
- `https://your-custom-domain.com` (如果有自定義域名)

#### 步驟 2: 在後端部署平台設定環境變數

**Railway**:
1. 進入 Railway Dashboard
2. 選擇你的 backend service
3. 點擊 "Variables" 標籤
4. 添加新變數:
   - Key: `FRONTEND_URL`
   - Value: `https://trust-wedo.pages.dev` (或你的實際域名)
5. 點擊 "Save" 並重新部署

**Render**:
1. 進入 Render Dashboard
2. 選擇你的 backend service
3. 點擊 "Environment" 標籤
4. 添加新變數:
   - Key: `FRONTEND_URL`
   - Value: `https://trust-wedo.pages.dev`
5. 保存並重新部署

**Zeabur**:
1. 進入 Zeabur Dashboard
2. 選擇你的 project
3. 點擊 backend service
4. 進入 "Variables" 設定
5. 添加 `FRONTEND_URL=https://trust-wedo.pages.dev`

**Docker / Kubernetes**:
```yaml
env:
  - name: FRONTEND_URL
    value: "https://trust-wedo.pages.dev"
```

## 如何獲取 Cloudflare Pages URL?

### 方法 1: Cloudflare Dashboard
1. 登入 Cloudflare Dashboard
2. 進入 "Pages" 區塊
3. 選擇 "trust-wedo" 項目
4. 查看 "Production" 部署的 URL

### 方法 2: 檢查部署日誌
在 Cloudflare Pages 部署成功後,會顯示:
```
✅ Deployment complete!
🌍 https://trust-wedo.pages.dev
```

### 方法 3: 檢查你的前端 .env
```bash
cat apps/landing/.env
# 可能有 VITE_APP_URL 或類似變數
```

## 驗證設定

### 本地測試
```bash
# 1. 確保前端運行
cd apps/landing
npm run dev
# 應該顯示: Local: http://localhost:5173

# 2. 確保後端能訪問前端
curl http://localhost:5173/pdf-report/test-scan-id
# 應該返回 HTML (不是 404)

# 3. 測試 PDF 生成
# 訪問: http://localhost:8000/api/reports/{scanId}/pdf
```

### 生產環境測試
```bash
# 測試前端 PDF template 是否可訪問
curl https://trust-wedo.pages.dev/pdf-report/test-scan-id

# 應該返回 HTML 內容,不是 404 或錯誤
```

## 常見問題

### Q: PDF 生成失敗,錯誤: "Failed to navigate"
**A**: `FRONTEND_URL` 設定錯誤或前端無法訪問
- 檢查 URL 是否正確
- 確保前端已部署且可公開訪問
- 檢查是否有 CORS 或防火牆限制

### Q: PDF 內容為空白
**A**: PDF template 路由可能需要認證
- 確保 `/pdf-report/:scanId` 路由是公開的 (不需要登入)
- 或者在後端使用 service token 訪問

### Q: 本地開發時 PDF 生成很慢
**A**: 這是正常的,因為 Playwright 需要啟動 browser
- 首次生成: ~5-10 秒
- 後續生成: ~2-3 秒

### Q: 生產環境找不到 Chromium
**A**: Docker image 可能沒有正確安裝 Playwright
- 檢查 Dockerfile 是否包含 `playwright install chromium`
- 重新構建 Docker image

## 安全考量

### 建議: 使用環境變數,不要硬編碼

❌ **不好**:
```python
frontend_url = "https://trust-wedo.pages.dev"  # 硬編碼
```

✅ **好**:
```python
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
```

### 建議: 驗證 URL 格式

```python
from urllib.parse import urlparse

def validate_frontend_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
```

## 快速參考

| 環境 | FRONTEND_URL 值 |
|------|----------------|
| 本地開發 | `http://localhost:5173` |
| Cloudflare Pages (預設) | `https://trust-wedo.pages.dev` |
| 自定義域名 | `https://your-domain.com` |

## 相關文件

- PDF 生成技術文檔: `docs/PDF_REPORT_GENERATION.md`
- 後端環境變數範例: `apps/backend/.env.example`
