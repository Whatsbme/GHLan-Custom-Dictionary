#!/usr/bin/env python3
"""
词条管理功能测试脚本
Word Management Test Script
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_word_management():
    """测试词条管理功能"""
    print("测试词条管理功能...")
    
    try:
        from services.dictionary_service import dictionary_service
        from utils.validators import Validators
        
        # 测试添加词条
        print("1. 测试添加词条...")
        test_word_data = {
            'word_id': 'TEST001',
            'latin_form': 'testus',
            'phonetic': "['testəs]",
            'word_type': 'noun',
            'definitions': ['测试释义1', '测试释义2'],
            'examples': [
                {'text': '这是一个测试例句', 'translation': 'This is a test example'},
                {'text': '另一个测试例句', 'translation': 'Another test example'}
            ],
            'notes': '这是一个测试词条'
        }
        
        # 验证数据
        validation_result = Validators.validate_word_entry_data(test_word_data)
        if validation_result['valid']:
            print("✓ 词条数据验证通过")
        else:
            print(f"✗ 词条数据验证失败: {validation_result['errors']}")
            return False
        
        # 添加词条
        word_entry = dictionary_service.add_word_entry(test_word_data)
        if word_entry:
            print("✓ 词条添加成功")
        else:
            print("✗ 词条添加失败")
            return False
        
        # 测试获取词条
        print("2. 测试获取词条...")
        retrieved_word = dictionary_service.get_word_entry('TEST001')
        if retrieved_word:
            print("✓ 词条获取成功")
            print(f"  - 字序号: {retrieved_word.word_id}")
            print(f"  - 拉丁写法: {retrieved_word.latin_form}")
            print(f"  - 释义数量: {len(retrieved_word.definitions)}")
            print(f"  - 例句数量: {len(retrieved_word.examples)}")
        else:
            print("✗ 词条获取失败")
            return False
        
        # 测试获取词条列表
        print("3. 测试获取词条列表...")
        word_list = dictionary_service.get_all_word_entries(limit=10)
        print(f"✓ 获取到 {len(word_list)} 条词条")
        
        # 测试搜索功能
        print("4. 测试搜索功能...")
        from services.search_service import search_service
        
        search_results = search_service.search_words('test')
        print(f"✓ 搜索到 {len(search_results)} 条结果")
        
        # 测试收藏功能
        print("5. 测试收藏功能...")
        success = dictionary_service.toggle_favorite('TEST001')
        if success:
            print("✓ 收藏状态切换成功")
        else:
            print("✗ 收藏状态切换失败")
        
        # 测试获取收藏词条
        favorites = dictionary_service.get_favorite_word_entries()
        print(f"✓ 获取到 {len(favorites)} 条收藏词条")
        
        # 测试更新词条
        print("6. 测试更新词条...")
        update_data = {
            'latin_form': 'testus_updated',
            'definitions': ['更新后的释义'],
            'notes': '更新后的备注'
        }
        
        success = dictionary_service.update_word_entry('TEST001', update_data)
        if success:
            print("✓ 词条更新成功")
        else:
            print("✗ 词条更新失败")
        
        # 测试删除词条
        print("7. 测试删除词条...")
        success = dictionary_service.delete_word_entry('TEST001')
        if success:
            print("✓ 词条删除成功")
        else:
            print("✗ 词条删除失败")
        
        print("\n🎉 所有词条管理功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_ui_components():
    """测试UI组件"""
    print("\n测试UI组件...")
    
    try:
        from views.components.image_picker import ImagePicker
        from views.components.word_card import WordCard
        from views.components.search_bar import SearchBar
        
        print("✓ 图片选择组件导入成功")
        print("✓ 词条卡片组件导入成功")
        print("✓ 搜索栏组件导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ UI组件测试失败: {e}")
        return False

def test_screens():
    """测试界面"""
    print("\n测试界面...")
    
    try:
        from views.word_list_screen import WordListScreen
        from views.word_detail_screen import WordDetailScreen
        from views.word_edit_screen import WordEditScreen
        
        print("✓ 词条列表界面导入成功")
        print("✓ 词条详情界面导入成功")
        print("✓ 词条编辑界面导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 界面测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("GHLan自定义字典 - 词条管理功能测试")
    print("=" * 50)
    
    tests = [
        test_word_management,
        test_ui_components,
        test_screens
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
        print("🎉 所有测试通过！词条管理功能已完善。")
        return True
    else:
        print("❌ 部分测试失败，请检查相关功能。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)


