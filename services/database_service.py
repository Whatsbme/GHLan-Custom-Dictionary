"""
数据库服务
Database Service
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import logging

from models.base import Base
from models.settings import SettingsBase
from models import WordEntry, Definition, Example, WordImage, Bookmark, MemoWord, UserSettings
from app.config import config


class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
    
    def _initialize_database(self):
        """初始化数据库连接"""
        try:
            # 创建数据库引擎
            database_url = f"sqlite:///{config.database_path}"
            self.engine = create_engine(
                database_url,
                echo=False,  # 生产环境设为False
                pool_pre_ping=True
            )
            
            # 创建会话工厂
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # 创建所有表
            self.create_tables()
            
            self.logger.info("数据库初始化成功")
            
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
            raise
    
    def create_tables(self):
        """创建数据库表"""
        try:
            Base.metadata.create_all(bind=self.engine)
            SettingsBase.metadata.create_all(bind=self.engine)
            self.logger.info("数据库表创建成功")
        except Exception as e:
            self.logger.error(f"创建数据库表失败: {e}")
            raise
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    def execute_raw_sql(self, sql: str, params=None):
        """执行原始SQL"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            self.logger.error(f"执行SQL失败: {e}")
            raise
    
    def backup_database(self, backup_path: str):
        """备份数据库"""
        try:
            import shutil
            shutil.copy2(config.database_path, backup_path)
            self.logger.info(f"数据库备份成功: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"数据库备份失败: {e}")
            return False
    
    def restore_database(self, backup_path: str):
        """恢复数据库"""
        try:
            import shutil
            shutil.copy2(backup_path, config.database_path)
            self.logger.info(f"数据库恢复成功: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"数据库恢复失败: {e}")
            return False
    
    def get_database_info(self):
        """获取数据库信息"""
        try:
            with self.get_session() as session:
                # 获取表信息
                tables_info = {}
                for table_name in ['word_entries', 'definitions', 'examples', 'bookmarks', 'memo_words']:
                    result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.scalar()
                    tables_info[table_name] = count
                
                # 获取数据库文件大小
                db_size = Path(config.database_path).stat().st_size if Path(config.database_path).exists() else 0
                
                return {
                    'tables': tables_info,
                    'size_mb': round(db_size / (1024 * 1024), 2),
                    'path': str(config.database_path)
                }
        except Exception as e:
            self.logger.error(f"获取数据库信息失败: {e}")
            return None
    
    def close(self):
        """关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("数据库连接已关闭")


# 全局数据库服务实例
db_service = DatabaseService()
