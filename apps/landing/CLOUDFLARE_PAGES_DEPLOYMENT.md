# Cloudflare Pages 部署指南 ☁️

## 📋 前置確認

✅ **您的專案已完全相容 Cloudflare Pages**

| 項目 | 狀態 | 說明 |
|------|------|------|
| 框架 | ✅ Vite + React | Cloudflare Pages 原生支援 |
| 建置指令 | ✅ `npm run build` | 已配置 TypeScript 編譯 + Vite 建置 |
| 輸出目錄 | ✅ `dist/` | Vite 預設輸出目錄 |
| Node 版本 | ✅ 18+ | 符合 Cloudflare Pages 要求 |

---

## 🚀 部署方式一：透過 Cloudflare Dashboard（推薦）

### Step 1: 推送程式碼到 GitHub

```bash
cd /Users/MING/Sites/Trust-WEDO

# 確認 Git 狀態
git status

# 新增所有變更
git add apps/landing

# 提交變更
git commit -m "feat: add Trust WEDO landing page MVP"

# 推送到 GitHub
git push origin main
```

### Step 2: 連接 Cloudflare Pages

1. **登入 Cloudflare Dashboard**
   - 前往：https://dash.cloudflare.com/
   - 選擇您的帳號

2. **建立 Pages 專案**
   - 左側選單：**Workers & Pages**
   - 點擊：**Create application** → **Pages** → **Connect to Git**

3. **選擇 Repository**
   - 授權 Cloudflare 存取您的 GitHub
   - 選擇 Repository：`Trust-WEDO`

4. **配置建置設定**

   ```yaml
   Project name: trust-wedo-landing
   Production branch: main
   
   Build settings:
   ├─ Framework preset: Vite
   ├─ Build command: cd apps/landing && npm install && npm run build
   ├─ Build output directory: apps/landing/dist
   └─ Root directory (advanced): apps/landing
   ```

   > [!TIP]
   > 如果設定 **Root directory** 為 `apps/landing`，則 Build command 可簡化為 `npm install && npm run build`，Build output directory 改為 `dist`

5. **環境變數**（選填）
   - `NODE_VERSION`: `18`（如果需要指定版本）

6. **部署**
   - 點擊 **Save and Deploy**
   - 等待建置完成（約 1-2 分鐘）

### Step 3: 取得部署網址

部署完成後，您會得到：
- **Production URL**: `https://trust-wedo-landing.pages.dev`
- **Custom Domain**: 可在 Pages 設定中綁定自訂網域

---

## 🔧 部署方式二：使用 Wrangler CLI

### Step 1: 安裝 Wrangler

```bash
npm install -g wrangler
```

### Step 2: 登入 Cloudflare

```bash
wrangler login
```

### Step 3: 建置專案

```bash
cd /Users/MING/Sites/Trust-WEDO/apps/landing
npm run build
```

### Step 4: 部署

```bash
wrangler pages deploy dist --project-name=trust-wedo-landing
```

---

## ⚙️ 自動部署設定

### GitHub Actions 自動化（選填）

如果您想要更精細的控制，可以建立 GitHub Actions workflow：

**檔案位置**: `.github/workflows/deploy-landing.yml`

```yaml
name: Deploy Landing Page to Cloudflare Pages

on:
  push:
    branches:
      - main
    paths:
      - 'apps/landing/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd apps/landing
          npm ci

      - name: Build
        run: |
          cd apps/landing
          npm run build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: trust-wedo-landing
          directory: apps/landing/dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**設定 Secrets**:
1. 前往 GitHub Repository → Settings → Secrets and variables → Actions
2. 新增以下 secrets：
   - `CLOUDFLARE_API_TOKEN`: 從 Cloudflare Dashboard → My Profile → API Tokens 建立
   - `CLOUDFLARE_ACCOUNT_ID`: 從 Cloudflare Dashboard URL 取得

---

## 🔄 自動同步機制

### Cloudflare Pages 自動部署觸發條件

| 事件 | 行為 |
|------|------|
| **Push to `main`** | 自動觸發 Production 部署 |
| **Push to 其他分支** | 自動建立 Preview 部署 |
| **Pull Request** | 自動建立 Preview 部署並留言 PR |

### Preview 部署網址格式
```
https://<commit-hash>.trust-wedo-landing.pages.dev
```

---

## 🎯 建議的 Git 工作流程

```bash
# 開發新功能
git checkout -b feature/new-section
# ... 進行開發 ...
git add .
git commit -m "feat: add new section"
git push origin feature/new-section

# 在 GitHub 建立 Pull Request
# → Cloudflare Pages 自動建立 Preview 部署

# 合併到 main
git checkout main
git merge feature/new-section
git push origin main

# → Cloudflare Pages 自動部署到 Production
```

---

## 📊 部署後驗證

### 檢查清單

- [ ] Production URL 可正常存取
- [ ] Dark Mode 切換功能正常
- [ ] 響應式設計在移動端正常顯示
- [ ] 所有靜態資源（Logo、圖片）正確載入
- [ ] Console 無錯誤訊息

### 效能測試

建議使用以下工具測試：
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [WebPageTest](https://www.webpagetest.org/)
- Cloudflare Analytics（內建）

---

## 🔧 常見問題排解

### Q1: 建置失敗 - "Module not found"
**解決方案**: 確認 `package.json` 中的 dependencies 完整，執行 `npm install` 後再推送。

### Q2: 路由 404 錯誤（React Router）
**解決方案**: Cloudflare Pages 需要額外配置 SPA 路由。

建立檔案：`apps/landing/public/_redirects`
```
/*    /index.html   200
```

### Q3: 環境變數未生效
**解決方案**: 在 Cloudflare Pages 設定中新增環境變數，並重新部署。

---

## 🎉 完成！

部署完成後，您的 Landing Page 將會：
- ✅ 自動從 GitHub 同步
- ✅ 每次 Push 自動重新部署
- ✅ 享受 Cloudflare 全球 CDN 加速
- ✅ 免費 SSL 憑證
- ✅ 無限流量與頻寬

**下一步建議**：
1. 綁定自訂網域（例如：`landing.trustwedo.com`）
2. 設定 Cloudflare Analytics 追蹤流量
3. 啟用 Web Analytics（隱私友善的分析工具）
