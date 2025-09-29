"""
用户设置模型
User Settings Model
"""

from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


# 创建专门用于设置表的基础类
SettingsBase = declarative_base()


class UserSettings(SettingsBase):
    """用户设置模型"""
    
    __tablename__ = 'user_settings'
    
    # 设置信息
    key = Column(String(100), primary_key=True, comment='设置键')
    value = Column(Text, comment='设置值')
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<UserSettings(key='{self.key}', value='{self.value}')>"
