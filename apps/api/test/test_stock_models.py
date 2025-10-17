"""
株価モデルのテスト
"""
import pytest
from models.stock import (
    StockInfoResponse, StockPriceResponse, StockSearchRequest, 
    StockSearchResponse, StockPriceRequest, StockPriceDataResponse
)


class TestStockModels:
    """株価モデルのテストクラス"""
    
    def test_stock_info_response_validation(self):
        """StockInfoResponseのバリデーションテスト"""
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
    
    def test_stock_price_response_validation(self):
        """StockPriceResponseのバリデーションテスト"""
        from datetime import datetime
        
        valid_data = {
            "symbol": "6758",
            "date": datetime.now(),
            "open_price": 100.0,
            "high_price": 105.0,
            "low_price": 95.0,
            "close_price": 102.0,
            "volume": 1000000,
            "adjusted_close": 102.0
        }
        
        price_response = StockPriceResponse(**valid_data)
        assert price_response.symbol == "6758"
        assert price_response.close_price == 102.0
    
    def test_stock_search_request_validation(self):
        """StockSearchRequestのバリデーションテスト"""
        # 正常なデータ
        valid_data = {
            "query": "ソニー",
            "limit": 10
        }
        
        request = StockSearchRequest(**valid_data)
        assert request.query == "ソニー"
        assert request.limit == 10
    
    def test_stock_search_request_invalid_query(self):
        """無効なクエリでのバリデーションテスト"""
        with pytest.raises(ValueError):
            StockSearchRequest(query="", limit=10)
    
    def test_stock_search_request_invalid_limit(self):
        """無効なlimitでのバリデーションテスト"""
        with pytest.raises(ValueError):
            StockSearchRequest(query="ソニー", limit=0)
        
        with pytest.raises(ValueError):
            StockSearchRequest(query="ソニー", limit=100)
    
    def test_stock_price_request_validation(self):
        """StockPriceRequestのバリデーションテスト"""
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
        with pytest.raises(ValueError):
            StockPriceRequest(symbol="6758", period="invalid", interval="1d")
    
    def test_stock_price_request_invalid_interval(self):
        """無効なintervalでのバリデーションテスト"""
        with pytest.raises(ValueError):
            StockPriceRequest(symbol="6758", period="1d", interval="invalid")
    
    def test_stock_price_request_invalid_symbol(self):
        """無効なsymbolでのバリデーションテスト"""
        with pytest.raises(ValueError):
            StockPriceRequest(symbol="", period="1d", interval="1d")
    
    def test_stock_search_response_validation(self):
        """StockSearchResponseのバリデーションテスト"""
        stock_info = StockInfoResponse(
            symbol="6758",
            company_name="ソニーグループ株式会社"
        )
        
        response = StockSearchResponse(
            results=[stock_info],
            total=1
        )
        
        assert len(response.results) == 1
        assert response.total == 1
        assert response.results[0].symbol == "6758"
    
    def test_stock_price_data_response_validation(self):
        """StockPriceDataResponseのバリデーションテスト"""
        from datetime import datetime
        
        price_data = StockPriceResponse(
            symbol="6758",
            date=datetime.now(),
            close_price=102.0
        )
        
        response = StockPriceDataResponse(
            symbol="6758",
            company_name="ソニーグループ株式会社",
            current_price=102.0,
            change=2.0,
            change_percent=2.0,
            volume=1000000,
            market_cap=1000000000,
            data=[price_data]
        )
        
        assert response.symbol == "6758"
        assert response.current_price == 102.0
        assert len(response.data) == 1
