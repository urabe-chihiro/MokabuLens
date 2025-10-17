# 株価取得API 実装ガイド

## 概要

企業名または企業コードから株価情報を取得するAPIを実装しました。Yahoo Finance APIを使用してリアルタイムの株価データを取得し、データベースに保存・管理できます。

## 実装した機能

### 1. 株式検索 API
- **エンドポイント**: `GET /api/v1/stocks/search`
- **機能**: 企業名または証券コードで株式を検索
- **パラメータ**:
  - `query`: 検索クエリ（企業名または証券コード）
  - `limit`: 検索結果の最大件数（デフォルト: 10、最大: 50）

### 2. 株価データ取得 API
- **エンドポイント**: `GET /api/v1/stocks/{symbol}/price`
- **機能**: 指定された証券コードの株価データを取得
- **パラメータ**:
  - `symbol`: 証券コード（必須）
  - `period`: 取得期間（1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max）
  - `interval`: データ間隔（1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo）

### 3. 株式基本情報取得 API
- **エンドポイント**: `GET /api/v1/stocks/{symbol}/info`
- **機能**: 指定された証券コードの基本情報を取得

### 4. 株式データ保存 API
- **エンドポイント**: `POST /api/v1/stocks/{symbol}/save`
- **機能**: 指定された証券コードの情報と価格データをデータベースに保存

### 5. 人気株式一覧 API
- **エンドポイント**: `GET /api/v1/stocks/popular`
- **機能**: 主要な日本株の一覧を取得
- **パラメータ**:
  - `limit`: 取得件数（デフォルト: 20、最大: 50）

## データベース構造

### StockInfo テーブル
株式の基本情報を格納
- `symbol`: 証券コード
- `company_name`: 企業名
- `company_name_en`: 企業名（英語）
- `market`: 市場名
- `sector`: 業種
- `industry`: 業界

### StockPrice テーブル
株価データを格納
- `symbol`: 証券コード
- `date`: 日付
- `open_price`: 始値
- `high_price`: 高値
- `low_price`: 安値
- `close_price`: 終値
- `volume`: 出来高
- `adjusted_close`: 調整後終値

## 使用技術

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **PostgreSQL**: データベース
- **Yahoo Finance API**: 株価データ取得
- **Alembic**: データベースマイグレーション
- **Pydantic**: データバリデーション

## セットアップ手順

### 1. 依存関係のインストール
```bash
cd /Users/cu/MokabuLens/apps/api
source venv/bin/activate
pip install -r requirements.txt
```

### 2. データベースマイグレーション
```bash
# 初回マイグレーション
alembic revision --autogenerate -m "Create stock tables"
alembic upgrade head
```

### 3. APIサーバーの起動
```bash
python main.py
```

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

### テスト構造

プロジェクトには包括的なテストスイートが含まれており、以下の構造で整理されています：

```
apps/api/test/
├── conftest.py              # テスト共通設定とフィクスチャ
├── test_config.py           # テスト用データベース設定
├── pytest.ini              # pytest設定ファイル
├── test_stock_endpoints.py # APIエンドポイントテスト
├── test_stock_service.py   # サービス層テスト
└── test_stock_models.py    # モデルバリデーションテスト
```

### テストの種類

#### 1. **APIエンドポイントテスト** (`test_stock_endpoints.py`)
- HTTPリクエスト/レスポンスのテスト
- エンドポイントの動作確認
- バリデーションエラーのテスト
- ステータスコードの検証

#### 2. **サービス層テスト** (`test_stock_service.py`)
- ビジネスロジックのテスト
- データベース操作のテスト
- 外部API連携のテスト
- 非同期メソッドのテスト

#### 3. **モデルテスト** (`test_stock_models.py`)
- Pydanticモデルのバリデーション
- データ型の検証
- エラーハンドリング
- 入力値の検証

### テスト実行方法

#### **すべてのテストを実行**
```bash
cd /Users/cu/MokabuLens/apps/api
source venv/bin/activate
python -m pytest test/ -v
```

#### **特定のテストファイルを実行**
```bash
# APIエンドポイントテストのみ
python -m pytest test/test_stock_endpoints.py -v

# サービス層テストのみ
python -m pytest test/test_stock_service.py -v

# モデルテストのみ
python -m pytest test/test_stock_models.py -v
```

#### **特定のテストクラスを実行**
```bash
python -m pytest test/test_stock_endpoints.py::TestStockEndpoints -v
python -m pytest test/test_stock_service.py::TestStockService -v
```

#### **特定のテストメソッドを実行**
```bash
python -m pytest test/test_stock_endpoints.py::TestStockEndpoints::test_root_endpoint -v
```

#### **テスト実行スクリプトを使用**
```bash
# すべてのテストを実行
python run_tests.py

# 特定のテストファイルを実行
python run_tests.py test_stock_endpoints.py

# キーワードでテストを絞り込み
python run_tests.py -k "test_search"
```

#### **マーカーを使った実行**
```bash
# APIテストのみ実行
python -m pytest test/ -m "api" -v

# サービステストのみ実行
python -m pytest test/ -m "service" -v

# モデルテストのみ実行
python -m pytest test/ -m "model" -v
```

### テストカバレッジ

#### **カバレッジレポートの生成**
```bash
# カバレッジライブラリをインストール
pip install pytest-cov

# カバレッジレポートを生成
python -m pytest test/ --cov=. --cov-report=html

# カバレッジレポートを確認
open htmlcov/index.html
```

### テストの特徴

- ✅ **45個のテストケース** - 包括的なテストカバレッジ
- ✅ **非同期対応** - async/awaitメソッドのテスト
- ✅ **データベーステスト** - テスト用SQLiteを使用
- ✅ **モック対応** - 外部APIのモック化
- ✅ **フィクスチャ** - 再利用可能なテストデータ
- ✅ **パラメータ化テスト** - 複数の入力値でのテスト

### テストデータ

テストでは以下のデータを使用します：

- **テスト用データベース**: SQLite（メモリ内）
- **テストデータ**: 各テストで動的に生成
- **クリーンアップ**: 各テスト後に自動的にデータをクリア

### CI/CD対応

テストは以下の環境で実行可能です：

- **ローカル開発環境**
- **GitHub Actions**
- **Docker環境**
- **本番環境のデプロイ前チェック**

### テストのベストプラクティス

1. **単一責任**: 各テストは1つの機能のみをテスト
2. **独立性**: テスト間で依存関係を持たない
3. **再現性**: 同じ結果が常に得られる
4. **高速実行**: テストは迅速に完了する
5. **明確な名前**: テスト名から内容が分かる

## 注意事項

1. **Yahoo Finance API**: 非公式APIのため、サービスの継続性に注意が必要
2. **レート制限**: 外部APIの呼び出し回数に制限がある場合があります
3. **データの正確性**: 取得したデータは参考情報として使用し、投資判断は自己責任で行ってください
4. **日本株**: 証券コードは4桁の数字で指定し、自動的に`.T`サフィックスが追加されます

## 今後の拡張予定

- J-Quants APIとの連携
- リアルタイムデータのWebSocket対応
- キャッシュ機能の実装
- より詳細な財務データの取得
- チャートデータの提供

## API仕様書

FastAPIの自動生成ドキュメントは以下のURLで確認できます：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`



