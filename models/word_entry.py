"""
词条模型
Word Entry Model
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class WordEntry(Base):
    """词条主表模型"""
    
    __tablename__ = 'word_entries'
    
    # 基本信息
    word_id = Column(String(50), unique=True, nullable=False, comment='字序号')
    latin_form = Column(String(200), nullable=False, comment='拉丁写法')
    phonetic = Column(String(200), comment='音标')
    word_type = Column(String(50), comment='词性')
    
    # 状态信息
    is_favorite = Column(Boolean, default=False, comment='是否收藏')
    sort_order = Column(Integer, default=0, comment='排序顺序')
    notes = Column(Text, comment='备注')
    
    # 关联关系
    definitions = relationship("Definition", back_populates="word_entry", cascade="all, delete-orphan")
    examples = relationship("Example", back_populates="word_entry", cascade="all, delete-orphan")
    images = relationship("WordImage", back_populates="word_entry", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<WordEntry(id={self.id}, word_id='{self.word_id}', latin_form='{self.latin_form}')>"
    
    def get_primary_definition(self):
        """获取主要释义"""
        if self.definitions:
            return self.definitions[0].definition_text
        return ""
    
    def get_all_definitions(self):
        """获取所有释义"""
        return [defn.definition_text for defn in self.definitions]
    
    def get_all_examples(self):
        """获取所有例句"""
        return [(ex.example_text, ex.translation) for ex in self.examples]
    
    def has_images(self):
        """是否有图片"""
        return len(self.images) > 0
    
    def to_dict(self):
        """转换为字典，包含关联数据"""
        data = super().to_dict()
        data['definitions'] = self.get_all_definitions()
        data['examples'] = self.get_all_examples()
        data['has_images'] = self.has_images()
        return data
