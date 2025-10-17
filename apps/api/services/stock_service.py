"""
株価データ取得サービス
外部APIから株価情報を取得し、データベースに保存・管理
"""
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

import pandas as pd
import yfinance as yf
from sqlalchemy.orm import Session

from models.stock import StockInfo, StockPrice, StockInfoResponse, StockPriceResponse

logger = logging.getLogger(__name__)


class StockService:
    """株価データ取得サービス"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def search_stocks(self, query: str, limit: int = 10) -> List[StockInfoResponse]:
        """
        企業名または証券コードで株式を検索
        
        Args:
            query: 検索クエリ（企業名または証券コード）
            limit: 検索結果の最大件数
            
        Returns:
            検索結果のリスト
        """
        try:
            # データベースから検索
            db_results = self._search_from_database(query, limit)
            
            # データベースに結果がない場合、外部APIから検索
            if not db_results:
                external_results = await self._search_from_external_api(query, limit)
                return external_results
            
            return db_results
            
        except Exception as e:
            logger.error(f"株式検索エラー: {e}")
            raise Exception(f"株式検索に失敗しました: {str(e)}")
    
    def _search_from_database(self, query: str, limit: int) -> List[StockInfoResponse]:
        """データベースから株式情報を検索"""
        results = []
        
        # 証券コードで検索（完全一致）
        if query.isdigit():
            stock = self.db.query(StockInfo).filter(
                StockInfo.symbol == query,
                StockInfo.is_active == True
            ).first()
            if stock:
                results.append(StockInfoResponse.model_validate(stock))
        
        # 企業名で検索（部分一致）
        stocks = self.db.query(StockInfo).filter(
            StockInfo.company_name.ilike(f"%{query}%"),
            StockInfo.is_active == True
        ).limit(limit).all()
        
        for stock in stocks:
            if len(results) < limit:
                results.append(StockInfoResponse.model_validate(stock))
        
        return results
    
    async def _search_from_external_api(self, query: str, limit: int) -> List[StockInfoResponse]:
        """外部APIから株式情報を検索"""
        results = []
        
        try:
            # Yahoo Financeから検索
            if query.isdigit():
                # 証券コードの場合、日本株として検索
                symbol = f"{query}.T"
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                if info and info.get('symbol'):
                    stock_info = StockInfoResponse(
                        symbol=query,
                        company_name=info.get('longName', ''),
                        company_name_en=info.get('shortName', ''),
                        market=info.get('exchange', ''),
                        sector=info.get('sector', ''),
                        industry=info.get('industry', '')
                    )
                    results.append(stock_info)
            
            # 企業名での検索は複雑なため、基本的な検索のみ実装
            # 実際の実装では、より高度な検索機能が必要
            
        except Exception as e:
            logger.error(f"外部API検索エラー: {e}")
        
        return results
    
    async def get_stock_price(self, symbol: str, period: str = "1d", interval: str = "1d") -> Dict[str, Any]:
        """
        株価データを取得
        
        Args:
            symbol: 証券コード
            period: 取得期間
            interval: データ間隔
            
        Returns:
            株価データの辞書
        """
        try:
            # 日本株の場合、.Tを追加
            yahoo_symbol = f"{symbol}.T" if symbol.isdigit() else symbol
            
            # Yahoo Financeからデータを取得
            ticker = yf.Ticker(yahoo_symbol)
            
            # 基本情報を取得
            info = ticker.info
            
            # 価格データを取得
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                raise Exception(f"株価データが見つかりません: {symbol}")
            
            # 最新の価格情報
            latest = hist.iloc[-1]
            
            # 前日比の計算
            change = 0
            change_percent = 0
            if len(hist) > 1:
                prev_close = hist.iloc[-2]['Close']
                change = latest['Close'] - prev_close
                change_percent = (change / prev_close) * 100
            
            # 価格データをリストに変換
            price_data = []
            for date, row in hist.iterrows():
                price_data.append(StockPriceResponse(
                    symbol=symbol,
                    date=date,
                    open_price=float(row['Open']) if not pd.isna(row['Open']) else None,
                    high_price=float(row['High']) if not pd.isna(row['High']) else None,
                    low_price=float(row['Low']) if not pd.isna(row['Low']) else None,
                    close_price=float(row['Close']) if not pd.isna(row['Close']) else None,
                    volume=int(row['Volume']) if not pd.isna(row['Volume']) else None,
                    adjusted_close=float(row['Close']) if not pd.isna(row['Close']) else None
                ))
            
            return {
                "symbol": symbol,
                "company_name": info.get('longName', ''),
                "current_price": float(latest['Close']) if not pd.isna(latest['Close']) else None,
                "change": change,
                "change_percent": change_percent,
                "volume": int(latest['Volume']) if not pd.isna(latest['Volume']) else None,
                "market_cap": info.get('marketCap'),
                "data": price_data
            }
            
        except Exception as e:
            logger.error(f"株価取得エラー ({symbol}): {e}")
            raise Exception(f"株価データの取得に失敗しました: {str(e)}")
    
    async def save_stock_info(self, stock_info: StockInfoResponse) -> None:
        """株式情報をデータベースに保存"""
        try:
            # 既存のレコードをチェック
            existing = self.db.query(StockInfo).filter(StockInfo.symbol == stock_info.symbol).first()
            
            if existing:
                # 更新
                existing.company_name = stock_info.company_name
                existing.company_name_en = stock_info.company_name_en
                existing.market = stock_info.market
                existing.sector = stock_info.sector
                existing.industry = stock_info.industry
                existing.updated_at = datetime.now(timezone.utc)
            else:
                # 新規作成
                new_stock = StockInfo(
                    symbol=stock_info.symbol,
                    company_name=stock_info.company_name,
                    company_name_en=stock_info.company_name_en,
                    market=stock_info.market,
                    sector=stock_info.sector,
                    industry=stock_info.industry
                )
                self.db.add(new_stock)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"株式情報保存エラー: {e}")
            raise Exception(f"株式情報の保存に失敗しました: {str(e)}")
    
    async def save_stock_price(self, symbol: str, price_data: List[StockPriceResponse]) -> None:
        """株価データをデータベースに保存"""
        try:
            if not price_data:
                return
            
            # 日付のリストを作成して一括クエリで既存レコードを取得
            dates = [price.date for price in price_data]
            existing_records = self.db.query(StockPrice).filter(
                StockPrice.symbol == symbol,
                StockPrice.date.in_(dates)
            ).all()
            
            # 既存レコードを辞書に変換（日付をキーとして）
            existing_dict = {(record.symbol, record.date): record for record in existing_records}
            
            for price in price_data:
                key = (price.symbol, price.date)
                
                if key in existing_dict:
                    # 更新
                    existing = existing_dict[key]
                    existing.open_price = price.open_price
                    existing.high_price = price.high_price
                    existing.low_price = price.low_price
                    existing.close_price = price.close_price
                    existing.volume = price.volume
                    existing.adjusted_close = price.adjusted_close
                else:
                    # 新規作成
                    new_price = StockPrice(
                        symbol=price.symbol,
                        date=price.date,
                        open_price=price.open_price,
                        high_price=price.high_price,
                        low_price=price.low_price,
                        close_price=price.close_price,
                        volume=price.volume,
                        adjusted_close=price.adjusted_close
                    )
                    self.db.add(new_price)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"株価データ保存エラー: {e}")
            raise Exception(f"株価データの保存に失敗しました: {str(e)}")


