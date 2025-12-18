from sqlalchemy.orm import declarative_base

# 创建数据库模型基类（同时支持同步和异步操作）
Base = declarative_base()

# 导入所有模型，确保它们被Base.metadata捕获
from app.models.user import User
from app.models.task import Task
from app.models.record import StudyRecord
