from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.models.record import StudyRecord
from app.models.task import Task
from app.schemas.record import StudyRecordCreate, StudyRecordUpdate
from app.crud.record import create_record as crud_create_record, get_records_by_date_range


def create_record(db: Session, record_in: StudyRecordCreate, user_id: int) -> StudyRecord:
    """创建学习记录"""
    # 验证任务是否存在且属于当前用户
    task = db.query(Task).filter(Task.id == record_in.task_id, Task.user_id == user_id).first()
    if not task:
        raise ValueError("Task not found or not owned by user")
    
    return crud_create_record(db, record_in=record_in, user_id=user_id)


def get_user_records_in_date_range(db: Session, user_id: int, start_date: date, end_date: date) -> List[StudyRecord]:
    """获取用户在指定日期范围内的学习记录"""
    if start_date > end_date:
        raise ValueError("Start date must be before end date")
    
    return get_records_by_date_range(db, user_id=user_id, start_date=start_date, end_date=end_date)


def get_total_minutes_by_task(db: Session, user_id: int, task_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> int:
    """获取用户在指定任务上的总学习时长"""
    # 构建查询条件
    query = db.query(StudyRecord).filter(
        StudyRecord.user_id == user_id,
        StudyRecord.task_id == task_id
    )
    
    # 添加日期范围条件（如果提供）
    if start_date:
        query = query.filter(StudyRecord.record_date >= start_date)
    if end_date:
        query = query.filter(StudyRecord.record_date <= end_date)
    
    # 计算总学习时长
    records = query.all()
    return sum(record.duration for record in records)
