"""
测试套件
Test Suite
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 测试配置
TEST_CONFIG = {
    'database_path': ':memory:',  # 使用内存数据库进行测试
    'log_level': 'WARNING',       # 测试时减少日志输出
    'test_data_dir': project_root / 'tests' / 'data',
    'temp_dir': project_root / 'tests' / 'temp'
}

# 创建测试目录
TEST_CONFIG['test_data_dir'].mkdir(parents=True, exist_ok=True)
TEST_CONFIG['temp_dir'].mkdir(parents=True, exist_ok=True)