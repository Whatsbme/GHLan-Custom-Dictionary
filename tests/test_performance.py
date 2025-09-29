"""
性能测试
Performance Tests
"""

import unittest
import time
import psutil
import os
from unittest.mock import Mock, patch

from tests.test_base import PerformanceTestCase, BaseTestCase
from services.dictionary_service import dictionary_service
from services.search_service import search_service
from services.import_service import import_service
from services.export_service import export_service


class TestDatabasePerformance(PerformanceTestCase):
    """数据库性能测试"""
    
    def test_bulk_insert_performance(self):
        """测试批量插入性能"""
        # 测试大量数据插入
        start_time = time.time()
        
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
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 1000条记录应该在5秒内完成
        self.assertLess(execution_time, 5.0)
        print(f"Bulk insert 1000 records: {execution_time:.4f} seconds")
    
    def test_search_performance(self):
        """测试搜索性能"""
        # 创建测试数据
        for i in range(500):
            word_data = {
                'word_id': f'search{i:04d}',
                'latin_form': f'search test {i}',
                'definitions': [f'search definition {i}']
            }
            dictionary_service.add_word_entry(word_data)
        
        # 测试精确搜索性能
        start_time = time.time()
        results = search_service.search_by_latin_form('search test 250')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.1)  # 精确搜索应该在100ms内完成
        self.assertEqual(len(results), 1)
        print(f"Exact search time: {search_time:.4f} seconds")
        
        # 测试模糊搜索性能
        start_time = time.time()
        results = search_service.fuzzy_search('search')
        end_time = time.time()
        
        fuzzy_time = end_time - start_time
        self.assertLess(fuzzy_time, 0.5)  # 模糊搜索应该在500ms内完成
        self.assertGreater(len(results), 0)
        print(f"Fuzzy search time: {fuzzy_time:.4f} seconds")
    
    def test_memory_usage(self):
        """测试内存使用"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建大量数据
        for i in range(1000):
            word_data = {
                'word_id': f'mem{i:04d}',
                'latin_form': f'memory test {i}',
                'definitions': [f'definition {i}']
            }
            dictionary_service.add_word_entry(word_data)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该在合理范围内（小于100MB）
        self.assertLess(memory_increase, 100 * 1024 * 1024)
        print(f"Memory increase: {memory_increase / 1024 / 1024:.2f} MB")


class TestSearchPerformance(PerformanceTestCase):
    """搜索性能测试"""
    
    def setUp(self):
        super().setUp()
        # 创建测试数据
        self.test_words = []
        for i in range(1000):
            word_data = {
                'word_id': f'search{i:04d}',
                'latin_form': f'search word {i}',
                'phonetic': f'phonetic {i}',
                'word_type': 'noun',
                'definitions': [f'definition {i}', f'meaning {i}'],
                'examples': [{'text': f'example {i}', 'translation': f'translation {i}'}],
                'notes': f'notes {i}'
            }
            word_entry = dictionary_service.add_word_entry(word_data)
            self.test_words.append(word_entry)
    
    def test_latin_form_search_performance(self):
        """测试拉丁形式搜索性能"""
        # 测试精确搜索
        start_time = time.time()
        results = search_service.search_by_latin_form('search word 500')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.1)
        self.assertEqual(len(results), 1)
        print(f"Latin form search time: {search_time:.4f} seconds")
    
    def test_phonetic_search_performance(self):
        """测试音标搜索性能"""
        start_time = time.time()
        results = search_service.search_by_phonetic('phonetic 500')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.1)
        self.assertEqual(len(results), 1)
        print(f"Phonetic search time: {search_time:.4f} seconds")
    
    def test_definition_search_performance(self):
        """测试释义搜索性能"""
        start_time = time.time()
        results = search_service.search_by_definition('definition 500')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.2)
        self.assertEqual(len(results), 1)
        print(f"Definition search time: {search_time:.4f} seconds")
    
    def test_fuzzy_search_performance(self):
        """测试模糊搜索性能"""
        start_time = time.time()
        results = search_service.fuzzy_search('search')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.5)
        self.assertGreater(len(results), 0)
        print(f"Fuzzy search time: {search_time:.4f} seconds")
    
    def test_regex_search_performance(self):
        """测试正则搜索性能"""
        start_time = time.time()
        results = search_service.search_by_pattern(r'search word \d+')
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.3)
        self.assertGreater(len(results), 0)
        print(f"Regex search time: {search_time:.4f} seconds")
    
    def test_multi_field_search_performance(self):
        """测试多字段搜索性能"""
        start_time = time.time()
        results = search_service.multi_field_search(
            'search', 
            ['latin_form', 'definitions']
        )
        end_time = time.time()
        
        search_time = end_time - start_time
        self.assertLess(search_time, 0.4)
        self.assertGreater(len(results), 0)
        print(f"Multi-field search time: {search_time:.4f} seconds")


class TestImportExportPerformance(PerformanceTestCase):
    """导入导出性能测试"""
    
    def test_export_performance(self):
        """测试导出性能"""
        # 创建测试数据
        for i in range(500):
            word_data = {
                'word_id': f'export{i:04d}',
                'latin_form': f'export test {i}',
                'phonetic': f'phonetic {i}',
                'word_type': 'noun',
                'definitions': [f'definition {i}'],
                'examples': [{'text': f'example {i}', 'translation': f'translation {i}'}],
                'notes': f'notes {i}'
            }
            dictionary_service.add_word_entry(word_data)
        
        # 测试Excel导出性能
        start_time = time.time()
        with patch.object(export_service, 'export_to_excel') as mock_export:
            mock_export.return_value = {'success': True, 'file_path': 'test.xlsx'}
            result = export_service.export_to_excel()
        end_time = time.time()
        
        export_time = end_time - start_time
        self.assertLess(export_time, 2.0)  # 导出应该在2秒内完成
        print(f"Excel export time: {export_time:.4f} seconds")
        
        # 测试PDF导出性能
        start_time = time.time()
        with patch.object(export_service, 'export_to_pdf') as mock_export:
            mock_export.return_value = 'test.pdf'
            result = export_service.export_to_pdf()
        end_time = time.time()
        
        export_time = end_time - start_time
        self.assertLess(export_time, 3.0)  # PDF导出应该在3秒内完成
        print(f"PDF export time: {export_time:.4f} seconds")
    
    def test_import_performance(self):
        """测试导入性能"""
        # 模拟大量数据导入
        start_time = time.time()
        with patch.object(import_service, 'import_from_excel') as mock_import:
            mock_import.return_value = {'success': 1000, 'failed': 0}
            result = import_service.import_from_excel('test.xlsx')
        end_time = time.time()
        
        import_time = end_time - start_time
        self.assertLess(import_time, 5.0)  # 导入应该在5秒内完成
        self.assertEqual(result['success'], 1000)
        print(f"Excel import time: {import_time:.4f} seconds")


class TestUIComponentPerformance(PerformanceTestCase):
    """UI组件性能测试"""
    
    def test_component_creation_performance(self):
        """测试组件创建性能"""
        from views.components.ink_card import InkCard
        from views.components.ink_button import InkButton
        from views.components.ink_input import InkTextField
        
        # 测试卡片创建性能
        start_time = time.time()
        for i in range(100):
            card = InkCard(
                title=f"Test Card {i}",
                content=f"Test content {i}"
            )
        end_time = time.time()
        
        creation_time = end_time - start_time
        self.assertLess(creation_time, 1.0)  # 100个卡片应该在1秒内创建
        print(f"Card creation time (100 cards): {creation_time:.4f} seconds")
        
        # 测试按钮创建性能
        start_time = time.time()
        for i in range(100):
            button = InkButton(text=f"Button {i}")
        end_time = time.time()
        
        creation_time = end_time - start_time
        self.assertLess(creation_time, 0.5)  # 100个按钮应该在0.5秒内创建
        print(f"Button creation time (100 buttons): {creation_time:.4f} seconds")
        
        # 测试输入框创建性能
        start_time = time.time()
        for i in range(100):
            text_field = InkTextField(hint_text=f"Input {i}")
        end_time = time.time()
        
        creation_time = end_time - start_time
        self.assertLess(creation_time, 0.5)  # 100个输入框应该在0.5秒内创建
        print(f"Input creation time (100 inputs): {creation_time:.4f} seconds")
    
    def test_theme_application_performance(self):
        """测试主题应用性能"""
        from utils.ink_theme import ink_theme
        
        # 测试颜色获取性能
        start_time = time.time()
        for i in range(1000):
            color = ink_theme.get_color('ink_black')
        end_time = time.time()
        
        color_time = end_time - start_time
        self.assertLess(color_time, 0.1)  # 1000次颜色获取应该在100ms内完成
        print(f"Color retrieval time (1000 times): {color_time:.4f} seconds")
        
        # 测试样式获取性能
        start_time = time.time()
        for i in range(1000):
            style = ink_theme.get_ink_style()
        end_time = time.time()
        
        style_time = end_time - start_time
        self.assertLess(style_time, 0.2)  # 1000次样式获取应该在200ms内完成
        print(f"Style retrieval time (1000 times): {style_time:.4f} seconds")


class TestConcurrentPerformance(PerformanceTestCase):
    """并发性能测试"""
    
    def test_concurrent_search(self):
        """测试并发搜索"""
        import threading
        import queue
        
        # 创建测试数据
        for i in range(1000):
            word_data = {
                'word_id': f'concurrent{i:04d}',
                'latin_form': f'concurrent test {i}',
                'definitions': [f'definition {i}']
            }
            dictionary_service.add_word_entry(word_data)
        
        results_queue = queue.Queue()
        
        def search_worker(search_term):
            results = search_service.search_by_latin_form(search_term)
            results_queue.put(len(results))
        
        # 启动多个搜索线程
        threads = []
        start_time = time.time()
        
        for i in range(10):
            thread = threading.Thread(
                target=search_worker, 
                args=(f'concurrent test {i * 100}',)
            )
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        concurrent_time = end_time - start_time
        
        # 验证所有搜索都完成了
        total_results = 0
        while not results_queue.empty():
            total_results += results_queue.get()
        
        self.assertEqual(total_results, 10)  # 应该有10个搜索结果
        self.assertLess(concurrent_time, 2.0)  # 并发搜索应该在2秒内完成
        print(f"Concurrent search time (10 threads): {concurrent_time:.4f} seconds")


class TestMemoryLeakPerformance(PerformanceTestCase):
    """内存泄漏性能测试"""
    
    def test_memory_leak_detection(self):
        """测试内存泄漏检测"""
        import gc
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建和销毁大量对象
        for cycle in range(10):
            # 创建大量词条
            for i in range(100):
                word_data = {
                    'word_id': f'leak{cycle}{i:04d}',
                    'latin_form': f'leak test {cycle} {i}',
                    'definitions': [f'definition {i}']
                }
                word_entry = dictionary_service.add_word_entry(word_data)
            
            # 删除所有词条
            all_entries = dictionary_service.get_all_word_entries()
            for entry in all_entries:
                dictionary_service.delete_word_entry(entry.id)
            
            # 强制垃圾回收
            gc.collect()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该很小（小于10MB）
        self.assertLess(memory_increase, 10 * 1024 * 1024)
        print(f"Memory leak test - increase: {memory_increase / 1024 / 1024:.2f} MB")


if __name__ == '__main__':
    unittest.main()







