from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=1)  # 1低 2中 3高
    status = Column(Integer, nullable=False, default=0)  # 0未开始 1进行中 2完成
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="tasks")
    study_records = relationship("StudyRecord", back_populates="task")
