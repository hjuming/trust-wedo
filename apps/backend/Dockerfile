# 使用官方 Playwright 基礎鏡像
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件 (此時在 apps/backend 目錄下)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製代碼 (包含已複製進來的 trust_wedo 目錄)
COPY . .

# 設定環境變數
# 這裡 trust_wedo 就在 /app/trust_wedo
# app 就在 /app/app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

# 啟動命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
