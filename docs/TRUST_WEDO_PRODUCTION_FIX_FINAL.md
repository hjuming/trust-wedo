# Trust WEDO 生產環境 Playwright 問題 - 最終診斷

## 🚨 緊急問題

**症狀**: 
- 本地測試: ✅ Playwright 正常 (Size: 70.7KB, Schema: True)
- 生產環境: ❌ 評分仍是 20/100, Schema: 0/30
- 資料庫顯示: `parser_used: "static"` (不是 "playwright")

**結論**: Playwright 在生產環境未被使用!

---

## 🔍 根本原因分析

根據你們的更新說明:

> "inspect_supabase.py 診斷腳本，成功識別出生產環境因環境配置問題靜默退回到 static parser"

這說明**生產環境缺少 Chromium 瀏覽器**或**權限不足**。

### 常見生產環境問題

#### 問題 1: Chromium 未安裝

**檢查方法**:
```bash
# SSH 進入生產服務器
ssh your-server

# 檢查 Playwright 瀏覽器
python3 -c "from playwright.async_api import async_playwright; import asyncio; asyncio.run(async_playwright().start())"
```

**如果報錯**: "Executable doesn't exist at ..."

**解決方法**:
```bash
# 在生產環境執行
playwright install chromium

# 或在 Docker 中
RUN playwright install --with-deps chromium
```

#### 問題 2: Docker/Container 環境缺少依賴

**Dockerfile 必須包含**:
```dockerfile
# 方案 A: 使用官方 Playwright 基礎鏡像
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 方案 B: 手動安裝依賴
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright
RUN playwright install chromium
```

#### 問題 3: 無頭模式權限問題

**檢查**:
```bash
# 在生產環境運行測試
python scripts/verify_playwright.py
```

**如果報錯**: "Permission denied" 或 "Failed to launch browser"

**解決方法**:
```python
# playwright_parser.py 添加參數
browser = await self.playwright.chromium.launch(
    headless=True,
    args=[
        '--no-sandbox',  # ← 關鍵! Docker 環境必須
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',  # 避免共享內存問題
        '--disable-blink-features=AutomationControlled'
    ]
)
```

#### 問題 4: 環境變量未設置

**檢查 `.env` 或環境變量**:
```bash
# 生產環境應該有
PLAYWRIGHT_ENABLED=true
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright  # Docker 路徑
```

---

## ✅ 解決方案

### 方案 A: 使用 Playwright Docker 鏡像 (推薦)

**Dockerfile**:
```dockerfile
# 使用官方 Playwright 鏡像 (已預裝瀏覽器)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# 複製依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製應用
COPY . .

# 不需要額外安裝瀏覽器!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
services:
  backend:
    image: mcr.microsoft.com/playwright/python:v1.40.0-jammy
    build: .
    environment:
      - PLAYWRIGHT_ENABLED=true
    # 不需要額外卷掛載
```

### 方案 B: 手動安裝 (如果不能用官方鏡像)

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
RUN playwright install --with-deps chromium

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 方案 C: 在部署時安裝 (Serverless/PaaS)

如果使用 Vercel, Railway, Fly.io 等 PaaS:

**添加 `playwright.sh` 部署腳本**:
```bash
#!/bin/bash
# 在部署時執行
playwright install chromium
```

**在 `package.json` 或部署配置中調用**:
```json
{
  "scripts": {
    "postinstall": "playwright install chromium"
  }
}
```

---

## 🧪 生產環境驗證步驟

### 步驟 1: SSH 進入生產服務器

```bash
# 連接到生產環境
ssh your-server

# 或進入 Docker 容器
docker exec -it your-container bash
```

### 步驟 2: 檢查 Playwright 狀態

```bash
# 1. 檢查 Python 和 Playwright
python3 --version
pip show playwright

# 2. 檢查瀏覽器安裝
playwright install --dry-run chromium

# 3. 測試瀏覽器啟動
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    print('✓ Browser launched successfully')
    browser.close()
"
```

**預期輸出**:
```
✓ Browser launched successfully
```

**如果失敗**,會看到錯誤訊息,例如:
- `Executable doesn't exist at /ms-playwright/chromium-1091/chrome-linux/chrome`
- `Permission denied`
- `Failed to launch browser`

### 步驟 3: 運行測試腳本

```bash
# 運行 verify_playwright.py
cd /app
python3 scripts/verify_playwright.py

# 運行 wedopr.com 測試
python3 scripts/test_wedopr.py
```

### 步驟 4: 檢查實際掃描日誌

```bash
# 查看最近的應用日誌
tail -f /var/log/trust-wedo/app.log

# 或 Docker 日誌
docker logs -f your-container
```

**搜尋關鍵字**:
```bash
grep "PLAYWRIGHT" app.log
grep "parser_used" app.log
grep "Failed to init Playwright" app.log
```

