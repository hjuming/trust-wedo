# PDF Report Generation - Technical Documentation

## 概述

Trust WEDO 的 PDF 報告生成系統已從「網頁列印」模式升級為「專用 Report Template」模式,確保輸出專業、簡約、固定版面 (1-2 頁 A4)。

## 架構設計

### 前端: PDF Report Template

**路由**: `/pdf-report/:scanId`  
**組件**: `apps/landing/src/pages/PDFReportTemplate.tsx`  
**樣式**: `apps/landing/src/styles/pdf-report.css`

**特點**:
- ✅ 獨立的報告模板,不共用一般 UI 頁面
- ✅ 強制 Light Theme (不受使用者 dark mode 影響)
- ✅ 固定 A4 版面 (210mm x 297mm)
- ✅ 只包含報告必要資訊,無 HTML 標籤或程式碼片段
- ✅ 使用 `break-inside: avoid` 防止內容被切割

**內容結構** (Page 1):
1. **Header**: Logo + 報告標題 + 客戶網址 + 日期
2. **Hero Summary**: 總分 + 等級 + 一句結論
3. **五大維度**: 簡潔條狀圖 (不使用大圖表)
4. **Top 3 Quick Wins**: 最有感的 3 條建議
5. **Trust Gap 摘要**: 最多 5 條,每條一句話
6. **Footer**: 引擎版本 + 掃描編號

### 後端: Playwright PDF Generator

**服務**: `apps/backend/app/services/report_pdf.py`  
**方法**: 使用 Playwright headless Chromium 渲染 `/pdf-report/:scanId` 並轉換為 PDF

**流程**:
1. 後端接收 PDF 下載請求 (`/api/reports/:scanId/pdf`)
2. 使用 Playwright 啟動 headless Chromium
3. 導航到 `{FRONTEND_URL}/pdf-report/:scanId`
4. 等待內容載入 (`.pdf-report` 元素)
5. 調用 `page.pdf()` 生成 PDF
6. 返回 PDF bytes 給客戶端

**配置**:
```python
pdf_bytes = await page.pdf(
    format='A4',
    print_background=True,
    margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
    prefer_css_page_size=True
)
```

## 環境變數

```bash
# Frontend URL (用於 PDF 生成)
FRONTEND_URL=https://your-frontend.com  # 生產環境
FRONTEND_URL=http://localhost:5173      # 本地開發
```

## 部署要求

### Docker

Dockerfile 已更新,包含:
1. Playwright Python 套件 + **pypdf** (用於 QA 檢測)
2. Chromium browser
3. 所有必要的系統依賴

```dockerfile
RUN pip install pypdf
RUN playwright install chromium
RUN playwright install-deps chromium
```

### 本地開發

```bash
# 安裝 Playwright & pypdf
pip install playwright pypdf

# 安裝 Chromium browser
playwright install chromium
playwright install-deps chromium
```

## 驗收標準 (Strict QA Checklist)

- [ ] **安全邊距**: 上下左右 12-14mm (防止印表機裁切)
- [ ] **頁數限制**: 系統會自動檢測頁數,若 >2 頁會記錄 `[QA FAIL]` (目標: 1 頁)
- [ ] **無 HTML tag**: 絕對禁止出現 `<footer>` / `<script>` 等原始碼
- [ ] **Light Theme**: 根節點強制 Light Mode,背景純白,文字深灰
- [ ] **無 Fallback**: 若生成失敗,直接報錯,不提供次級品

## 故障排除

### QA FAIL: PDF exceeds 2 pages

**原因**: 內容過多 (例如 Trust Gaps 或維度描述太長)
**解決**:
1. 檢查 `PDFReportTemplate.tsx` 的內容長度
2. 調整 CSS 字體大小或間距
3. 減少 Trust Gaps 顯示數量 (目前限制 5 條)

### Report Generation Failed

**原因**: Playwright 啟動失敗或 Timeout
**解決**:
1. 確保 Docker 容器記憶體足夠 (至少 1GB)
2. 檢查 `FRONTEND_URL` 是否可訪問
3. 查看後端日誌中的具體錯誤訊息


## 未來優化

1. **Page 2 支援**: 當建議項目過多時,自動分頁
2. **多語言支援**: i18n for PDF templates
3. **自定義品牌**: 允許客戶上傳 logo
4. **PDF 快取**: 相同 scanId 的 PDF 快取 24 小時

## 相關文件

- Frontend Template: `apps/landing/src/pages/PDFReportTemplate.tsx`
- PDF CSS: `apps/landing/src/styles/pdf-report.css`
- Backend Service: `apps/backend/app/services/report_pdf.py`
- Legacy Service: `apps/backend/app/services/report_pdf_legacy.py`
