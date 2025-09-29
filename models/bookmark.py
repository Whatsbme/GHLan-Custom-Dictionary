"""
书签模型
Bookmark Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from datetime import datetime

from .base import Base


class Bookmark(Base):
    """书签模型"""
    
    __tablename__ = 'bookmarks'
    
    # 基本信息
    id = Column(Integer, primary_key=True, autoincrement=True, comment='书签ID')
    title = Column(String(200), nullable=False, comment='书签标题')
    url = Column(String(500), nullable=False, comment='网址')
    category = Column(String(100), default='未分类', comment='分类')
    description = Column(Text, comment='描述')
    
    # 时间信息
    created_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, title='{self.title}', url='{self.url}')>"