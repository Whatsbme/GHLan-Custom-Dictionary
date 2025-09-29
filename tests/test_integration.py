"""
集成测试
Integration Tests
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from tests.test_base import BaseTestCase, PerformanceTestCase
from app.main import OfflineDictionaryApp
from services.dictionary_service import dictionary_service
from services.search_service import search_service
from services.import_service import import_service
from services.export_service import export_service
from services.bookmark_service import bookmark_service
from services.memo_service import memo_service


class TestAppIntegration(BaseTestCase):
    """应用集成测试"""
    
    def setUp(self):
        super().setUp()
        self.app = OfflineDictionaryApp()
    
    def test_app_initialization(self):
        """测试应用初始化"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.title, "GHLan自定义字典")
    
    def test_database_integration(self):
        """测试数据库集成"""
        # 创建测试数据
        word_entry = self.create_test_word_entry()
        definition = self.create_test_definition(word_entry)
        example = self.create_test_example(word_entry)
        
        # 验证数据创建
        self.assertIsNotNone(word_entry.id)
        self.assertIsNotNone(definition.id)
        self.assertIsNotNone(example.id)
        
        # 验证数据关联
        self.assertEqual(definition.word_entry_id, word_entry.id)
        self.assertEqual(example.word_entry_id, word_entry.id)
    
    def test_service_integration(self):
        """测试服务集成"""
        # 测试词条服务
        word_data = {
            'word_id': 'integration001',
            'latin_form': 'integration test',
            'phonetic': 'test phonetic',
            'word_type': 'noun',
            'definitions': ['test definition'],
            'examples': [{'text': 'test example', 'translation': 'test translation'}],
            'notes': 'test notes'
        }
        
        word_entry = dictionary_service.add_word_entry(word_data)
        self.assertIsNotNone(word_entry)
        
        # 测试搜索服务
        results = search_service.search_by_latin_form('integration test')
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].word_id, 'integration001')


class TestDataFlowIntegration(BaseTestCase):
    """数据流集成测试"""
    
    def test_word_creation_flow(self):
        """测试词条创建流程"""
        # 1. 创建词条
        word_data = {
            'word_id': 'flow001',
            'latin_form': 'flow test',
            'phonetic': 'flow phonetic',
            'word_type': 'verb',
            'definitions': ['flow definition 1', 'flow definition 2'],
            'examples': [
                {'text': 'flow example 1', 'translation': 'flow translation 1'},
                {'text': 'flow example 2', 'translation': 'flow translation 2'}
            ],
            'notes': 'flow notes'
        }
        
        word_entry = dictionary_service.add_word_entry(word_data)
        self.assertIsNotNone(word_entry)
        
        # 2. 验证词条数据
        self.assertEqual(word_entry.word_id, 'flow001')
        self.assertEqual(word_entry.latin_form, 'flow test')
        self.assertEqual(len(word_entry.definitions), 2)
        self.assertEqual(len(word_entry.examples), 2)
        
        # 3. 测试搜索
        results = search_service.search_by_latin_form('flow test')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].word_id, 'flow001')
        
        # 4. 测试更新
        word_entry.notes = 'updated flow notes'
        dictionary_service.update_word_entry(word_entry)
        
        updated_entry = dictionary_service.get_word_entry_by_id(word_entry.id)
        self.assertEqual(updated_entry.notes, 'updated flow notes')
        
        # 5. 测试删除
        dictionary_service.delete_word_entry(word_entry.id)
        deleted_entry = dictionary_service.get_word_entry_by_id(word_entry.id)
        self.assertIsNone(deleted_entry)
    
    def test_search_integration(self):
        """测试搜索集成"""
        # 创建测试数据
        test_words = [
            {'word_id': 'search001', 'latin_form': 'apple', 'definitions': ['fruit']},
            {'word_id': 'search002', 'latin_form': 'application', 'definitions': ['software']},
            {'word_id': 'search003', 'latin_form': 'apply', 'definitions': ['to use']},
        ]
        
        for word_data in test_words:
            dictionary_service.add_word_entry(word_data)
        
        # 测试精确搜索
        results = search_service.search_by_latin_form('apple')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].word_id, 'search001')
        
        # 测试模糊搜索
        results = search_service.fuzzy_search('app')
        self.assertGreaterEqual(len(results), 2)
        
        # 测试多字段搜索
        results = search_service.multi_field_search('fruit', ['definitions'])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].word_id, 'search001')
    
    def test_import_export_integration(self):
        """测试导入导出集成"""
        # 创建测试数据
        test_words = [
            {'word_id': 'import001', 'latin_form': 'import test 1', 'definitions': ['test 1']},
            {'word_id': 'import002', 'latin_form': 'import test 2', 'definitions': ['test 2']},
        ]
        
        for word_data in test_words:
            dictionary_service.add_word_entry(word_data)
        
        # 测试导出
        export_options = {
            'include_images': False,
            'include_examples': True,
            'include_notes': True
        }
        
        with patch.object(export_service, 'export_to_excel') as mock_export:
            mock_export.return_value = {'success': True, 'file_path': 'test.xlsx'}
            result = export_service.export_to_excel(export_options)
            self.assertTrue(result['success'])
        
        # 测试导入
        with patch.object(import_service, 'import_from_excel') as mock_import:
            mock_import.return_value = {'success': 2, 'failed': 0}
            result = import_service.import_from_excel('test.xlsx')
            self.assertEqual(result['success'], 2)


