"""
服务测试
Service Tests
"""

import unittest
import tempfile
import os
from pathlib import Path

from services.dictionary_service import DictionaryService
from services.search_service import SearchService
from utils.validators import Validators


class TestDictionaryService(unittest.TestCase):
    """词典服务测试"""
    
    def setUp(self):
        """测试前准备"""
        self.dictionary_service = DictionaryService()
    
    def test_add_word_entry(self):
        """测试添加词条"""
        word_data = {
            'word_id': 'TEST001',
            'latin_form': 'testus',
            'phonetic': "['testəs]",
            'word_type': 'noun',
            'definitions': ['测试释义1', '测试释义2'],
            'examples': [
                {'text': '测试例句1', 'translation': 'Test example 1'},
                {'text': '测试例句2', 'translation': 'Test example 2'}
            ]
        }
        
        # 注意：实际测试需要数据库连接
        # result = self.dictionary_service.add_word_entry(word_data)
        # self.assertIsNotNone(result)
    
    def test_get_word_count(self):
        """测试获取词条数量"""
        # 注意：实际测试需要数据库连接
        # count = self.dictionary_service.get_word_count()
        # self.assertIsInstance(count, int)
        pass


class TestSearchService(unittest.TestCase):
    """搜索服务测试"""
    
    def setUp(self):
        """测试前准备"""
        self.search_service = SearchService()
    
    def test_search_suggestions(self):
        """测试搜索建议"""
        # 注意：实际测试需要数据库连接
        # suggestions = self.search_service.get_search_suggestions("test")
        # self.assertIsInstance(suggestions, list)
        pass


class TestValidators(unittest.TestCase):
    """验证器测试"""
    
    def test_validate_word_id(self):
        """测试字序号验证"""
        # 有效字序号
        result = Validators.validate_word_id("TEST001")
        self.assertTrue(result['valid'])
        
        # 无效字序号
        result = Validators.validate_word_id("")
        self.assertFalse(result['valid'])
        self.assertIn('字序号不能为空', result['errors'])
    
    def test_validate_latin_form(self):
        """测试拉丁写法验证"""
        # 有效拉丁写法
        result = Validators.validate_latin_form("testus")
        self.assertTrue(result['valid'])
        
        # 无效拉丁写法
        result = Validators.validate_latin_form("")
        self.assertFalse(result['valid'])
        self.assertIn('拉丁写法不能为空', result['errors'])
    
    def test_validate_definitions(self):
        """测试释义验证"""
        # 有效释义
        result = Validators.validate_definitions(['释义1', '释义2'])
        self.assertTrue(result['valid'])
        
        # 无效释义
        result = Validators.validate_definitions([])
        self.assertFalse(result['valid'])
        self.assertIn('至少需要一个释义', result['errors'])
    
    def test_validate_url(self):
        """测试URL验证"""
        # 有效URL
        result = Validators.validate_url("https://www.example.com")
        self.assertTrue(result['valid'])
        
        # 无效URL
        result = Validators.validate_url("invalid-url")
        self.assertFalse(result['valid'])
        self.assertIn('URL格式不正确', result['errors'])


if __name__ == '__main__':
    unittest.main()
