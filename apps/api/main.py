"""
MokabuLens API
モダンな設定管理とセキュリティを実装
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config import settings
from routers import stock

# 環境変数を読み込み
load_dotenv()

# FastAPIアプリケーションを作成
app = FastAPI(
    title="MokabuLens API",
    description="MokabuLens Backend API",
    version=settings.version,
    debug=settings.api.debug,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加
app.include_router(stock.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "MokabuLens API is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.version,
        "environment": settings.environment,
        "database_host": settings.database.host
    }

@app.get("/config")
async def get_config():
    """設定情報を取得（開発環境のみ）"""
    if settings.is_development:
        return {
            "environment": settings.environment,
            "api": {
                "host": settings.api.host,
                "port": settings.api.port,
                "debug": settings.api.debug
            },
            "database": {
                "host": settings.database.host,
                "port": settings.database.port,
                "name": settings.database.name,
                "user": settings.database.user
            }
        }
    return {"message": "Configuration not available in production"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.api.host, 
        port=settings.api.port,
        reload=settings.is_development
    )
