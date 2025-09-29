#!/usr/bin/env python3
"""
测试运行脚本
Test Runner Script
"""

import sys
import os
import unittest
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_basic_tests():
    """运行基础测试"""
    print("🧪 运行基础测试...")
    
    try:
        # 测试导入
        from tests.test_base import BaseTestCase
        print("✅ 测试基础类导入成功")
        
        from utils.ink_theme import ink_theme
        print("✅ 水墨主题导入成功")
        
        from views.components.ink_card import InkCard
        print("✅ 水墨卡片组件导入成功")
        
        from views.components.ink_button import InkButton
        print("✅ 水墨按钮组件导入成功")
        
        from views.components.ink_input import InkTextField
        print("✅ 水墨输入组件导入成功")
        
        from views.components.ink_navigation import InkToolbar
        print("✅ 水墨导航组件导入成功")
        
        # 测试主题文件
        import json
        with open('assets/themes/ink_theme.json', 'r', encoding='utf-8') as f:
            theme_data = json.load(f)
        print(f"✅ 水墨主题文件加载成功: {theme_data['name']}")
        
        with open('assets/fonts/font_config.json', 'r', encoding='utf-8') as f:
            font_data = json.load(f)
        print(f"✅ 字体配置文件加载成功，包含 {len(font_data['fonts'])} 种字体")
        
        with open('assets/themes/color_themes.json', 'r', encoding='utf-8') as f:
            color_data = json.load(f)
        print(f"✅ 纯色主题文件加载成功，包含 {len(color_data['themes'])} 个主题")
        
        # 测试Logo生成器
        from assets.icons.ghlan_logo import GHLanLogoGenerator
        generator = GHLanLogoGenerator()
        print("✅ Logo生成器创建成功")
        
        print("\n🎉 所有基础测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_component_tests():
    """运行组件测试"""
    print("\n🧪 运行组件测试...")
    
    try:
        from views.components.ink_card import InkCard, InkInfoCard, InkActionCard
        from views.components.ink_button import InkButton, InkIconButton, InkFloatingButton
        from views.components.ink_input import InkTextField, InkSearchField, InkForm
        from views.components.ink_navigation import InkToolbar, InkTabBar, InkPagination
        
        # 测试卡片组件
        card = InkCard(title="测试卡片", content="测试内容")
        print("✅ 水墨卡片组件创建成功")
        
        info_card = InkInfoCard(icon="information", title="信息卡片", info="测试信息")
        print("✅ 信息卡片组件创建成功")
        
        # 测试按钮组件
        button = InkButton(text="测试按钮", ink_style="primary")
        print("✅ 水墨按钮组件创建成功")
        
        icon_button = InkIconButton(icon="home", ink_style="accent")
        print("✅ 图标按钮组件创建成功")
        
        # 测试输入组件
        text_field = InkTextField(hint_text="测试输入")
        print("✅ 文本输入组件创建成功")
        
        search_field = InkSearchField(hint_text="搜索...")
        print("✅ 搜索输入组件创建成功")
        
        # 测试导航组件
        toolbar = InkToolbar(title="测试工具栏")
        print("✅ 工具栏组件创建成功")
        
        print("\n🎉 所有组件测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 组件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_service_tests():
    """运行服务测试"""
    print("\n🧪 运行服务测试...")
    
    try:
        from services.dictionary_service import dictionary_service
        from services.search_service import search_service
        from services.bookmark_service import bookmark_service
        from services.memo_service import memo_service
        
        # 测试服务初始化
        print("✅ 词条服务初始化成功")
        print("✅ 搜索服务初始化成功")
        print("✅ 书签服务初始化成功")
        print("✅ 备忘服务初始化成功")
        
        print("\n🎉 所有服务测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 服务测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_theme_tests():
    """运行主题测试"""
    print("\n🧪 运行主题测试...")
    
    try:
        from utils.ink_theme import ink_theme
        from utils.theme_manager import theme_manager
        
        # 测试颜色获取
        color = ink_theme.get_color('ink_black')
        print("✅ 水墨颜色获取成功")
        
        # 测试样式获取
        style = ink_theme.get_ink_style()
        print("✅ 水墨样式获取成功")
        
        # 测试主题管理器
        print("✅ 主题管理器初始化成功")
        
        print("\n🎉 所有主题测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 主题测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 GHLan自定义字典 - 测试运行器")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        run_basic_tests,
        run_component_tests,
        run_service_tests,
        run_theme_tests
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用准备就绪。")
        return 0
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())







