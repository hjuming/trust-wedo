# 使用官方 Playwright 基礎鏡像，已預裝所有瀏覽器依賴
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

LABEL "language"="python"
LABEL "framework"="fastapi"
LABEL "build_timestamp"="2026-02-16_1900"

WORKDIR /app

# 安裝基本系統依賴 (postgresql client 等)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製後端依賴並安裝
COPY apps/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個項目代碼
COPY . /app

# 設定環境變數
# /app/apps/backend -> 讓 'from app import ...' 工作
# /app/src -> 讓 'import trust_wedo' 工作
# /app -> 讓 'import apps' 工作
ENV PYTHONPATH=/app/apps/backend:/app/src:/app:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

# 直接啟動 FastAPI 應用
CMD ["python", "-m", "uvicorn", "apps.backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]

