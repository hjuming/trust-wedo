# 使用官方 Playwright 基礎鏡像，已預裝所有瀏覽器依賴
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

LABEL "language"="python"
LABEL "framework"="fastapi"
LABEL "build_timestamp"="2026-02-16_2100"

WORKDIR /app

# 安裝基本系統依賴 (postgresql client 等)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 1. 複製後端依賴並安裝
COPY apps/backend/requirements.txt /app/apps/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/apps/backend/requirements.txt

# 2. 複製整個項目代碼
COPY . /app

# 3. 確保 trust_wedo 被正確安裝 (移除 symlink 依賴，直接安裝核心庫)
# 這樣不論 PYTHONPATH 如何，trust_wedo 都會在 site-packages 中
RUN pip install --no-cache-dir .

# 設定環境變數
# /app/apps/backend -> 讓 'import app' 找到 FastAPI 應用
# /app/src -> 雙重保證
ENV PYTHONPATH=/app/apps/backend:/app/src:/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

# 啟動命令
# 確保從 apps/backend 目錄運行或正確指定路徑
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]


