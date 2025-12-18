from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date, timedelta

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.stats import get_daily_stats, get_task_stats, get_total_stats, get_weekly_stats
from app.schemas.stats import DailyStats, TaskStats, TotalStats

router = APIRouter()


@router.get("/daily", response_model=list[DailyStats])
async def read_daily_stats(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取每日学习统计"""
    # 默认查询最近30天
    if not start_date:
        end_date = end_date or date.today()
        start_date = end_date - timedelta(days=29)
    
    if not end_date:
        end_date = start_date + timedelta(days=29)
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    return await get_daily_stats(db, user_id=current_user.id, start_date=start_date, end_date=end_date)


@router.get("/task", response_model=list[TaskStats])
async def read_task_stats(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务学习时间统计"""
    # 默认查询最近30天
    if not start_date:
        end_date = end_date or date.today()
        start_date = end_date - timedelta(days=29)
    
    if not end_date:
        end_date = start_date + timedelta(days=29)
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    return await get_task_stats(db, user_id=current_user.id, start_date=start_date, end_date=end_date)


@router.get("/total", response_model=TotalStats)
async def read_total_stats(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取总学习统计"""
    # 默认查询最近30天
    if not start_date:
        end_date = end_date or date.today()
        start_date = end_date - timedelta(days=29)
    
    if not end_date:
        end_date = start_date + timedelta(days=29)
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    return await get_total_stats(db, user_id=current_user.id, start_date=start_date, end_date=end_date)


@router.get("/weekly")
async def read_weekly_stats(
    weeks: int = Query(4, ge=1, le=52, description="查询周数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取最近几周的学习统计"""
    return await get_weekly_stats(db, user_id=current_user.id, weeks=weeks)
