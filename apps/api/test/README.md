# テストガイド

## 概要

このプロジェクトには包括的なテストスイートが含まれており、APIエンドポイント、サービス層、モデルの各層をテストしています。

## テスト構造

```
apps/api/test/
├── conftest.py              # テスト共通設定とフィクスチャ
├── test_config.py           # テスト用データベース設定
├── pytest.ini              # pytest設定ファイル
├── test_stock_endpoints.py # APIエンドポイントテスト
├── test_stock_service.py   # サービス層テスト
└── test_stock_models.py    # モデルバリデーションテスト
```

## テストの種類

### 1. APIエンドポイントテスト (`test_stock_endpoints.py`)

HTTPリクエスト/レスポンスのテストを行います。

**テスト内容:**
- ルートエンドポイント (`/`)
- ヘルスチェック (`/health`)
- 株式検索 (`/api/v1/stocks/search`)
- 株価取得 (`/api/v1/stocks/{symbol}/price`)
- 株式基本情報取得 (`/api/v1/stocks/{symbol}/info`)
- 株式データ保存 (`/api/v1/stocks/{symbol}/save`)
- 人気株式一覧 (`/api/v1/stocks/popular`)

**実行例:**
```bash
python -m pytest test/test_stock_endpoints.py -v
```

### 2. サービス層テスト (`test_stock_service.py`)

ビジネスロジックとデータベース操作をテストします。

**テスト内容:**
- データベース検索機能
- 株式情報の保存・更新
- 株価データの取得
- 非同期メソッドの動作

**実行例:**
```bash
python -m pytest test/test_stock_service.py -v
```

### 3. モデルテスト (`test_stock_models.py`)

Pydanticモデルのバリデーションをテストします。

**テスト内容:**
- レスポンスモデルのバリデーション
- リクエストモデルのバリデーション
- エラーハンドリング
- 入力値の検証

**実行例:**
```bash
python -m pytest test/test_stock_models.py -v
```

## テスト実行方法

### 基本的な実行

#### すべてのテストを実行
```bash
cd /MokabuLens/apps/api
source venv/bin/activate
python -m pytest test/ -v
```

#### 特定のテストファイルを実行
```bash
# APIエンドポイントテストのみ
python -m pytest test/test_stock_endpoints.py -v

# サービス層テストのみ
python -m pytest test/test_stock_service.py -v

# モデルテストのみ
python -m pytest test/test_stock_models.py -v
```

#### 特定のテストクラスを実行
```bash
python -m pytest test/test_stock_endpoints.py::TestStockEndpoints -v
python -m pytest test/test_stock_service.py::TestStockService -v
```

#### 特定のテストメソッドを実行
```bash
python -m pytest test/test_stock_endpoints.py::TestStockEndpoints::test_root_endpoint -v
```

### テスト実行スクリプトを使用

```bash
# すべてのテストを実行
python run_tests.py

# 特定のテストファイルを実行
python run_tests.py test_stock_endpoints.py

# キーワードでテストを絞り込み
python run_tests.py -k "test_search"
```

### マーカーを使った実行

```bash
# APIテストのみ実行
python -m pytest test/ -m "api" -v

# サービステストのみ実行
python -m pytest test/ -m "service" -v

# モデルテストのみ実行
python -m pytest test/ -m "model" -v
```

## テストカバレッジ

### カバレッジレポートの生成

```bash
# カバレッジライブラリをインストール
pip install pytest-cov

# カバレッジレポートを生成
python -m pytest test/ --cov=. --cov-report=html

# カバレッジレポートを確認
open htmlcov/index.html
```

### カバレッジの確認

```bash
# コンソールでカバレッジを表示
python -m pytest test/ --cov=. --cov-report=term

# XMLレポートを生成
python -m pytest test/ --cov=. --cov-report=xml
```

## テストデータ

### テスト用データベース

- **データベース**: SQLite（メモリ内）
- **設定**: `test_config.py`で管理
- **クリーンアップ**: 各テスト後に自動的にデータをクリア

### テストフィクスチャ

`conftest.py`で以下のフィクスチャを提供：

- `client`: FastAPIテストクライアント
- `db_session`: テスト用データベースセッション
- `clean_db`: データベースのクリーンアップ

## テストの特徴

- ✅ **45個のテストケース** - 包括的なテストカバレッジ
- ✅ **非同期対応** - async/awaitメソッドのテスト
- ✅ **データベーステスト** - テスト用SQLiteを使用
- ✅ **モック対応** - 外部APIのモック化
- ✅ **フィクスチャ** - 再利用可能なテストデータ
- ✅ **パラメータ化テスト** - 複数の入力値でのテスト

## テストのベストプラクティス

### 1. テストの命名規則

```python
def test_機能名_条件_期待結果(self):
    """テストの説明"""
    pass

# 例
def test_search_stocks_valid_query_returns_results(self):
    """有効なクエリで株式検索が結果を返すことをテスト"""
    pass
```

### 2. テストの構造

```python
def test_example(self):
    # Arrange（準備）
    test_data = create_test_data()
    
    # Act（実行）
    result = function_under_test(test_data)
    
    # Assert（検証）
    assert result == expected_result
```

### 3. テストの独立性

- 各テストは独立して実行可能
- テスト間でデータを共有しない
- 外部依存をモック化

### 4. テストの再現性

- 同じ入力に対して同じ結果
- ランダム要素を排除
- 環境に依存しない

## CI/CD対応

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        cd apps/api
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd apps/api
        python -m pytest test/ -v --cov=. --cov-report=xml
```

### Docker環境でのテスト

```bash
# Dockerコンテナ内でテストを実行
docker-compose exec api python -m pytest test/ -v
```

## トラブルシューティング

### よくある問題

#### 1. インポートエラー
```bash
# 仮想環境がアクティブになっているか確認
source venv/bin/activate

# 依存関係がインストールされているか確認
pip install -r requirements.txt
```

#### 2. データベースエラー
```bash
# テスト用データベースが正しく設定されているか確認
python -c "from test.test_config import TestingSessionLocal; print('OK')"
```

#### 3. 非同期テストエラー
```bash
# pytest-asyncioがインストールされているか確認
pip install pytest-asyncio

# 非同期テストに@pytest.mark.asyncioが付いているか確認
```

### デバッグ方法

#### 詳細なログ出力
```bash
python -m pytest test/ -v -s --tb=long
```

#### 特定のテストのみ実行
```bash
python -m pytest test/test_stock_endpoints.py::TestStockEndpoints::test_root_endpoint -v -s
```

#### テストの停止
```bash
# 最初の失敗で停止
python -m pytest test/ -x

# 特定の数の失敗で停止
python -m pytest test/ --maxfail=3
```

## 新しいテストの追加

### 1. テストファイルの作成

```python
# test/test_new_feature.py
import pytest
from fastapi.testclient import TestClient

class TestNewFeature:
    def test_new_endpoint(self, client: TestClient):
        response = client.get("/api/v1/new-endpoint")
        assert response.status_code == 200
```

### 2. テストの実行

```bash
python -m pytest test/test_new_feature.py -v
```

### 3. テストの追加

既存のテストファイルに新しいテストメソッドを追加：

```python
def test_new_functionality(self):
    """新しい機能のテスト"""
    # テストの実装
    pass
```

## 参考資料

- [pytest公式ドキュメント](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
