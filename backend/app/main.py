from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 异步创建数据库表
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # 创建表（如果不存在）
        await conn.run_sync(Base.metadata.create_all)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制允许的来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入并注册路由
from app.api.v1 import auth, task, record, stats

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(task.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(record.router, prefix=f"{settings.API_V1_STR}/records", tags=["records"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["stats"])


@app.get("/")
def root():
    """根路径"""
    return {"message": "Welcome to StudyTracker API"}
