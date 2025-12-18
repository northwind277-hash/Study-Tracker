from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class StudyRecord(Base):
    __tablename__ = "study_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    record_date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)  # 学习分钟数
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="study_records")
    task = relationship("Task", back_populates="study_records")
