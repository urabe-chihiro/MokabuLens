from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# データベースURLを取得
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/mokabu_lens")

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
