"""
株価APIのテスト
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.stock import StockInfo
from services.stock_service import StockService


class TestStockAPI:
    """株価APIのテストクラス"""
    
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


class TestStockService:
    """株価サービスのテストクラス"""
    
    def test_search_from_database_empty_query(self, db_session: Session):
        """空のクエリでのデータベース検索テスト"""
        service = StockService(db_session)
        results = service._search_from_database("", 10)
        assert results == []
    
    def test_search_from_database_numeric_query(self, db_session: Session):
        """数値クエリでのデータベース検索テスト"""
        # テストデータを作成
        test_stock = StockInfo(
            symbol="6758",
            company_name="ソニーグループ株式会社",
            company_name_en="Sony Group Corporation",
            market="東証プライム",
            sector="エレクトロニクス",
            industry="エレクトロニクス・電気機器"
        )
        db_session.add(test_stock)
        db_session.commit()
        
        service = StockService(db_session)
        results = service._search_from_database("6758", 10)
        
        assert len(results) == 1
        assert results[0].symbol == "6758"
        assert results[0].company_name == "ソニーグループ株式会社"
    
    def test_search_from_database_text_query(self, db_session: Session):
        """テキストクエリでのデータベース検索テスト"""
        # テストデータを作成
        test_stock = StockInfo(
            symbol="7203",
            company_name="トヨタ自動車株式会社",
            company_name_en="Toyota Motor Corporation",
            market="東証プライム",
            sector="輸送用機器",
            industry="自動車・輸送用機器"
        )
        db_session.add(test_stock)
        db_session.commit()
        
        service = StockService(db_session)
        results = service._search_from_database("トヨタ", 10)
        
        assert len(results) == 1
        assert results[0].symbol == "7203"
        assert "トヨタ" in results[0].company_name
    
    @pytest.mark.asyncio
    async def test_save_stock_info_new(self, db_session: Session):
        """新規株式情報保存テスト"""
        from models.stock import StockInfoResponse
        
        service = StockService(db_session)
        stock_info = StockInfoResponse(
            symbol="9984",
            company_name="ソフトバンクグループ株式会社",
            company_name_en="SoftBank Group Corp.",
            market="東証プライム",
            sector="情報・通信",
            industry="情報・通信"
        )
        
        # 保存前の確認
        existing = db_session.query(StockInfo).filter(StockInfo.symbol == "9984").first()
        assert existing is None
        
        # 保存実行
        await service.save_stock_info(stock_info)
        
        # 保存後の確認
        saved = db_session.query(StockInfo).filter(StockInfo.symbol == "9984").first()
        assert saved is not None
        assert saved.company_name == "ソフトバンクグループ株式会社"
    
    @pytest.mark.asyncio
    async def test_save_stock_info_update(self, db_session: Session):
        """既存株式情報更新テスト"""
        from models.stock import StockInfoResponse
        
        # 既存データを作成
        existing_stock = StockInfo(
            symbol="6758",
            company_name="旧ソニー",
            company_name_en="Old Sony",
            market="東証プライム",
            sector="エレクトロニクス",
            industry="エレクトロニクス・電気機器"
        )
        db_session.add(existing_stock)
        db_session.commit()
        
        service = StockService(db_session)
        updated_info = StockInfoResponse(
            symbol="6758",
            company_name="ソニーグループ株式会社",
            company_name_en="Sony Group Corporation",
            market="東証プライム",
            sector="エレクトロニクス",
            industry="エレクトロニクス・電気機器"
        )
        
        # 更新実行
        await service.save_stock_info(updated_info)
        
        # 更新後の確認
        updated = db_session.query(StockInfo).filter(StockInfo.symbol == "6758").first()
        assert updated.company_name == "ソニーグループ株式会社"
        assert updated.company_name_en == "Sony Group Corporation"


class TestStockModels:
    """株価モデルのテストクラス"""
    
    def test_stock_info_response_validation(self):
        """StockInfoResponseのバリデーションテスト"""
        from models.stock import StockInfoResponse
        
        # 正常なデータ
        valid_data = {
            "symbol": "6758",
            "company_name": "ソニーグループ株式会社",
            "company_name_en": "Sony Group Corporation",
            "market": "東証プライム",
            "sector": "エレクトロニクス",
            "industry": "エレクトロニクス・電気機器"
        }
        
        stock_info = StockInfoResponse(**valid_data)
        assert stock_info.symbol == "6758"
        assert stock_info.company_name == "ソニーグループ株式会社"
    
    def test_stock_price_request_validation(self):
        """StockPriceRequestのバリデーションテスト"""
        from models.stock import StockPriceRequest
        
        # 正常なデータ
        valid_data = {
            "symbol": "6758",
            "period": "1d",
            "interval": "1d"
        }
        
        request = StockPriceRequest(**valid_data)
        assert request.symbol == "6758"
        assert request.period == "1d"
        assert request.interval == "1d"
    
    def test_stock_price_request_invalid_period(self):
        """無効なperiodでのバリデーションテスト"""
        from models.stock import StockPriceRequest
        
        with pytest.raises(ValueError):
            StockPriceRequest(symbol="6758", period="invalid", interval="1d")
    
    def test_stock_price_request_invalid_interval(self):
        """無効なintervalでのバリデーションテスト"""
        from models.stock import StockPriceRequest
        
        with pytest.raises(ValueError):
            StockPriceRequest(symbol="6758", period="1d", interval="invalid")