**預期看到**:
```
[INFO] Initialized Playwright parser for https://www.wedopr.com
[PLAYWRIGHT] Starting navigation to https://www.wedopr.com/
[PLAYWRIGHT] ✓ Found 4 Schema.org script(s)
[SUCCESS] parser_used: playwright
```

**如果看到**:
```
[ERROR] Failed to init Playwright: ...
[WARN] Falling back to static parser
[INFO] parser_used: static  ← 問題!
```

**說明 Playwright 未啟動!**

---

## 🔧 緊急修復清單

### 優先級 1: 確保 Playwright 可用 (30 分鐘)

- [ ] 檢查生產環境 `playwright install chromium` 已執行
- [ ] 檢查 Dockerfile 包含系統依賴或使用官方鏡像
- [ ] 檢查 `--no-sandbox` 參數已添加
- [ ] 重新部署應用

### 優先級 2: 驗證修復 (10 分鐘)

- [ ] SSH 進入生產環境運行 `verify_playwright.py`
- [ ] 檢查應用日誌確認 Playwright 啟動
- [ ] 重新掃描 `https://trust.wedopr.com/`
- [ ] 確認 `parser_used: "playwright"` 而不是 "static"

### 優先級 3: 驗證評分 (5 分鐘)

- [ ] wedopr.com 評分 > 85 分
- [ ] Schema.org 檢測 > 28 分
- [ ] 各維度正常顯示

---

## 📊 預期結果對比

### 修復前 (當前狀態)

```yaml
URL: https://trust.wedopr.com/
評分: 20/100 (D級)
parser_used: "static"  # ← 問題根源!
維度:
  結構化: 0/30 (0%)
  可發現性: 0/20 (0%)
  信任訊號: 20/20 (100%)
  技術體質: 0/15 (0%)
  身份識別: 0/15 (0%)
```

### 修復後 (預期)

```yaml
URL: https://trust.wedopr.com/
評分: 87/100 (A級)
parser_used: "playwright"  # ← 關鍵指標!
維度:
  結構化: 28/30 (93%)    # +28
  可發現性: 19/20 (95%)  # +19
  信任訊號: 20/20 (100%) # 維持
  技術體質: 14/15 (93%)  # +14
  身份識別: 15/15 (100%) # +15
```

---

## 🎯 最終檢查清單

部署修復後,請依序確認:

### 環境檢查
```bash
# 1. Playwright 已安裝
playwright --version

# 2. Chromium 可用
ls /ms-playwright/chromium-*/chrome-linux/chrome

# 3. 權限正確
ls -la /ms-playwright/chromium-*/chrome-linux/chrome
# 應該有執行權限: -rwxr-xr-x
```

### 應用檢查
```bash
# 4. 測試腳本通過
python scripts/verify_playwright.py
python scripts/test_wedopr.py

# 5. 日誌正常
tail -100 app.log | grep PLAYWRIGHT
# 應該看到: "Initialized Playwright parser"
```

### 功能檢查
```bash
# 6. 重新掃描
curl -X POST https://your-api/scan -d '{"url":"https://trust.wedopr.com/"}'

# 7. 檢查結果
curl https://your-api/results/latest | jq '.parser_used'
# 應該返回: "playwright"
```

### 評分檢查
- [ ] wedopr.com: 85-91/100 (A級)
- [ ] trust.wedopr.com: 85-91/100 (A級)
- [ ] Schema 檢測: > 25 分
- [ ] 所有維度: > 85%

---

## 💡 關鍵洞察

### 為什麼本地正常,生產失敗?

1. **本地環境**: 
   - Playwright 已安裝 (`playwright install`)
   - 瀏覽器在 `~/.cache/ms-playwright/`
   - 有完整系統權限

2. **生產環境 (Docker)**:
   - 容器啟動時瀏覽器不存在
   - 或缺少系統依賴 (libnss3, libgbm1...)
   - 或無 `--no-sandbox` 權限不足

**解決方法**: 使用 Playwright 官方 Docker 鏡像或完整安裝依賴

---

## 📞 需要協助?

如果修復後仍有問題,請提供:

```bash
# 1. 環境信息
uname -a
python3 --version
pip show playwright
docker --version  # 如果用 Docker

# 2. Playwright 狀態
playwright install --dry-run chromium

# 3. 測試結果
python scripts/verify_playwright.py 2>&1 | tee verify.log

# 4. 應用日誌
docker logs your-container 2>&1 | grep -i playwright | tee playwright.log

# 5. 掃描結果
curl https://your-api/results/latest | jq '.' > scan-result.json
```

---

**文件版本**: v4.0-production-fix
**創建日期**: 2026-02-16
**狀態**: 緊急修復指南
**優先級**: 🔥 P0 - 關鍵生產問題
