"""
文件管理工具
File Manager Utilities
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

from app.config import config


class FileManager:
    """文件管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = config.data_dir
        self.images_dir = config.images_dir
        self.exports_dir = config.exports_dir
        self.imports_dir = config.imports_dir
    
    def ensure_directories(self):
        """确保所有必要的目录存在"""
        directories = [
            self.data_dir,
            self.images_dir,
            self.exports_dir,
            self.imports_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, image_data: bytes, filename: str) -> Optional[str]:
        """保存图片文件"""
        try:
            self.ensure_directories()
            filepath = self.images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            self.logger.info(f"图片保存成功: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"保存图片失败: {e}")
            return None
    
    def load_image(self, filename: str) -> Optional[bytes]:
        """加载图片文件"""
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    return f.read()
        except Exception as e:
            self.logger.error(f"加载图片失败: {e}")
        return None
    
    def delete_image(self, filename: str) -> bool:
        """删除图片文件"""
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                filepath.unlink()
                self.logger.info(f"图片删除成功: {filepath}")
                return True
        except Exception as e:
            self.logger.error(f"删除图片失败: {e}")
        return False
    
    def list_images(self) -> List[Dict[str, Any]]:
        """列出所有图片文件"""
        try:
            self.ensure_directories()
            images = []
            
            for filepath in self.images_dir.iterdir():
                if filepath.is_file() and filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    stat = filepath.stat()
                    images.append({
                        'filename': filepath.name,
                        'path': str(filepath),
                        'size': stat.st_size,
                        'created': stat.st_ctime,
                        'modified': stat.st_mtime
                    })
            
            return sorted(images, key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            self.logger.error(f"列出图片失败: {e}")
            return []
    
    def save_export_file(self, content: bytes, filename: str) -> Optional[str]:
        """保存导出文件"""
        try:
            self.ensure_directories()
            filepath = self.exports_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(content)
            
            self.logger.info(f"导出文件保存成功: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"保存导出文件失败: {e}")
            return None
    
    def list_export_files(self) -> List[Dict[str, Any]]:
        """列出所有导出文件"""
        try:
            self.ensure_directories()
            files = []
            
            for filepath in self.exports_dir.iterdir():
                if filepath.is_file():
                    stat = filepath.stat()
                    files.append({
                        'filename': filepath.name,
                        'path': str(filepath),
                        'size': stat.st_size,
                        'created': stat.st_ctime,
                        'modified': stat.st_mtime
                    })
            
            return sorted(files, key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            self.logger.error(f"列出导出文件失败: {e}")
            return []
    
    def cleanup_old_files(self, days: int = 30):
        """清理旧文件"""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            # 清理导出文件
            for filepath in self.exports_dir.iterdir():
                if filepath.is_file() and filepath.stat().st_mtime < cutoff_time:
                    filepath.unlink()
                    self.logger.info(f"清理旧文件: {filepath}")
            
            # 清理临时图片
            for filepath in self.images_dir.iterdir():
                if filepath.is_file() and filepath.stat().st_mtime < cutoff_time:
                    # 只删除临时文件，保留用户上传的图片
                    if filepath.name.startswith('temp_'):
                        filepath.unlink()
                        self.logger.info(f"清理临时图片: {filepath}")
        
        except Exception as e:
            self.logger.error(f"清理旧文件失败: {e}")
    
    def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        try:
            self.ensure_directories()
            
            def get_dir_size(directory: Path) -> int:
                total_size = 0
                for filepath in directory.rglob('*'):
                    if filepath.is_file():
                        total_size += filepath.stat().st_size
                return total_size
            
            return {
                'images_size': get_dir_size(self.images_dir),
                'exports_size': get_dir_size(self.exports_dir),
                'imports_size': get_dir_size(self.imports_dir),
                'total_size': get_dir_size(self.data_dir)
            }
        except Exception as e:
            self.logger.error(f"获取存储信息失败: {e}")
            return {}


# 全局文件管理器实例
file_manager = FileManager()
