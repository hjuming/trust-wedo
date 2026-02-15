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

# 3. 安裝本地 trust_wedo 包 (關鍵修復：解決 ModuleNotFoundError)
# 根目錄有 pyproject.toml，這會安裝 src/trust_wedo 作為可導入包
RUN pip install --no-cache-dir -e .

# 設定環境變數
# /app/apps/backend -> 讓 'import app' 找到 /app/apps/backend/app
# /app/src -> 讓 'import trust_wedo' 找到 /app/src/trust_wedo
ENV PYTHONPATH=/app/apps/backend:/app/src:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

# 啟動命令
# 基於 PYTHONPATH，app.main:app 指向 /app/apps/backend/app/main.py 的 app 實例
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
