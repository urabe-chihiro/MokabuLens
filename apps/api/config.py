"""
アプリケーション設定管理
モダンな設定管理パターンを実装
"""
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """データベース設定"""
    host: str = Field(default="postgres", description="データベースホスト")
    port: int = Field(default=5432, description="データベースポート")
    name: str = Field(default="mokabu_lens", description="データベース名")
    user: str = Field(default="postgres", description="データベースユーザー")
    password: str = Field(default="postgres", description="データベースパスワード")
    
    @property
    def url(self) -> str:
        """データベースURLを生成"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False


class APIConfig(BaseSettings):
    """API設定"""
    host: str = Field(default="0.0.0.0", description="APIサーバーホスト")
    port: int = Field(default=8000, description="APIサーバーポート")
    debug: bool = Field(default=False, description="デバッグモード")
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"], 
        description="CORS許可オリジン"
    )
    secret_key: str = Field(default="dev_secret_key", description="シークレットキー")
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """CORSオリジンをパース"""
        if isinstance(v, str):
            # カンマ区切りで分割し、空白を削除
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins
        return v
    
    class Config:
        env_prefix = "API_"
        case_sensitive = False


class SecurityConfig(BaseSettings):
    """セキュリティ設定"""
    jwt_secret: str = Field(default="dev_jwt_secret", description="JWT署名キー")
    jwt_algorithm: str = Field(default="HS256", description="JWTアルゴリズム")
    jwt_expire_minutes: int = Field(default=30, description="JWT有効期限（分）")
    encryption_key: str = Field(default="dev_encryption_key", description="暗号化キー")
    
    class Config:
        env_prefix = "SECURITY_"
        case_sensitive = False


class LoggingConfig(BaseSettings):
    """ログ設定"""
    level: str = Field(default="INFO", description="ログレベル")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="ログフォーマット"
    )
    
    @field_validator('level')
    @classmethod
    def validate_log_level(cls, v):
        """ログレベルの検証"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v.upper()
    
    class Config:
        env_prefix = "LOG_"
        case_sensitive = False


class AppConfig(BaseSettings):
    """アプリケーション全体の設定"""
    environment: str = Field(default="development", description="実行環境")
    version: str = Field(default="1.0.0", description="アプリケーションバージョン")
    
    # サブ設定
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        """環境の検証"""
        valid_envs = ["development", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"Invalid environment: {v}. Must be one of {valid_envs}")
        return v.lower()
    
    @property
    def is_development(self) -> bool:
        """開発環境かどうか"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """本番環境かどうか"""
        return self.environment == "production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> AppConfig:
    """
    設定を取得（シングルトンパターン）
    キャッシュされるため、複数回呼び出されても同じインスタンスを返す
    """
    return AppConfig()


# グローバル設定インスタンス
settings = get_settings()
