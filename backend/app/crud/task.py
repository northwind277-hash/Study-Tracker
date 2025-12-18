from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """获取单个任务（检查用户权限）"""
    result = await db.execute(
        select(Task).where(
            Task.id == task_id, 
            Task.user_id == user_id
        )
    )
    return result.scalars().first()


async def get_tasks(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    """获取用户的所有任务"""
    result = await db.execute(
        select(Task).where(
            Task.user_id == user_id
        ).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_task(db: AsyncSession, task_in: TaskCreate, user_id: int) -> Task:
    """创建任务"""
    db_task = Task(
        **task_in.model_dump(),
        user_id=user_id,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: int, task_in: TaskUpdate, user_id: int) -> Optional[Task]:
    """更新任务（检查用户权限）"""
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    # 更新任务属性
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
    """删除任务（检查用户权限）"""
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        return False
    
    await db.delete(db_task)
    await db.commit()
    return True
