# MokabuLens API

## 概要

MokabuLens APIは、企業名または企業コードから株価情報を取得するRESTful APIです。Yahoo Finance APIを使用してリアルタイムの株価データを取得し、PostgreSQLデータベースに保存・管理できます。

## プロジェクト構造

```
apps/api/
├── docs/                      # ドキュメント
│   └── STOCK_API_README.md   # API詳細ドキュメント
├── test/                      # テスト
│   ├── README.md             # テストガイド
│   ├── conftest.py           # テスト設定
│   ├── test_config.py        # テスト用設定
│   ├── test_stock_endpoints.py # APIエンドポイントテスト
│   ├── test_stock_service.py   # サービス層テスト
│   └── test_stock_models.py    # モデルテスト
├── models/                    # データモデル
├── services/                  # ビジネスロジック
├── routers/                   # APIルーター
├── alembic/                   # データベースマイグレーション
├── main.py                    # アプリケーションエントリーポイント
├── requirements.txt           # 依存関係
└── run_tests.py              # テスト実行スクリプト
```

## クイックスタート

### 1. 依存関係のインストール

```bash
cd /Users/cu/MokabuLens/apps/api
source venv/bin/activate
pip install -r requirements.txt
```

### 2. データベースマイグレーション

#### 初回セットアップ

```bash
# マイグレーションファイルの生成
alembic revision --autogenerate -m "Create stock tables"

# マイグレーションの実行
alembic upgrade head
```

#### Docker環境でのマイグレーション

```bash
# Dockerコンテナ内でマイグレーション実行
docker-compose exec api bash -c "cd /app && alembic revision --autogenerate -m 'Description'"
docker-compose exec api bash -c "cd /app && alembic upgrade head"
```

#### マイグレーション管理

```bash
# 現在のマイグレーション状態を確認
alembic current

# マイグレーション履歴を表示
alembic history

# 特定のリビジョンに戻す
alembic downgrade <revision_id>

# 最新のマイグレーションに更新
alembic upgrade head
```

### 3. APIサーバーの起動

```bash
python main.py
```

### 4. APIの確認

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 主要機能

- 🔍 **株式検索**: 企業名または証券コードで株式を検索
- 📊 **株価取得**: リアルタイムの株価データを取得
- 💾 **データ保存**: 取得したデータをデータベースに保存
- 📈 **人気株式**: 主要な日本株の一覧を取得
- 🛡️ **バリデーション**: 入力値の検証とエラーハンドリング

## APIエンドポイント

| エンドポイント | メソッド | 説明 |
|---------------|----------|------|
| `/` | GET | ルートエンドポイント |
| `/health` | GET | ヘルスチェック |
| `/api/v1/stocks/search` | GET | 株式検索 |
| `/api/v1/stocks/{symbol}/price` | GET | 株価データ取得 |
| `/api/v1/stocks/{symbol}/info` | GET | 株式基本情報取得 |
| `/api/v1/stocks/{symbol}/save` | POST | 株式データ保存 |
| `/api/v1/stocks/popular` | GET | 人気株式一覧 |

## 使用例

### 株式検索
```bash
curl "http://localhost:8000/api/v1/stocks/search?query=ソニー&limit=5"
```

### 株価データ取得
```bash
curl "http://localhost:8000/api/v1/stocks/6758/price?period=5d&interval=1d"
```

### 人気株式一覧
```bash
curl "http://localhost:8000/api/v1/stocks/popular?limit=10"
```

## テスト

### テストの実行

```bash
# すべてのテストを実行
python -m pytest test/ -v

# テスト実行スクリプトを使用
python run_tests.py
```

### テストカバレッジ

```bash
pip install pytest-cov
python -m pytest test/ --cov=. --cov-report=html
```

詳細なテストガイドは [test/README.md](test/README.md) を参照してください。

## データベーススキーマ

### テーブル構成

| テーブル名 | 説明 | 主要カラム |
|-----------|------|-----------|
| `stock_info` | 株式基本情報 | `symbol`, `company_name`, `market`, `sector` |
| `stock_prices` | 株価データ | `symbol`, `date`, `open_price`, `close_price`, `volume` |
| `users` | ユーザー情報 | `username`, `email`, `created_at` |
| `alembic_version` | マイグレーション管理 | `version_num` |

### インデックス

- `ix_stock_info_symbol`: 証券コード（ユニーク）
- `ix_stock_prices_symbol`: 証券コード
- `ix_stock_prices_date`: 日付
- `ix_users_username`: ユーザー名（ユニーク）
- `ix_users_email`: メールアドレス（ユニーク）

## 技術スタック

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **PostgreSQL**: データベース
- **Yahoo Finance API**: 株価データ取得
- **Alembic**: データベースマイグレーション
- **Pydantic**: データバリデーション
- **pytest**: テストフレームワーク

## 開発環境

### 必要な環境

- Python 3.11+
- PostgreSQL 15+
- Docker (オプション)

### 環境変数

`.env`ファイルを作成して以下の設定を行ってください：

```env
# データベース設定
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mokabu_lens
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# API設定
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
API_VERSION=v1
```

## Docker環境

### Docker Composeでの起動

```bash
# 開発環境で起動
docker-compose -f docker-compose.dev.yml up

# 本番環境で起動
docker-compose -f docker-compose.prod.yml up
```

## ドキュメント

- [API詳細ドキュメント](docs/STOCK_API_README.md)
- [テストガイド](test/README.md)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## トラブルシューティング

### マイグレーション関連

#### データベース接続エラー
```bash
# エラー: could not translate host name "postgres" to address
# 解決策: Dockerコンテナ内でマイグレーション実行
docker-compose exec api bash -c "cd /app && alembic upgrade head"
```

#### マイグレーション状態の確認
```bash
# 現在の状態を確認
docker-compose exec api bash -c "cd /app && alembic current"

# データベースのテーブル一覧を確認
docker-compose exec postgres psql -U postgres -d mokabu_lens -c "\dt"
```

#### マイグレーションのリセット
```bash
# 注意: 本番環境では実行しないでください
docker-compose exec postgres psql -U postgres -d mokabu_lens -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker-compose exec api bash -c "cd /app && alembic upgrade head"
```

### テスト関連

#### テストが失敗する場合
```bash
# 依存関係を再インストール
pip install -r requirements.txt

# テスト用データベースをリセット
rm -f test.db
python -m pytest test/ -v
```

## サポート

問題が発生した場合は、GitHubのIssuesページで報告してください。
