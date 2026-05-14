# Trust WEDO

**Answer Trust Infrastructure for Generative Systems.**

> Trust WEDO 是一個針對生成式 AI 系統設計的信任基礎設施。
> 它將網頁內容轉換為可驗證 (Verifiable)、可拒絕 (Rejectable)、且 AI 可用 (AI-usable) 的「答案物件 (Answer Objects)」。

![Status](https://img.shields.io/badge/Status-Production_Stable-success)
![Frontend](https://img.shields.io/badge/Frontend-React_19-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Database](https://img.shields.io/badge/Database-Supabase-emerald)

---

## 🚀 核心功能 (Core Features)

Trust WEDO 透過一系列標準化流程，建立內容的信任度：

1.  **🔍 深度掃描 (Deep Scan)**
    -   解析網頁結構、Schema.org 標記、Metadata 與作者資訊。
    -   識別網站類型 (電商、部落格、企業、個人)。

2.  **📊 信任評分 (Trust Scoring)**
    -   基於 **EC (Entity Confidence)** 演算法計算可信度。
    -   分析一致性 (Consistency)、權威性 (Authority)、與社群信號 (Social Signals)。

3.  **🧱 AFB 建構 (Answer-First Block)**
    -   生成標準化的 JSON 結構，專供 AI (LLMs) 引用與檢索。
    -   阻擋低品質或惡意內容進入 AI 上下文。

4.  **🕸️ 實體圖譜 (Trust Graph)**
    -   建立跨網頁的實體關係鏈，偵測孤立資訊與單一來源風險。

---

## 🛠️ 技術架構 (Tech Stack)

是一個現代化的 **Full-stack Monorepo**：

| Layer | Technology | Description |
|-------|------------|-------------|
| **Frontend** | React 19, Vite, TailwindCSS | 位於 `apps/landing`。提供直覺的分析 Dashboard 與報告介面。 |
| **Backend** | FastAPI, Python 3.10+ | 位於 `apps/backend`。內嵌核心引擎，處理高併發分析請求。 |
| **Core** | Trust WEDO Library | 位於 `src/trust_wedo`。核心演算法與 CLI 工具。 |
| **Database** | Supabase (PostgreSQL) | 儲存使用者資料、掃描任務與 RLS 權限控管。 |
| **Infra** | Cloudflare Pages | `apps/landing` 由 Cloudflare Pages 從 `main` 分支自動部署。 |

---

## 🚦 開發指南 (Development)

### 前置需求
- Node.js 18+
- Python 3.10+
- Supabase Account

### 啟動本地開發環境

1.  **安裝依賴**
    ```bash
    # Backend
    cd apps/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Frontend
    cd ../../apps/landing
    npm install
    ```

2.  **設定環境變數**
    複製 `.env.example` 並填入 Supabase 設定。

3.  **啟動服務**
    ```bash
    # Backend (Port 8000)
    cd apps/backend
    uvicorn app.main:app --reload

    # Frontend (Port 5173)
    cd apps/landing
    npm run dev
    ```

---

## 📚 文件索引 (Documentation)

- **[DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md)**: 開發進度與未來路線圖 (Roadmap)。
- **[DEVELOPMENT_BLUEPRINT.md](DEVELOPMENT_BLUEPRINT.md)**: 詳細工程架構與設計藍圖。
- **[CLI.md](CLI.md)**: 核心 CLI 指令規格說明。
- **[ISSUES.md](ISSUES.md)**: 已知問題與任務追蹤。

### 最新優化計劃 (2026-02-11)
- **評分引擎重構**: 修復 Apple.com 評分錯誤問題 (詳見 [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md#phase-5))

---

## License

MIT © Trust WEDO Team
