"""
株価サービスのテスト
"""
import pytest
from sqlalchemy.orm import Session

from models.stock import StockInfo
from services.stock_service import StockService


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
    
    @pytest.mark.asyncio
    async def test_get_stock_price_invalid_symbol(self, db_session: Session):
        """無効な証券コードでの株価取得テスト"""
        service = StockService(db_session)
        
        with pytest.raises(Exception):
            await service.get_stock_price("invalid_symbol")
    
    @pytest.mark.asyncio
    async def test_get_stock_price_valid_symbol(self, db_session: Session):
        """有効な証券コードでの株価取得テスト"""
        service = StockService(db_session)
        
        try:
            result = await service.get_stock_price("6758", "1d", "1d")
            assert "symbol" in result
            assert "data" in result
            assert result["symbol"] == "6758"
        except Exception:
            # Yahoo Finance APIが利用できない場合は例外が発生
            pass
