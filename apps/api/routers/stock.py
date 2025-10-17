"""
株価情報APIルーター
株式検索と価格データ取得のエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db
from services.stock_service import StockService
from models.stock import (
    StockInfo, StockSearchRequest, StockSearchResponse, StockPriceRequest, 
    StockPriceDataResponse, StockInfoResponse, ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/search", response_model=StockSearchResponse)
async def search_stocks(
    query: str = Query(..., description="検索クエリ（企業名または証券コード）", min_length=1),
    limit: int = Query(default=10, description="検索結果の最大件数", ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    株式を検索する
    
    企業名または証券コードで株式を検索します。
    検索結果は最大50件まで返されます。
    """
    try:
        stock_service = StockService(db)
        results = await stock_service.search_stocks(query, limit)
        
        return StockSearchResponse(
            results=results,
            total=len(results)
        )
        
    except Exception as e:
        logger.error(f"株式検索エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/price", response_model=StockPriceDataResponse)
async def get_stock_price(
    symbol: str,
    period: str = Query(default="1d", description="取得期間"),
    interval: str = Query(default="1d", description="データ間隔"),
    db: Session = Depends(get_db)
):
    """
    株価データを取得する
    
    指定された証券コードの株価データを取得します。
    期間とデータ間隔を指定できます。
    """
    try:
        stock_service = StockService(db)
        price_data = await stock_service.get_stock_price(symbol, period, interval)
        
        return StockPriceDataResponse(**price_data)
        
    except Exception as e:
        logger.error(f"株価取得エラー ({symbol}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/info")
async def get_stock_info(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    株式基本情報を取得する
    
    指定された証券コードの基本情報を取得します。
    """
    try:
        stock_service = StockService(db)
        results = await stock_service.search_stocks(symbol, 1)
        
        if not results:
            raise HTTPException(status_code=404, detail=f"株式情報が見つかりません: {symbol}")
        
        return results[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"株式情報取得エラー ({symbol}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{symbol}/save")
async def save_stock_data(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    株式データをデータベースに保存する
    
    指定された証券コードの情報と価格データをデータベースに保存します。
    """
    try:
        stock_service = StockService(db)
        
        # 基本情報を取得して保存
        search_results = await stock_service.search_stocks(symbol, 1)
        if search_results:
            await stock_service.save_stock_info(search_results[0])
        
        # 価格データを取得して保存
        price_data = await stock_service.get_stock_price(symbol, "1mo", "1d")
        if price_data.get("data"):
            await stock_service.save_stock_price(symbol, price_data["data"])
        
        return {"message": f"株式データを保存しました: {symbol}"}
        
    except Exception as e:
        logger.error(f"株式データ保存エラー ({symbol}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/popular")
async def get_popular_stocks(
    limit: int = Query(default=20, description="取得件数", ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    人気株式一覧を取得する
    
    主要な日本株の一覧を返します。
    """
    try:
        # 主要な日本株の証券コード
        popular_symbols = [
            "6758",  # ソニーグループ
            "9984",  # ソフトバンクグループ
            "7203",  # トヨタ自動車
            "8306",  # 三菱UFJフィナンシャル・グループ
            "6861",  # キーエンス
            "9433",  # KDDI
            "4063",  # 信越化学工業
            "8035",  # 東京エレクトロン
            "4519",  # 中外製薬
            "6501",  # 日立製作所
            "1605",  # INPEX
        ]
        
        stock_service = StockService(db)
        
        # 証券コードをOR条件で一括検索
        db_results = db.query(StockInfo).filter(
            StockInfo.symbol.in_(popular_symbols[:limit]),
            StockInfo.is_active == True
        ).all()
        
        results = []
        for stock in db_results:
            results.append(StockInfoResponse.model_validate(stock))
        
        # データベースにない銘柄は外部APIから取得
        found_symbols = {stock.symbol for stock in db_results}
        missing_symbols = [symbol for symbol in popular_symbols[:limit] if symbol not in found_symbols]
        
        for symbol in missing_symbols:
            try:
                search_results = await stock_service.search_stocks(symbol, 1)
                if search_results:
                    results.append(search_results[0])
            except Exception as e:
                logger.warning(f"人気株式取得エラー ({symbol}): {e}")
                continue
        
        return {
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"人気株式取得エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))
