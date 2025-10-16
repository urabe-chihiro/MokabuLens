# FastAPI用Dockerfile（マルチステージビルド）
FROM python:3.11-slim AS base

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 依存関係のインストール用ステージ
FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 本番用ステージ
FROM base AS production
WORKDIR /app

# 本番用の依存関係のみインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# 非rootユーザーを作成
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# ポート8000を公開
EXPOSE 8000

# ヘルスチェック用のコマンド
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# FastAPIアプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 開発用ステージ
FROM base AS development
WORKDIR /app

# 開発用の依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# ポート8000を公開
EXPOSE 8000

# 開発サーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]