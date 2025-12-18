from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 项目基本配置
    PROJECT_NAME: str = "StudyTracker"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./study_tracker.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
