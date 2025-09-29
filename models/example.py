"""
例句模型
Example Model
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Example(Base):
    """例句模型"""
    
    __tablename__ = 'examples'
    
    # 外键关联
    word_entry_id = Column(Integer, ForeignKey('word_entries.id', ondelete='CASCADE'), nullable=False)
    
    # 例句内容
    example_text = Column(Text, nullable=False, comment='例句内容')
    translation = Column(Text, comment='例句翻译')
    example_order = Column(Integer, default=1, comment='例句顺序')
    
    # 关联关系
    word_entry = relationship("WordEntry", back_populates="examples")
    
    def __repr__(self):
        return f"<Example(id={self.id}, word_entry_id={self.word_entry_id}, text='{self.example_text[:50]}...')>"
