# 使用 Python 3.10 Slim 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統相依套件 (編譯某些 Python 套件可能需要)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt (已移至根目錄以簡化)
COPY requirements.txt /app/requirements.txt

# 安裝相依套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案代碼 (包含 src/ 和 apps/)
COPY . /app

# 安裝根目錄專案 (trust_wedo 核心庫)
RUN pip install .

# 設定環境變數
ENV PYTHONPATH=/app
ENV PORT=8080

# 暴露端口
EXPOSE 8080

# 啟動指令
CMD ["sh", "-c", "python -m uvicorn apps.backend.app.main:app --host 0.0.0.0 --port $PORT"]
