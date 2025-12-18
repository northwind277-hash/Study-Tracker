from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date

from app.models.record import StudyRecord
from app.schemas.record import StudyRecordCreate, StudyRecordUpdate


async def get_record(db: AsyncSession, record_id: int, user_id: int) -> Optional[StudyRecord]:
    """获取单个学习记录（检查用户权限）"""
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.id == record_id, 
            StudyRecord.user_id == user_id
        )
    )
    return result.scalars().first()


async def get_records(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[StudyRecord]:
    """获取用户的所有学习记录"""
    result = await db.execute(
        select(StudyRecord).where(StudyRecord.user_id == user_id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_records_by_date_range(db: AsyncSession, user_id: int, start_date: date, end_date: date) -> List[StudyRecord]:
    """获取指定日期范围内的学习记录"""
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == user_id,
            StudyRecord.record_date >= start_date,
            StudyRecord.record_date <= end_date
        )
    )
    return result.scalars().all()


async def create_record(db: AsyncSession, record_in: StudyRecordCreate, user_id: int) -> StudyRecord:
    """创建学习记录"""
    db_record = StudyRecord(
        **record_in.model_dump(),
        user_id=user_id,
    )
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)
    return db_record


async def update_record(db: AsyncSession, record_id: int, record_in: StudyRecordUpdate, user_id: int) -> Optional[StudyRecord]:
    """更新学习记录（检查用户权限）"""
    db_record = await get_record(db, record_id, user_id)
    if not db_record:
        return None
    
    # 更新学习记录属性
    update_data = record_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)
    return db_record


async def delete_record(db: AsyncSession, record_id: int, user_id: int) -> bool:
    """删除学习记录（检查用户权限）"""
    db_record = await get_record(db, record_id, user_id)
    if not db_record:
        return False
    
    await db.delete(db_record)
    await db.commit()
    return True


async def get_daily_total(db: AsyncSession, user_id: int, target_date: date) -> int:
    """获取指定日期的总学习时长"""
    result = await db.execute(
        select(func.sum(StudyRecord.duration)).where(
            StudyRecord.user_id == user_id,
            StudyRecord.record_date == target_date
        )
    )
    return result.scalar() or 0
