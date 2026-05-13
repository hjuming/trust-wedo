# 🚀 Trust WEDO 生產部署指南

## 📋 部署檢查清單

Entity Check MVP 已成功推送到 GitHub (`commit b431d32`)。現在進行以下步驟以部署到生產環境。

---

## ✅ 方案一：自動部署（推薦）- 使用 Cloudflare Pages + GitHub Actions

### 步驟 1：配置 Cloudflare 認證

1. **取得 Cloudflare 認證資料**：
   - 登入 Cloudflare Dashboard: https://dash.cloudflare.com/
   - 前往帳戶設定 > API Tokens
   - 建立新的 API Token（權限：`Cloudflare Pages - Edit`）
   - 複製 Token

2. **設定 GitHub Secrets**：
   - 前往你的倉庫: https://github.com/hjuming/trust-wedo
   - Settings > Secrets and variables > Actions
   - 新增以下 Secrets：

   ```
   CLOUDFLARE_API_TOKEN = [上面複製的 Token]
   CLOUDFLARE_ACCOUNT_ID = [你的 Cloudflare Account ID]
   VITE_SUPABASE_URL = [Supabase URL]
   VITE_SUPABASE_ANON_KEY = [Supabase Anon Key]
   VITE_API_URL = https://trust-wedo-api.zeabur.app (或你的後端 URL)
   ```

   > 📌 查找 Cloudflare Account ID：
   > - 右上角帳戶選單 > Accounts
   > - 複製 Account ID

### 步驟 2：連接到 Cloudflare Pages

1. **在 Cloudflare 中建立 Pages 專案**：
   - Workers & Pages > Pages
   - Create > Connect to Git
   - 授權 Cloudflare 存取 GitHub
   - 選擇 `hjuming/trust-wedo` 倉庫

2. **配置建置設定**：
   - **Branch to deploy**: `main`
   - **Framework preset**: `Vite`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `apps/landing`
   - **Environment variables**:
     - `NODE_VERSION`: `18`

3. **保存並部署**

### 步驟 3：驗證部署

- 推送新的 commit 到 main 分支
- 前往 GitHub Actions 檢查工作流運行狀態
- 前往 Cloudflare Pages 檢查部署日誌
- 訪問你的部署 URL（通常是 `https://trust-wedo.pages.dev`）

---

## 方案二：手動部署

### 使用 Wrangler CLI 部署

```bash
# 1. 進入前端目錄
cd apps/landing

# 2. 構建應用
npm run build

# 3. 登入 Cloudflare
npx wrangler login

# 4. 部署
npx wrangler pages deploy dist --project-name trust-wedo
```

---

## 🔒 環境變數配置

### `.env.production` 設定

在 `apps/landing` 目錄新增或修改 `.env.production`：

```bash
# Supabase 設定
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# Backend API（生產環境）
VITE_API_URL=https://trust-wedo-api.zeabur.app

# 或使用環境變數（推薦用於敏感資料）
```

---

## 🧪 部署前測試

### 本地生產構建驗證

```bash
cd apps/landing

# 構建
npm run build

# 預覽生產構建
npm run preview

# 訪問 http://localhost:4173
```

### Entity Check 功能測試

1. 訪問 `/entity-check` 頁面
2. 輸入測試公司資料：
   - 公司名稱：`擎天金屬股份有限公司`
   - 統一編號：`04595257`
   - 網站 URL：`https://example.com`（選填）
3. 驗證：
   - ✅ 報告正確顯示公司資訊
   - ✅ 風險訊號正確解析
   - ✅ 信任評分計算正確

---

## 📊 部署後檢查

| 項目 | 檢查點 |
|------|--------|
| **首頁** | 訪問 `/` 確認首頁載入無誤 |
| **Entity Check** | 訪問 `/entity-check` 測試功能 |
| **API 連接** | 確認前端能呼叫後端 API |
| **性能** | 檢查 Lighthouse 評分 |
| **安全** | 確認 HTTPS 啟用，無混合內容警告 |

---

## 🔧 後端整合（如需）

### 配置後端 API URL

如果後端使用 Zeabur 部署：

1. **後端部署指南**：
   ```bash
   cd apps/backend
   zeabur deploy
   ```

2. **更新前端 API 地址**：
   - GitHub Secrets: `VITE_API_URL`
   - 或修改 `CLOUDFLARE_API_URL` 環境變數

---

## 🚨 常見問題排查

### Q1: 部署失敗 - "Cannot find module"
**解決**：確認所有新文件已提交到 git
```bash
git status
git add apps/landing/src/components/EntityCheck/
git commit -m "fix: add missing EntityCheck components"
git push origin main
```

### Q2: API 調用失敗 (CORS 錯誤)
**解決**：後端需配置 CORS 允許 Cloudflare Pages 域名
```python
# apps/backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trust-wedo.pages.dev", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q3: 環境變數未生效
**解決**：
- 確認 GitHub Secrets 已正確設定
- 重新運行 GitHub Actions workflow
- 檢查 Cloudflare Pages 環境變數是否已同步

---

## 📚 相關資源

- [Cloudflare Pages 文檔](https://developers.cloudflare.com/pages/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Vite 部署指南](https://vitejs.dev/guide/static-deploy.html)

---

## ✨ 部署後功能

生產環境中 Entity Check 將提供：

✅ **企業實體查核**：輸入統編查詢登記狀態
✅ **風險訊號分析**：自動識別公司狀態異常
✅ **信任評分**：基於多維度計算可信度
✅ **多語言支援**：繁體中文、英文
✅ **響應式設計**：手機、平板、電腦完整支援
