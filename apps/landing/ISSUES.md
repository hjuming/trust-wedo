# Trust WEDO Landing Page - GitHub Issues

> **9 個獨立任務，可並行開發**

---

## Phase 1: 品牌與設計基礎（Week 1）

### Issue #10: 品牌色票與 Token 🎨

**Skill:** `theme-factory`

**目標：** 建立 Trust WEDO 品牌色彩系統

**任務：**
1. 定義主色/輔色/中性色/狀態色
2. 建立 Tailwind tokens
3. 設計深色模式對應

**Deliverables:**
- `tailwind.config.js` 完整配置
- 色票文件（Markdown）
- 深色模式切換邏輯

**驗收標準:**
- [ ] 所有顏色符合 WCAG AA 對比度標準
- [ ] 深色模式可正常切換
- [ ] 文件包含使用範例

---

### Issue #11: Logo 設計 🎨

**Skill:** `canvas-design`

**目標：** 設計 Trust WEDO Logo（2 版）

**任務：**
1. 設計 Icon（1:1）
2. 設計 Wordmark（橫式）
3. 提供 SVG + PNG 格式

**Deliverables:**
- `public/logo-icon.svg`
- `public/logo-wordmark.svg`
- `public/logo-icon.png`
- `public/logo-wordmark.png`

**設計方向：**
- 版本 A：偏工程感（齒輪、代碼）
- 版本 B：偏信任與盾牌意象（盾牌、勾勾）

**驗收標準:**
- [ ] SVG 可縮放不失真
- [ ] PNG 透明底
- [ ] 兩版都符合品牌定位

---

### Issue #12: 品牌規範套用 📐

**Skill:** `brand-guidelines`

**目標：** 套用品牌到 Landing Layout

**任務：**
1. 定義 Header / Hero / Cards / CTA / Footer 版型
2. 建立字體、間距、按鈕、陰影、圓角規範
3. 建立網格系統

**Deliverables:**
- `src/styles/globals.css` 完整 Design Tokens
- 品牌規範文件（Markdown）

**驗收標準:**
- [ ] 所有元件使用統一 tokens
- [ ] 響應式網格系統
- [ ] 文件包含使用範例

---

### Issue #13: 響應式導覽列 📱

**Skill:** `frontend-design`

**目標：** 實作響應式導覽列

**任務：**
1. Desktop 版本：Logo + nav + CTA
2. Mobile 版本：漢堡選單 + CTA
3. 無障礙優化

**Deliverables:**
- `src/components/Navigation.tsx`
- `src/components/MobileMenu.tsx`

**功能需求:**
- Desktop：Logo + Docs + Pricing + Playground + GitHub + CTA
- Mobile：漢堡選單（點擊展開）
- 無障礙：aria-label, focus states, keyboard navigation

**驗收標準:**
- [ ] Desktop/Mobile 都正常運作
- [ ] 鍵盤可導覽
- [ ] Focus states 清晰

---

## Phase 2: 內容與文案（Week 2）

### Issue #14: Landing UX Review 🔍

**Skill:** `web-design-guidelines`

**目標：** 優化 Landing Page UX

**任務：**
1. 首屏訊息密度調整
2. CTA 層級優化
3. 可信訊號擺放（8/8✅、20 tests）
4. FAQ 問題順序與文案建議

**Deliverables:**
- UX Review 報告（Markdown）
- 改善建議清單

**驗收標準:**
- [ ] 報告包含具體改善建議
- [ ] 每個建議都有理由說明
- [ ] 優先級排序

---

### Issue #15: 產品文案 ✍️

**Skill:** `copywriting`

**目標：** 撰寫產品文案（中/英可選）

**任務：**
1. Hero 主標/副標（3 組備選）
2. 6 個 feature bullets（對應 CLI 指令）
3. Pricing 文案（測試期不收費的說法）
4. 3 組 CTA 按鈕文字

**Deliverables:**
- 文案文件（Markdown）
- 3 組 Hero 主標/副標備選
- 6 個 feature bullets
- Pricing 文案
- CTA 按鈕文字

**驗收標準:**
- [ ] 文案清晰易懂
- [ ] 符合品牌語氣
- [ ] 包含備選方案

---

### Issue #16: 去 AI 味文案 🎯

**Skill:** `humanizer-zh-tw`

**目標：** 優化文案，去除 AI 生成痕跡

**任務：**
1. 建立報告摘要（Executive Summary）模板
2. 定義 "不誇大、可驗證" 的語氣規範

**Deliverables:**
- 語氣規範文件（Markdown）
- 報告摘要模板

**驗收標準:**
- [ ] 語氣規範包含 DO/DON'T 範例
- [ ] 報告摘要模板可直接使用
- [ ] 文案自然不做作

---

### Issue #17: Persona 卡片 👥

**Skill:** `content-generator`

**目標：** 建立兩個人設卡片

**任務：**
1. 超級邊牧犬：一句話定位 + 擅長/不擅長 + 出場情境
2. 瘋狂程序喵：一句話定位 + 擅長/不擅長 + 出場情境
3. 用在 Landing 的短段落（不超過 80 字/張）

**Deliverables:**
- `src/components/Personas.tsx`
- Persona 資料檔（JSON 或 TS）

**驗收標準:**
- [ ] 兩個 Persona 都有完整資訊
- [ ] 文案不超過 80 字/張
- [ ] 符合角色定位

---

## Phase 3: 進階功能（可選）

### Issue #18: 流場粒子背景 ✨

**Skill:** `algorithmic-art`

**目標：** 建立 Hero 背景動畫（可選）

**任務：**
1. 建立 Canvas/WebGL 背景元件
2. 實作效能限制與開關
3. 支援 prefers-reduced-motion

**Deliverables:**
- `src/components/ParticleBackground.tsx`
- 效能優化文件

**驗收標準:**
- [ ] 不影響頁面可讀性
- [ ] 支援 prefers-reduced-motion
- [ ] 效能影響 < 5% (Lighthouse)

---

## 任務優先級

### P0（必做）
- Issue #10: 品牌色票
- Issue #11: Logo 設計
- Issue #13: 響應式導覽列
- Issue #15: 產品文案

### P1（重要）
- Issue #12: 品牌規範
- Issue #14: UX Review
- Issue #17: Persona 卡片

### P2（加分）
- Issue #16: 去 AI 味文案
- Issue #18: 流場粒子背景

---

## 認領方式

1. 在 GitHub Issues 留言「認領」
2. Fork repo 並建立分支
3. 完成後提交 PR
4. 等待 Review 與合併

---

## 參考資源

- [開發計畫](../../.gemini/antigravity/brain/dfa9363c-c85a-469e-98ff-fd575642905c/implementation_plan.md)
- [CLI 工具](../../README.md)
- [技術規範](../../docs/technical-specs/README.md)
