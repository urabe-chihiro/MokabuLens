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

```bash
alembic revision --autogenerate -m "Create stock tables"
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

## サポート

問題が発生した場合は、GitHubのIssuesページで報告してください。
