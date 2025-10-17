"""
データベース接続設定
モダンな設定管理パターンを使用
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 設定からデータベースURLを取得
DATABASE_URL = settings.database.url

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションファクトリーを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスを作成
Base = declarative_base()

# データベースセッションを取得する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
