"""
基础模型类
Base Model Class
"""

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class BaseModel:
    """基础模型类，包含通用字段"""
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data):
        """从字典更新字段"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


# 创建基础类
Base = declarative_base(cls=BaseModel)
