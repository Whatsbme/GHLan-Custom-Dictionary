#!/usr/bin/env python3
"""
应用启动脚本（备用版本）
Alternative Application Startup Script
"""

import sys
import os
from pathlib import Path

# 获取当前脚本所在目录
current_dir = Path(__file__).parent.absolute()

# 添加项目根目录到Python路径
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# 设置环境变量
os.environ.setdefault('KIVY_LOG_LEVEL', 'info')

# 打印调试信息
print(f"当前工作目录: {os.getcwd()}")
print(f"脚本所在目录: {current_dir}")
print(f"Python路径: {sys.path[:3]}...")

if __name__ == '__main__':
    try:
        print("正在导入app模块...")
        from app.main import main
        print("app模块导入成功，启动应用...")
        main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保在项目根目录下运行此脚本")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n应用已退出")
        sys.exit(0)
    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)