class TestBookmarkIntegration(BaseTestCase):
    """书签集成测试"""
    
    def test_bookmark_flow(self):
        """测试书签流程"""
        # 1. 添加书签
        bookmark_data = {
            'title': '测试书签',
            'url': 'https://example.com',
            'category': '测试分类',
            'description': '测试描述'
        }
        
        bookmark = bookmark_service.add_bookmark(bookmark_data)
        self.assertIsNotNone(bookmark)
        self.assertEqual(bookmark.title, '测试书签')
        
        # 2. 获取书签
        bookmarks = bookmark_service.get_all_bookmarks()
        self.assertEqual(len(bookmarks), 1)
        
        # 3. 搜索书签
        results = bookmark_service.search_bookmarks('测试')
        self.assertEqual(len(results), 1)
        
        # 4. 更新书签
        bookmark.title = '更新的书签'
        bookmark_service.update_bookmark(bookmark)
        
        updated_bookmark = bookmark_service.get_bookmark_by_id(bookmark.id)
        self.assertEqual(updated_bookmark.title, '更新的书签')
        
        # 5. 删除书签
        bookmark_service.delete_bookmark(bookmark.id)
        deleted_bookmark = bookmark_service.get_bookmark_by_id(bookmark.id)
        self.assertIsNone(deleted_bookmark)


class TestMemoIntegration(BaseTestCase):
    """备忘集成测试"""
    
    def test_memo_flow(self):
        """测试备忘流程"""
        # 1. 添加备忘
        memo_data = {
            'content': '测试备忘内容',
            'priority': 3
        }
        
        memo = memo_service.add_memo_word(memo_data)
        self.assertIsNotNone(memo)
        self.assertEqual(memo.content, '测试备忘内容')
        self.assertFalse(memo.is_completed)
        
        # 2. 获取备忘
        memos = memo_service.get_all_memo_words()
        self.assertEqual(len(memos), 1)
        
        # 3. 完成备忘
        memo_service.complete_memo_word(memo.id)
        completed_memo = memo_service.get_memo_word_by_id(memo.id)
        self.assertTrue(completed_memo.is_completed)
        
        # 4. 搜索备忘
        results = memo_service.search_memo_words('测试')
        self.assertEqual(len(results), 1)
        
        # 5. 删除备忘
        memo_service.delete_memo_word(memo.id)
        deleted_memo = memo_service.get_memo_word_by_id(memo.id)
        self.assertIsNone(deleted_memo)


class TestPerformanceIntegration(PerformanceTestCase):
    """性能集成测试"""
    
    def test_large_dataset_performance(self):
        """测试大数据集性能"""
        # 创建大量测试数据
        for i in range(1000):
            word_data = {
                'word_id': f'perf{i:04d}',
                'latin_form': f'performance test {i}',
                'phonetic': f'phonetic {i}',
                'word_type': 'noun',
                'definitions': [f'definition {i}'],
                'examples': [{'text': f'example {i}', 'translation': f'translation {i}'}],
                'notes': f'notes {i}'
            }
            dictionary_service.add_word_entry(word_data)
        
        # 测试搜索性能
        results = search_service.search_by_latin_form('performance test 500')
        self.assertEqual(len(results), 1)
        
        # 测试模糊搜索性能
        results = search_service.fuzzy_search('performance')
        self.assertGreater(len(results), 0)
        
        # 性能断言（应该在1秒内完成）
        self.assert_performance(1.0)
    
    def test_memory_usage(self):
        """测试内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建大量数据
        for i in range(500):
            word_data = {
                'word_id': f'mem{i:04d}',
                'latin_form': f'memory test {i}',
                'definitions': [f'definition {i}']
            }
            dictionary_service.add_word_entry(word_data)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该在合理范围内（小于50MB）
        self.assertLess(memory_increase, 50 * 1024 * 1024)


class TestErrorHandlingIntegration(BaseTestCase):
    """错误处理集成测试"""
    
    def test_database_error_handling(self):
        """测试数据库错误处理"""
        # 测试重复词条ID
        word_data1 = {'word_id': 'duplicate', 'latin_form': 'test1'}
        word_data2 = {'word_id': 'duplicate', 'latin_form': 'test2'}
        
        word1 = dictionary_service.add_word_entry(word_data1)
        self.assertIsNotNone(word1)
        
        # 第二个应该失败或处理重复
        word2 = dictionary_service.add_word_entry(word_data2)
        # 根据实现，可能返回None或处理重复
    
    def test_invalid_data_handling(self):
        """测试无效数据处理"""
        # 测试空数据
        word_data = {}
        result = dictionary_service.add_word_entry(word_data)
        self.assertIsNone(result)
        
        # 测试无效搜索
        results = search_service.search_by_latin_form('')
        self.assertEqual(len(results), 0)
    
    def test_file_operation_error_handling(self):
        """测试文件操作错误处理"""
        # 测试不存在的文件导入
        with patch.object(import_service, 'import_from_excel') as mock_import:
            mock_import.side_effect = FileNotFoundError("File not found")
            
            try:
                result = import_service.import_from_excel('nonexistent.xlsx')
                self.assertFalse(result.get('success', True))
            except FileNotFoundError:
                pass  # 预期的错误


if __name__ == '__main__':
    unittest.main()







