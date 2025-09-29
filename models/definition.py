"""
释义模型
Definition Model
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Definition(Base):
    """词条释义模型"""
    
    __tablename__ = 'definitions'
    
    # 外键关联
    word_entry_id = Column(Integer, ForeignKey('word_entries.id', ondelete='CASCADE'), nullable=False)
    
    # 释义内容
    definition_text = Column(Text, nullable=False, comment='释义内容')
    definition_order = Column(Integer, default=1, comment='释义顺序')
    
    # 关联关系
    word_entry = relationship("WordEntry", back_populates="definitions")
    
    def __repr__(self):
        return f"<Definition(id={self.id}, word_entry_id={self.word_entry_id}, text='{self.definition_text[:50]}...')>"
