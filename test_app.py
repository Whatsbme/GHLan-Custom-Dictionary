#!/usr/bin/env python3
"""
应用测试脚本
Application Test Script
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        from app.config import config
        print("✓ 配置模块导入成功")
    except Exception as e:
        print(f"✗ 配置模块导入失败: {e}")
        return False
    
    try:
        from models import WordEntry, Definition, Example
        print("✓ 数据模型导入成功")
    except Exception as e:
        print(f"✗ 数据模型导入失败: {e}")
        return False
    
    try:
        from services.database_service import db_service
        print("✓ 数据库服务导入成功")
    except Exception as e:
        print(f"✗ 数据库服务导入失败: {e}")
        return False
    
    try:
        from services.dictionary_service import dictionary_service
        print("✓ 词典服务导入成功")
    except Exception as e:
        print(f"✗ 词典服务导入失败: {e}")
        return False
    
    try:
        from utils.validators import Validators
        print("✓ 验证器导入成功")
    except Exception as e:
        print(f"✗ 验证器导入失败: {e}")
        return False
    
    return True

def test_database():
    """测试数据库连接"""
    print("\n测试数据库连接...")
    
    try:
        from services.database_service import db_service
        
        # 测试数据库信息
        db_info = db_service.get_database_info()
        if db_info:
            print(f"✓ 数据库连接成功")
            print(f"  - 路径: {db_info.get('path', 'N/A')}")
            print(f"  - 大小: {db_info.get('size_mb', 0)} MB")
            print(f"  - 表数量: {len(db_info.get('tables', []))}")
            return True
        else:
            print("✗ 无法获取数据库信息")
            return False
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def test_validators():
    """测试验证器"""
    print("\n测试验证器...")
    
    try:
        from utils.validators import Validators
        
        # 测试字序号验证
        result = Validators.validate_word_id("TEST001")
        if result['valid']:
            print("✓ 字序号验证正常")
        else:
            print(f"✗ 字序号验证失败: {result['errors']}")
            return False
        
        # 测试拉丁写法验证
        result = Validators.validate_latin_form("testus")
        if result['valid']:
            print("✓ 拉丁写法验证正常")
        else:
            print(f"✗ 拉丁写法验证失败: {result['errors']}")
            return False
        
        # 测试释义验证
        result = Validators.validate_definitions(['测试释义1', '测试释义2'])
        if result['valid']:
            print("✓ 释义验证正常")
        else:
            print(f"✗ 释义验证失败: {result['errors']}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ 验证器测试失败: {e}")
        return False

def test_config():
    """测试配置管理"""
    print("\n测试配置管理...")
    
    try:
        from app.config import config
        
        # 测试配置读取
        app_name = config.get('APP', 'name', 'Unknown')
        print(f"✓ 应用名称: {app_name}")
        
        # 测试配置设置
        config.set('TEST', 'test_key', 'test_value')
        test_value = config.get('TEST', 'test_key')
        if test_value == 'test_value':
            print("✓ 配置设置和读取正常")
            return True
        else:
            print("✗ 配置设置和读取失败")
            return False
    except Exception as e:
        print(f"✗ 配置管理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("离线词典应用测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_validators,
        test_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用可以正常运行。")
        return True
    else:
        print("❌ 部分测试失败，请检查相关模块。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
