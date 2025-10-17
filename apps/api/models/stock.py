"""
株価情報モデル
企業情報と株価データを管理
"""
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class StockInfo(Base):
    """株価情報テーブル"""
    __tablename__ = "stock_info"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False, comment="証券コード")
    company_name = Column(String(255), nullable=False, comment="企業名")
    company_name_en = Column(String(255), nullable=True, comment="企業名（英語）")
    market = Column(String(50), nullable=True, comment="市場名")
    sector = Column(String(100), nullable=True, comment="業種")
    industry = Column(String(100), nullable=True, comment="業界")
    is_active = Column(Boolean, default=True, comment="アクティブフラグ")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="作成日時")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment="更新日時")


class StockPrice(Base):
    """株価データテーブル"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True, comment="証券コード")
    date = Column(DateTime, nullable=False, index=True, comment="日付")
    open_price = Column(Float, nullable=True, comment="始値")
    high_price = Column(Float, nullable=True, comment="高値")
    low_price = Column(Float, nullable=True, comment="安値")
    close_price = Column(Float, nullable=True, comment="終値")
    volume = Column(Integer, nullable=True, comment="出来高")
    adjusted_close = Column(Float, nullable=True, comment="調整後終値")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="作成日時")


# Pydanticモデル（APIレスポンス用）
class StockInfoResponse(BaseModel):
    """株価情報レスポンス"""
    symbol: str = Field(..., description="証券コード")
    company_name: str = Field(..., description="企業名")
    company_name_en: Optional[str] = Field(None, description="企業名（英語）")
    market: Optional[str] = Field(None, description="市場名")
    sector: Optional[str] = Field(None, description="業種")
    industry: Optional[str] = Field(None, description="業界")
    
    model_config = ConfigDict(from_attributes=True)


class StockPriceResponse(BaseModel):
    """株価データレスポンス"""
    symbol: str = Field(..., description="証券コード")
    date: datetime = Field(..., description="日付")
    open_price: Optional[float] = Field(None, description="始値")
    high_price: Optional[float] = Field(None, description="高値")
    low_price: Optional[float] = Field(None, description="安値")
    close_price: Optional[float] = Field(None, description="終値")
    volume: Optional[int] = Field(None, description="出来高")
    adjusted_close: Optional[float] = Field(None, description="調整後終値")
    
    model_config = ConfigDict(from_attributes=True)


class StockSearchRequest(BaseModel):
    """株価検索リクエスト"""
    query: str = Field(..., description="検索クエリ（企業名または証券コード）", min_length=1)
    limit: int = Field(default=10, description="検索結果の最大件数", ge=1, le=50)


class StockSearchResponse(BaseModel):
    """株価検索レスポンス"""
    results: List[StockInfoResponse] = Field(..., description="検索結果")
    total: int = Field(..., description="総件数")


class StockPriceRequest(BaseModel):
    """株価取得リクエスト"""
    symbol: str = Field(..., description="証券コード", min_length=1)
    period: str = Field(default="1d", description="取得期間")
    interval: str = Field(default="1d", description="データ間隔")
    
    @field_validator('period')
    @classmethod
    def validate_period(cls, v):
        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if v not in valid_periods:
            raise ValueError(f"Invalid period: {v}. Must be one of {valid_periods}")
        return v
    
    @field_validator('interval')
    @classmethod
    def validate_interval(cls, v):
        valid_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
        if v not in valid_intervals:
            raise ValueError(f"Invalid interval: {v}. Must be one of {valid_intervals}")
        return v


class StockPriceDataResponse(BaseModel):
    """株価データ取得レスポンス"""
    symbol: str = Field(..., description="証券コード")
    company_name: Optional[str] = Field(None, description="企業名")
    current_price: Optional[float] = Field(None, description="現在価格")
    change: Optional[float] = Field(None, description="前日比")
    change_percent: Optional[float] = Field(None, description="前日比（%）")
    volume: Optional[int] = Field(None, description="出来高")
    market_cap: Optional[float] = Field(None, description="時価総額")
    data: List[StockPriceResponse] = Field(..., description="価格データ")


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    error: str = Field(..., description="エラーメッセージ")
    detail: Optional[str] = Field(None, description="エラー詳細")
    code: Optional[str] = Field(None, description="エラーコード")
