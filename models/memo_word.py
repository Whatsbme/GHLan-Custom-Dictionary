"""
备忘词条模型
Memo Word Model
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from datetime import datetime

from .base import Base


class MemoWord(Base):
    """备忘词条模型"""
    
    __tablename__ = 'memo_words'
    
    # 基本信息
    id = Column(Integer, primary_key=True, autoincrement=True, comment='备忘ID')
    content = Column(Text, nullable=False, comment='备忘内容')
    priority = Column(Integer, default=3, comment='优先级 (1-5)')
    is_completed = Column(Boolean, default=False, comment='是否已完成')
    
    # 时间信息
    created_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    completed_at = Column(DateTime, comment='完成时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'priority': self.priority,
            'is_completed': self.is_completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at
        }
    
    def __repr__(self):
        return f"<MemoWord(id={self.id}, content='{self.content[:20]}...', completed={self.is_completed})>"