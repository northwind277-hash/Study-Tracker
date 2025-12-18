from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# 任务基础信息
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    priority: int = Field(..., ge=1, le=3)  # 1低 2中 3高
    status: Optional[int] = Field(None, ge=0, le=2)  # 0未开始 1进行中 2完成


# 任务创建请求
class TaskCreate(TaskBase):
    pass


# 任务更新请求
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=3)
    status: Optional[int] = Field(None, ge=0, le=2)


# 任务响应
class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
