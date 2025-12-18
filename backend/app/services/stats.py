from typing import List, Dict, Tuple
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.record import StudyRecord
from app.models.task import Task
from app.schemas.stats import DailyStats, TaskStats, TotalStats


async def get_daily_stats(db: AsyncSession, user_id: int, start_date: date, end_date: date) -> List[DailyStats]:
    """获取指定日期范围内的每日学习统计"""
    # 查询每日总学习时长
    stmt = select(
        StudyRecord.record_date,
        func.sum(StudyRecord.duration).label("total_minutes")
    ).where(
        StudyRecord.user_id == user_id,
        StudyRecord.record_date >= start_date,
        StudyRecord.record_date <= end_date
    ).group_by(StudyRecord.record_date).order_by(StudyRecord.record_date)
    
    result = await db.execute(stmt)
    daily_stats = result.all()
    
    # 将结果转换为DailyStats对象列表
    return [DailyStats(date=stat.record_date, total_minutes=stat.total_minutes) for stat in daily_stats]


async def get_task_stats(db: AsyncSession, user_id: int, start_date: date, end_date: date) -> List[TaskStats]:
    """获取指定日期范围内的任务学习时间统计"""
    # 查询各任务的总学习时长
    stmt = select(
        StudyRecord.task_id,
        Task.title.label("task_title"),
        func.sum(StudyRecord.duration).label("minutes")
    ).join(Task, StudyRecord.task_id == Task.id).where(
        StudyRecord.user_id == user_id,
        StudyRecord.record_date >= start_date,
        StudyRecord.record_date <= end_date
    ).group_by(StudyRecord.task_id, Task.title).order_by(func.sum(StudyRecord.duration).desc())
    
    result = await db.execute(stmt)
    task_stats = result.all()
    
    # 计算总学习时长
    total_minutes = sum(stat.minutes for stat in task_stats) if task_stats else 0
    
    # 将结果转换为TaskStats对象列表，并计算百分比
    result = []
    for stat in task_stats:
        percentage = (stat.minutes / total_minutes * 100) if total_minutes > 0 else 0.0
        result.append(TaskStats(
            task_id=stat.task_id,
            task_title=stat.task_title,
            minutes=stat.minutes,
            percentage=round(percentage, 2)
        ))
    
    return result


async def get_total_stats(db: AsyncSession, user_id: int, start_date: date, end_date: date) -> TotalStats:
    """获取指定日期范围内的总学习统计"""
    # 获取所有学习记录
    stmt = select(StudyRecord).where(
        StudyRecord.user_id == user_id,
        StudyRecord.record_date >= start_date,
        StudyRecord.record_date <= end_date
    )
    
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    # 计算总学习时长
    total_minutes = sum(record.duration for record in records)
    
    # 计算学习天数（去重）
    study_days = len(set(record.record_date for record in records))
    
    # 计算平均每日学习时长
    average_minutes_per_day = total_minutes / study_days if study_days > 0 else 0.0
    
    return TotalStats(
        total_minutes=total_minutes,
        total_days=study_days,
        average_minutes_per_day=round(average_minutes_per_day, 2)
    )


async def get_weekly_stats(db: AsyncSession, user_id: int, weeks: int = 4) -> Dict[str, any]:
    """获取最近几周的学习统计"""
    # 计算日期范围
    end_date = date.today()
    start_date = end_date - timedelta(weeks=weeks)
    
    return {
        "daily": await get_daily_stats(db, user_id, start_date, end_date),
        "tasks": await get_task_stats(db, user_id, start_date, end_date),
        "total": await get_total_stats(db, user_id, start_date, end_date)
    }
