from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 生产环境可以设置为False
    connect_args={"check_same_thread": False}  # SQLite特定配置
)

# 创建异步会话工厂
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


async def get_db():
    """获取异步数据库会话"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
