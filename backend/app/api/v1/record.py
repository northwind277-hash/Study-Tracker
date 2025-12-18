from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crud.record import (
    get_record, get_records, get_records_by_date_range, 
    create_record, update_record, delete_record
)
from app.schemas.record import StudyRecordCreate, StudyRecordUpdate, StudyRecordResponse

router = APIRouter()


@router.post("/", response_model=StudyRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_new_record(
    record_in: StudyRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的学习记录"""
    return await create_record(db, record_in=record_in, user_id=current_user.id)


@router.get("/", response_model=List[StudyRecordResponse])
async def read_records(
    skip: int = 0,
    limit: int = 100,
    start: Optional[date] = Query(None, description="开始日期"),
    end: Optional[date] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取学习记录（可按日期范围过滤）"""
    if start and end:
        if start > end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
        return await get_records_by_date_range(db, user_id=current_user.id, start_date=start, end_date=end)
    return await get_records(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{record_id}", response_model=StudyRecordResponse)
async def read_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个学习记录"""
    record = await get_record(db, record_id=record_id, user_id=current_user.id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study record not found"
        )
    return record


@router.put("/{record_id}", response_model=StudyRecordResponse)
async def update_existing_record(
    record_id: int,
    record_in: StudyRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新学习记录"""
    record = await update_record(db, record_id=record_id, record_in=record_in, user_id=current_user.id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study record not found"
        )
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除学习记录"""
    success = await delete_record(db, record_id=record_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study record not found"
        )
    return None
