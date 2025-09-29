"""
日志工具
Logger Utility
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "offline_dictionary", level: int = logging.INFO):
    """设置日志系统"""
    
    # 创建日志目录
    log_dir = Path.home() / ".offline_dictionary" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件名（按日期）
    log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器（开发环境）
    if os.getenv('DEBUG', 'false').lower() == 'true':
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = None):
    """获取logger实例"""
    if name:
        return logging.getLogger(f"offline_dictionary.{name}")
    return logging.getLogger("offline_dictionary")
