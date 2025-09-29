"""
数据库工具
Database Utilities
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from app.config import config


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = config.database_path
    
    def create_connection(self) -> Optional[sqlite3.Connection]:
        """创建数据库连接"""
        try:
            # 确保数据库目录存在
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
            return conn
        except Exception as e:
            self.logger.error(f"创建数据库连接失败: {e}")
            return None
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        try:
            with self.create_connection() as conn:
                if conn:
                    cursor = conn.execute(query, params)
                    return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"执行查询失败: {e}")
        return []
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """执行更新操作"""
        try:
            with self.create_connection() as conn:
                if conn:
                    conn.execute(query, params)
                    conn.commit()
                    return True
        except Exception as e:
            self.logger.error(f"执行更新失败: {e}")
        return False
    
    def backup_database(self, backup_path: str) -> bool:
        """备份数据库"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"数据库备份成功: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"数据库备份失败: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """获取数据库信息"""
        try:
            if not self.db_path.exists():
                return {'exists': False}
            
            # 获取文件大小
            size_bytes = self.db_path.stat().st_size
            
            # 获取表信息
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = self.execute_query(tables_query)
            
            return {
                'exists': True,
                'path': str(self.db_path),
                'size_mb': round(size_bytes / (1024 * 1024), 2),
                'tables': [table['name'] for table in tables]
            }
        except Exception as e:
            self.logger.error(f"获取数据库信息失败: {e}")
            return {'exists': False, 'error': str(e)}
