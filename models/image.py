"""
图片模型
Image Model
"""

from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class WordImage(Base):
    """词条图片模型"""
    
    __tablename__ = 'word_images'
    
    # 外键关联
    word_entry_id = Column(Integer, ForeignKey('word_entries.id', ondelete='CASCADE'), nullable=False)
    
    # 图片数据
    image_data = Column(LargeBinary, nullable=False, comment='图片二进制数据')
    image_type = Column(String(20), default='png', comment='图片类型')
    image_size = Column(Integer, comment='图片大小(字节)')
    
    # 关联关系
    word_entry = relationship("WordEntry", back_populates="images")
    
    def __repr__(self):
        return f"<WordImage(id={self.id}, word_entry_id={self.word_entry_id}, type='{self.image_type}')>"
    
    def get_image_size_mb(self):
        """获取图片大小(MB)"""
        if self.image_size:
            return round(self.image_size / (1024 * 1024), 2)
        return 0
