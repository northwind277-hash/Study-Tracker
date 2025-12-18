from pydantic import BaseModel
from datetime import date
from typing import List


# 每日学习统计
class DailyStats(BaseModel):
    date: date
    total_minutes: int


# 任务学习时间统计
class TaskStats(BaseModel):
    task_id: int
    task_title: str
    minutes: int
    percentage: float


# 总学习统计
class TotalStats(BaseModel):
    total_minutes: int
    total_days: int
    average_minutes_per_day: float


# 统计响应
class StatsResponse(BaseModel):
    daily: List[DailyStats]
    tasks: List[TaskStats]
    total: TotalStats
