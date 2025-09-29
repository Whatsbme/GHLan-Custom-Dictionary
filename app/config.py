"""
应用配置管理
Application Configuration Management
"""

import os
from configparser import ConfigParser
from pathlib import Path


class Config:
    """应用配置类"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".offline_dictionary"
        self.config_file = self.config_dir / "config.ini"
        self.data_dir = self.config_dir / "data"
        self.images_dir = self.data_dir / "images"
        self.exports_dir = self.data_dir / "exports"
        self.imports_dir = self.data_dir / "imports"
        self.database_path = self.data_dir / "dictionary.db"
        
        # 创建必要的目录
        self._create_directories()
        
        # 加载配置
        self.config = ConfigParser()
        self._load_config()
    
    def _create_directories(self):
        """创建必要的目录"""
        for directory in [self.config_dir, self.data_dir, self.images_dir, self.exports_dir, self.imports_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        self.config['APP'] = {
            'name': 'GHLan自定义字典',
            'version': '1.0.0',
            'language': 'zh_CN',
            'auto_save': 'true',
            'show_welcome': 'true'
        }
        
        self.config['THEME'] = {
            'style': 'light',
            'primary_palette': 'Blue',
            'accent_palette': 'Orange'
        }
        
        self.config['FONT'] = {
            'size': '16',
            'family': 'default'
        }
        
        self.config['SEARCH'] = {
            'default_type': 'all',
            'save_history': 'true',
            'default_fuzzy': 'true',
            'case_sensitive': 'false',
            'search_in_definitions': 'true'
        }
        
        self.config['DATABASE'] = {
            'path': str(self.database_path),
            'backup_enabled': 'true',
            'backup_interval': '7'  # days
        }
        
        self.config['EXPORT'] = {
            'default_format': 'pdf',
            'include_images': 'true',
            'include_examples': 'true'
        }
        
        self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get(self, section, key, fallback=None):
        """获取配置值"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section, key, value):
        """设置配置值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save_config()
    
    def get_boolean(self, section, key, fallback=False):
        """获取布尔配置值"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    def get_int(self, section, key, fallback=0):
        """获取整数配置值"""
        return self.config.getint(section, key, fallback=fallback)
    
    def save(self):
        """保存配置"""
        self.save_config()


# 全局配置实例
config = Config()
