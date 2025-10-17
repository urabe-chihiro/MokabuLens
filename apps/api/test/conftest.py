"""
pytest設定ファイル
テストの共通設定とフィクスチャを定義
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from test_config import TestingSessionLocal, engine

# テスト用データベースの作成
Base.metadata.create_all(bind=engine)

def override_get_db():
    """テスト用データベースセッションをオーバーライド"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# 依存関係をオーバーライド
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """テストクライアント"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def db_session():
    """テスト用データベースセッション"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def clean_db(db_session):
    """各テスト後にデータベースをクリーンアップ"""
    yield
    # テスト後にテーブルをクリア
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
