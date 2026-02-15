FROM python:3.10-slim
LABEL "language"="python"
LABEL "framework"="fastapi"
LABEL "build_timestamp"="2026-02-10_1700"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    # Playwright dependencies for Chromium
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Chromium only for PDF generation)
RUN playwright install chromium
RUN playwright install-deps chromium

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
