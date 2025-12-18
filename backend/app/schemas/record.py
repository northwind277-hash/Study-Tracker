from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


# 学习记录基础信息
class StudyRecordBase(BaseModel):
    task_id: int = Field(..., gt=0)
    record_date: date
    duration: int = Field(..., gt=0)  # 学习分钟数


# 学习记录创建请求
class StudyRecordCreate(StudyRecordBase):
    pass


# 学习记录更新请求
class StudyRecordUpdate(BaseModel):
    task_id: Optional[int] = Field(None, gt=0)
    record_date: Optional[date] = None
    duration: Optional[int] = Field(None, gt=0)


# 学习记录响应
class StudyRecordResponse(StudyRecordBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
