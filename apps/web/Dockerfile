# ========================================
# Next.js Multi-Stage Dockerfile
# 本番・開発環境両対応
# ========================================

# Base stage - 共通の依存関係とセットアップ
FROM node:20-alpine AS base

# システムの依存関係をインストール
RUN apk add --no-cache libc6-compat

# pnpmをインストール
RUN npm install -g pnpm@10.17.1

# 作業ディレクトリを設定
WORKDIR /app

# ========================================
# Dependencies stage - 依存関係のインストール
# ========================================
FROM base AS deps

# package.jsonとpnpm-lock.yamlをコピー
COPY package.json pnpm-lock.yaml ./

# 依存関係をインストール（本番用）
RUN pnpm install --no-frozen-lockfile --prod

# ========================================
# Development stage - 開発環境
# ========================================
FROM base AS development

# 開発用の依存関係をインストール
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --no-frozen-lockfile

# ソースコードをコピー
COPY . .

# ポート3000を公開
EXPOSE 3000

# 開発サーバーを起動
CMD ["pnpm", "dev"]

# ========================================
# Builder stage - アプリケーションのビルド
# ========================================
FROM base AS builder

# 開発用の依存関係をインストール
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --no-frozen-lockfile

# ソースコードをコピー
COPY . .

# 環境変数を設定
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# アプリケーションをビルド
RUN pnpm build

# ========================================
# Production stage - 本番実行環境
# ========================================
FROM base AS production

# 環境変数を設定
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 非rootユーザーを作成
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# ビルド結果をコピー
COPY --from=builder /app/public ./public

# 自動的に出力されるファイルをコピー
RUN mkdir .next
RUN chown nextjs:nodejs .next

# ビルド結果をコピー
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 非rootユーザーに切り替え
USER nextjs

# ポート3000を公開
EXPOSE 3000

# 環境変数を設定
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# 本番サーバーを起動
CMD ["node", "server.js"]