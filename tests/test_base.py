"""
测试基础类
Test Base Classes
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from tests import TEST_CONFIG
from app.config import Config
from services.database_service import DatabaseService
from utils.logger import setup_logger


class BaseTestCase(unittest.TestCase):
    """测试基础类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类设置"""
        # 设置测试环境
        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.test_config = Config()
        
        # 使用临时目录
        cls.test_config.config_dir = cls.temp_dir / "test_config"
        cls.test_config.data_dir = cls.temp_dir / "test_data"
        cls.test_config.images_dir = cls.temp_dir / "test_images"
        cls.test_config.exports_dir = cls.temp_dir / "test_exports"
        cls.test_config.imports_dir = cls.temp_dir / "test_imports"
        cls.test_config.database_path = cls.temp_dir / "test.db"
        
        # 创建测试目录
        cls.test_config._create_directories()
        
        # 设置数据库服务
        cls.db_service = DatabaseService()
        cls.db_service.database_path = cls.test_config.database_path
        cls.db_service.create_tables()
        
        # 设置日志
        setup_logger(level=TEST_CONFIG['log_level'])
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        # 清理临时目录
        if cls.temp_dir.exists():
            shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        """每个测试方法前的设置"""
        # 清理数据库
        self.db_service.clear_all_data()
    
    def tearDown(self):
        """每个测试方法后的清理"""
        pass
    
    def create_test_word_entry(self, word_id="test001", latin_form="test"):
        """创建测试词条"""
        from models.word_entry import WordEntry
        
        word_entry = WordEntry(
            word_id=word_id,
            latin_form=latin_form,
            phonetic="test phonetic",
            word_type="noun",
            notes="test notes"
        )
        
        self.db_service.add_object(word_entry)
        return word_entry
    
    def create_test_definition(self, word_entry, definition_text="test definition"):
        """创建测试释义"""
        from models.definition import Definition
        
        definition = Definition(
            word_entry_id=word_entry.id,
            definition_text=definition_text,
            definition_order=1
        )
        
        self.db_service.add_object(definition)
        return definition
    
    def create_test_example(self, word_entry, example_text="test example"):
        """创建测试例句"""
        from models.example import Example
        
        example = Example(
            word_entry_id=word_entry.id,
            example_text=example_text,
            translation="test translation",
            example_order=1
        )
        
        self.db_service.add_object(example)
        return example


class MockTestCase(unittest.TestCase):
    """Mock测试基础类"""
    
    def setUp(self):
        """设置Mock"""
        self.mock_patchers = []
    
    def tearDown(self):
        """清理Mock"""
        for patcher in self.mock_patchers:
            patcher.stop()
    
    def add_patcher(self, patcher):
        """添加Mock patcher"""
        self.mock_patchers.append(patcher)
        return patcher.start()
    
    def patch(self, target, **kwargs):
        """创建Mock patch"""
        patcher = patch(target, **kwargs)
        self.add_patcher(patcher)
        return patcher.start()


class PerformanceTestCase(unittest.TestCase):
    """性能测试基础类"""
    
    def setUp(self):
        """性能测试设置"""
        import time
        self.start_time = time.time()
    
    def tearDown(self):
        """性能测试清理"""
        import time
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time
        print(f"Test execution time: {self.execution_time:.4f} seconds")
    
    def assert_performance(self, max_time):
        """断言性能"""
        self.assertLess(self.execution_time, max_time, 
                       f"Performance test failed: {self.execution_time:.4f}s > {max_time}s")


class UITestCase(unittest.TestCase):
    """UI测试基础类"""
    
    def setUp(self):
        """UI测试设置"""
        from kivy.app import App
        from kivy.clock import Clock
        
        # 创建测试应用
        self.app = App()
        self.app.build = lambda: None
        
        # 设置时钟
        self.clock = Clock
    
    def tearDown(self):
        """UI测试清理"""
        if hasattr(self, 'app'):
            self.app.stop()
    
    def run_ui_test(self, test_func, timeout=1.0):
        """运行UI测试"""
        from kivy.clock import Clock
        
        def timeout_func(dt):
            self.fail("UI test timeout")
        
        # 设置超时
        Clock.schedule_once(timeout_func, timeout)
        
        # 运行测试
        Clock.schedule_once(lambda dt: test_func(), 0.1)
        
        # 运行应用循环
        self.app.run()







