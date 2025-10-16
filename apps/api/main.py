from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 環境変数を読み込み
load_dotenv()

# FastAPIアプリケーションを作成
app = FastAPI(
    title="MokabuLens API",
    description="MokabuLens Backend API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.jsの開発サーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース設定
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/mokabu_lens")

@app.get("/")
async def root():
    return {"message": "MokabuLens API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database_url": DATABASE_URL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
