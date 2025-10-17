"""
株価APIエンドポイントのテスト
"""
import pytest
from fastapi.testclient import TestClient


class TestStockEndpoints:
    """株価APIエンドポイントのテストクラス"""
    
    def test_root_endpoint(self, client: TestClient):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "MokabuLens API is running!"}
    
    def test_health_check(self, client: TestClient):
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data
    
    def test_stock_search_empty_query(self, client: TestClient):
        """空のクエリでの株式検索テスト"""
        response = client.get("/api/v1/stocks/search?query=")
        assert response.status_code == 422  # Validation error
    
    def test_stock_search_invalid_limit(self, client: TestClient):
        """無効なlimitでの株式検索テスト"""
        response = client.get("/api/v1/stocks/search?query=ソニー&limit=100")
        assert response.status_code == 422  # Validation error
    
    def test_stock_search_valid_query(self, client: TestClient):
        """有効なクエリでの株式検索テスト"""
        response = client.get("/api/v1/stocks/search?query=ソニー&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
    
    def test_stock_price_invalid_symbol(self, client: TestClient):
        """無効な証券コードでの株価取得テスト"""
        response = client.get("/api/v1/stocks/invalid_symbol/price")
        assert response.status_code == 500  # External API error
    
    def test_stock_price_valid_symbol(self, client: TestClient):
        """有効な証券コードでの株価取得テスト"""
        response = client.get("/api/v1/stocks/6758/price?period=1d")
        # Yahoo Finance APIの結果に依存するため、200または500のいずれか
        assert response.status_code in [200, 500]
    
    def test_stock_info_endpoint(self, client: TestClient):
        """株式基本情報取得エンドポイントのテスト"""
        response = client.get("/api/v1/stocks/6758/info")
        # データベースにない場合は500エラー
        assert response.status_code in [200, 404, 500]
    
    def test_save_stock_data_endpoint(self, client: TestClient):
        """株式データ保存エンドポイントのテスト"""
        response = client.post("/api/v1/stocks/6758/save")
        # 外部APIの結果に依存するため、200または500のいずれか
        assert response.status_code in [200, 500]
    
    def test_popular_stocks(self, client: TestClient):
        """人気株式一覧のテスト"""
        response = client.get("/api/v1/stocks/popular?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert len(data["results"]) <= 5
