# Trust WEDO Landing Page

> **目標：** 將 CLI 工具轉化為「可被看懂、可被試用、可被升級」的產品入口

---

## 快速開始

### 本地開發

```bash
# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev

# 開啟瀏覽器
# http://localhost:5173
```

### 建置

```bash
# 建置生產版本
npm run build

# 預覽建置結果
npm run preview
```

---

## 技術棧

- **框架：** Vite + React 18 + TypeScript
- **樣式：** Tailwind CSS
- **路由：** React Router v6
- **部署：** Cloudflare Pages

---

## 專案結構

```
apps/landing/
├── src/
│   ├── components/          # React 元件
│   │   ├── Hero.tsx
│   │   ├── ProblemSolution.tsx
│   │   ├── HowItWorks.tsx
│   │   ├── Demo.tsx
│   │   ├── TrustSignals.tsx
│   │   ├── Personas.tsx
│   │   ├── FAQ.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   ├── pages/               # 頁面
│   │   ├── Home.tsx
│   │   ├── Pricing.tsx
│   │   ├── Docs.tsx
│   │   └── Playground.tsx
│   ├── styles/              # 樣式
│   │   └── globals.css
│   ├── App.tsx
│   └── main.tsx
├── public/                  # 靜態資源
│   ├── demo.gif
│   ├── logo.svg
│   └── _redirects
├── index.html
├── vite.config.ts
├── tailwind.config.js
├── package.json
└── README.md
```

---

## Cloudflare Pages 部署

### Build 設定

```
Framework preset: Vite
Root directory: apps/landing
Build command: npm install && npm run build
Build output directory: dist
```

### 環境變數

```
NODE_VERSION=18
```

### 自訂網域

```
trust.wedopr.com → trust-wedo.pages.dev
```

---

## 開發指南

### 新增頁面

1. 在 `src/pages/` 建立新檔案
2. 在 `App.tsx` 新增路由
3. 在 `Navigation.tsx` 新增連結

### 新增元件

1. 在 `src/components/` 建立新檔案
2. 使用 Tailwind CSS 樣式
3. 確保響應式設計（mobile-first）

### 樣式規範

- 使用 Tailwind utility classes
- 遵循品牌色票（見 `tailwind.config.js`）
- 確保無障礙（aria labels, focus states）

---

## 驗收標準

### Lighthouse 分數

- Performance ≥ 85
- SEO ≥ 90
- Accessibility ≥ 90
- Best Practices ≥ 90

### 功能檢查

- [ ] 所有 CTA 可點擊
- [ ] Mobile 導覽列正常
- [ ] FAQ 可展開/收合
- [ ] Footer 顯示版本號

---

## 相關連結

- [開發計畫](../../.gemini/antigravity/brain/dfa9363c-c85a-469e-98ff-fd575642905c/implementation_plan.md)
- [CLI 工具](../../README.md)
- [技術規範](../../docs/technical-specs/README.md)

---

**版本：** Landing v1.0（對應 CLI v0.4.0）  
**授權：** MIT
