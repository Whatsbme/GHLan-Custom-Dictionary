#!/usr/bin/env python3
"""
应用启动脚本
Application Startup Script
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault('KIVY_LOG_LEVEL', 'info')

if __name__ == '__main__':
    try:
        from app.main import main
        main()
    except KeyboardInterrupt:
        print("\n应用已退出")
        sys.exit(0)
    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)
