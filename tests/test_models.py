"""
模型测试
Model Tests
"""

import unittest
from datetime import datetime

from models import WordEntry, Definition, Example, WordImage


class TestWordEntry(unittest.TestCase):
    """词条模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.word_entry = WordEntry(
            word_id="TEST001",
            latin_form="testus",
            phonetic="['testəs]",
            word_type="noun"
        )
    
    def test_word_entry_creation(self):
        """测试词条创建"""
        self.assertEqual(self.word_entry.word_id, "TEST001")
        self.assertEqual(self.word_entry.latin_form, "testus")
        self.assertEqual(self.word_entry.phonetic, "['testəs]")
        self.assertEqual(self.word_entry.word_type, "noun")
    
    def test_word_entry_to_dict(self):
        """测试词条转字典"""
        data = self.word_entry.to_dict()
        self.assertIn('word_id', data)
        self.assertIn('latin_form', data)
        self.assertEqual(data['word_id'], "TEST001")


class TestDefinition(unittest.TestCase):
    """释义模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.definition = Definition(
            word_entry_id=1,
            definition_text="测试释义",
            definition_order=1
        )
    
    def test_definition_creation(self):
        """测试释义创建"""
        self.assertEqual(self.definition.definition_text, "测试释义")
        self.assertEqual(self.definition.definition_order, 1)


class TestExample(unittest.TestCase):
    """例句模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.example = Example(
            word_entry_id=1,
            example_text="这是一个测试例句",
            translation="This is a test example",
            example_order=1
        )
    
    def test_example_creation(self):
        """测试例句创建"""
        self.assertEqual(self.example.example_text, "这是一个测试例句")
        self.assertEqual(self.example.translation, "This is a test example")


if __name__ == '__main__':
    unittest.main()
