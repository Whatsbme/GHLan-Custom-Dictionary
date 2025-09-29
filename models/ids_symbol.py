"""
IDS符号模型
IDS Symbol Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from datetime import datetime

from .base import Base


class IdsSymbol(Base):
    """IDS符号模型"""
    
    __tablename__ = 'ids_symbols'
    
    # 基本信息
    id = Column(Integer, primary_key=True, autoincrement=True, comment='符号ID')
    name = Column(String(200), nullable=False, comment='符号名称')
    description = Column(Text, comment='符号描述')
    symbols_data = Column(Text, nullable=False, comment='符号数据(JSON)')
    canvas_size = Column(String(50), nullable=False, comment='画布大小(JSON)')
    
    # 时间信息
    created_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symbols_data': self.symbols_data,
            'canvas_size': self.canvas_size,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<IdsSymbol(id={self.id}, name='{self.name}')>"

