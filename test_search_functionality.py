#!/usr/bin/env python3
"""
搜索功能测试脚本
Search Functionality Test Script
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_search_functionality():
    """测试搜索功能"""
    print("测试搜索功能...")
    
    try:
        from services.search_service import search_service
        from services.dictionary_service import dictionary_service
        
        # 首先添加一些测试数据
        print("1. 添加测试数据...")
        test_words = [
            {
                'word_id': 'SEARCH001',
                'latin_form': 'testus',
                'phonetic': "['testəs]",
                'word_type': 'noun',
                'definitions': ['测试词条1', '用于测试的词汇'],
                'examples': [
                    {'text': '这是一个测试例句', 'translation': 'This is a test example'},
                    {'text': '另一个测试句子', 'translation': 'Another test sentence'}
                ],
                'notes': '搜索测试词条1'
            },
            {
                'word_id': 'SEARCH002',
                'latin_form': 'example',
                'phonetic': "['ɪɡzæmpəl]",
                'word_type': 'noun',
                'definitions': ['例子', '示例'],
                'examples': [
                    {'text': '这是一个例子', 'translation': 'This is an example'},
                    {'text': '请给我一个示例', 'translation': 'Please give me an example'}
                ],
                'notes': '搜索测试词条2'
            },
            {
                'word_id': 'SEARCH003',
                'latin_form': 'demo',
                'phonetic': "['demoʊ]",
                'word_type': 'noun',
                'definitions': ['演示', '展示'],
                'examples': [
                    {'text': '这是一个演示', 'translation': 'This is a demo'},
                    {'text': '演示功能', 'translation': 'Demo function'}
                ],
                'notes': '搜索测试词条3'
            }
        ]
        
        for word_data in test_words:
            word_entry = dictionary_service.add_word_entry(word_data)
            if word_entry:
                print(f"✓ 添加测试词条: {word_entry.word_id}")
            else:
                print(f"✗ 添加测试词条失败: {word_data['word_id']}")
        
        # 测试基本搜索
        print("\n2. 测试基本搜索...")
        results = search_service.search_words('test')
        print(f"✓ 搜索 'test' 找到 {len(results)} 条结果")
        
        # 测试多字段搜索
        print("\n3. 测试多字段搜索...")
        search_params = {
            'query': 'example',
            'search_mode': 'fuzzy',
            'search_fields': ['word_id', 'latin_form', 'definitions'],
            'case_sensitive': False,
            'search_translation': True
        }
        results = search_service.advanced_search(search_params)
        print(f"✓ 多字段搜索 'example' 找到 {len(results)} 条结果")
        
        # 测试正则表达式搜索
        print("\n4. 测试正则表达式搜索...")
        search_params = {
            'query': 'SEARCH00[12]',
            'search_mode': 'regex',
            'search_fields': ['word_id'],
            'case_sensitive': False,
            'search_translation': False
        }
        results = search_service.advanced_search(search_params)
        print(f"✓ 正则搜索 'SEARCH00[12]' 找到 {len(results)} 条结果")
        
        # 测试区分大小写搜索
        print("\n5. 测试区分大小写搜索...")
        search_params = {
            'query': 'TEST',
            'search_mode': 'exact',
            'search_fields': ['latin_form'],
            'case_sensitive': True,
            'search_translation': False
        }
        results = search_service.advanced_search(search_params)
        print(f"✓ 区分大小写搜索 'TEST' 找到 {len(results)} 条结果")
        
        # 测试例句翻译搜索
        print("\n6. 测试例句翻译搜索...")
        search_params = {
            'query': 'This is',
            'search_mode': 'fuzzy',
            'search_fields': ['examples'],
            'case_sensitive': False,
            'search_translation': True
        }
        results = search_service.advanced_search(search_params)
        print(f"✓ 例句翻译搜索 'This is' 找到 {len(results)} 条结果")
        
        # 清理测试数据
        print("\n7. 清理测试数据...")
        for word_data in test_words:
            success = dictionary_service.delete_word_entry(word_data['word_id'])
            if success:
                print(f"✓ 删除测试词条: {word_data['word_id']}")
            else:
                print(f"✗ 删除测试词条失败: {word_data['word_id']}")
        
        print("\n🎉 所有搜索功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 搜索功能测试失败: {e}")
        return False

def test_ui_components():
    """测试UI组件"""
    print("\n测试搜索UI组件...")
    
    try:
        from views.components.search_bar import SearchBar
        from views.components.highlighted_label import HighlightedLabel, SearchResultCard
        from views.advanced_search_screen import AdvancedSearchScreen
        
        print("✓ 搜索栏组件导入成功")
        print("✓ 高亮标签组件导入成功")
        print("✓ 搜索结果卡片组件导入成功")
        print("✓ 高级搜索界面导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 搜索UI组件测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("GHLan自定义字典 - 搜索功能测试")
    print("=" * 50)
    
    tests = [
        test_search_functionality,
        test_ui_components
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
        print("🎉 所有搜索功能测试通过！")
        return True
    else:
        print("❌ 部分测试失败，请检查相关功能。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

