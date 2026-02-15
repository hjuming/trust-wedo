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
1. Playwright Python 套件
2. Chromium browser
3. 所有必要的系統依賴 (libnss3, libgbm1, etc.)

```dockerfile
RUN playwright install chromium
RUN playwright install-deps chromium
```

### 本地開發

```bash
# 安裝 Playwright
pip install playwright

# 安裝 Chromium browser
playwright install chromium
playwright install-deps chromium
```

## 驗收標準 (QA Checklist)

- [ ] PDF 永遠只有 1-2 頁 (超過視為 fail)
- [ ] 不會出現任何 HTML tag / code block (例如 `<footer>`, `<meta>`, `<script>`)
- [ ] 同一份 scanId 產出的 PDF:不同裝置/不同 dark mode 狀態,版面一致
- [ ] 內容只保留「總覽 + 行動建議 + 必要掃描資訊」,不輸出整頁網頁
- [ ] 背景永遠白色,文字永遠深色 (不受 dark mode 影響)
- [ ] 檔名格式: `Trust-WEDO-{domain}-{date}.pdf`

## 故障排除

### PDF 生成失敗

**症狀**: `RuntimeError: Playwright is not installed`

**解決**:
```bash
pip install playwright
playwright install chromium
```

### PDF 內容空白

**症狀**: PDF 生成成功但內容為空

**可能原因**:
1. Frontend URL 配置錯誤
2. 網路連線問題 (headless browser 無法訪問 frontend)
3. 認證問題 (PDF template route 需要 auth)

**解決**:
- 檢查 `FRONTEND_URL` 環境變數
- 確保 `/pdf-report/:scanId` 路由可公開訪問 (或使用 service token)

### Fallback 機制

如果 Playwright 失敗,系統會自動 fallback 到舊的 FPDF 方法:

```python
except Exception as e:
    logger.error(f"Failed to generate PDF with Playwright: {e}")
    from app.services.report_pdf_legacy import generate_report_pdf as legacy_generate
    return legacy_generate(report_data, dimensions)
```

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
