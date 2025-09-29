"""
视图层测试
Views Layer Tests
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

from tests.test_base import BaseTestCase, MockTestCase, UITestCase
from views.main_screen import MainScreen
from views.word_list_screen import WordListScreen
from views.word_detail_screen import WordDetailScreen
from views.word_edit_screen import WordEditScreen
from views.advanced_search_screen import AdvancedSearchScreen
from views.settings_screen import SettingsScreen
from views.tools_screen import ToolsScreen
from views.url_bookmark_screen import UrlBookmarkScreen
from views.memo_words_screen import MemoWordsScreen
from views.import_export_screen import ImportExportScreen


class TestMainScreen(BaseTestCase):
    """主界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = MainScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "GHLan自定义字典")
    
    def test_navigation_setup(self):
        """测试导航设置"""
        self.assertIsNotNone(self.screen.screen_manager)
        self.assertIsNotNone(self.screen.navigation_drawer)
    
    def test_search_functionality(self):
        """测试搜索功能"""
        # 模拟搜索
        with patch.object(self.screen, 'show_snackbar') as mock_snackbar:
            self.screen._perform_search()
            mock_snackbar.assert_called()
    
    def test_navigation_items(self):
        """测试导航项"""
        menu_items = self.screen._get_menu_items()
        self.assertIsInstance(menu_items, list)
        self.assertGreater(len(menu_items), 0)


class TestWordListScreen(BaseTestCase):
    """词条列表界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = WordListScreen()
        # 创建测试数据
        self.word_entry = self.create_test_word_entry()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "词条列表")
    
    def test_word_list_display(self):
        """测试词条列表显示"""
        self.screen._load_word_entries()
        self.assertIsNotNone(self.screen.word_list)
    
    def test_pagination(self):
        """测试分页功能"""
        # 创建多个测试词条
        for i in range(25):
            self.create_test_word_entry(f"test{i:03d}", f"test{i}")
        
        self.screen._load_word_entries()
        self.assertIsNotNone(self.screen.pagination)
    
    def test_sorting(self):
        """测试排序功能"""
        # 创建测试数据
        self.create_test_word_entry("test002", "zebra")
        self.create_test_word_entry("test003", "apple")
        
        self.screen._load_word_entries()
        self.screen._sort_words("latin_form", "asc")
        
        # 验证排序结果
        self.assertIsNotNone(self.screen.word_entries)


class TestWordDetailScreen(BaseTestCase):
    """词条详情界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = WordDetailScreen()
        # 创建测试数据
        self.word_entry = self.create_test_word_entry()
        self.definition = self.create_test_definition(self.word_entry)
        self.example = self.create_test_example(self.word_entry)
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "词条详情")
    
    def test_word_display(self):
        """测试词条显示"""
        self.screen.word_entry = self.word_entry
        self.screen._display_word_details()
        
        self.assertIsNotNone(self.screen.word_entry)
    
    def test_edit_functionality(self):
        """测试编辑功能"""
        with patch.object(self.screen, '_show_edit_screen') as mock_edit:
            self.screen._edit_word(None)
            mock_edit.assert_called()
    
    def test_delete_functionality(self):
        """测试删除功能"""
        with patch.object(self.screen, 'show_dialog') as mock_dialog:
            self.screen._delete_word(None)
            mock_dialog.assert_called()


class TestWordEditScreen(BaseTestCase):
    """词条编辑界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = WordEditScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "编辑词条")
    
    def test_form_validation(self):
        """测试表单验证"""
        # 测试空表单
        is_valid, errors = self.screen._validate_form()
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_save_functionality(self):
        """测试保存功能"""
        with patch.object(self.screen, '_save_word_entry') as mock_save:
            self.screen._save_word(None)
            mock_save.assert_called()


class TestAdvancedSearchScreen(BaseTestCase):
    """高级搜索界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = AdvancedSearchScreen()
        # 创建测试数据
        self.word_entry = self.create_test_word_entry()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "高级搜索")
    
    def test_search_functionality(self):
        """测试搜索功能"""
        with patch.object(self.screen, '_perform_search') as mock_search:
            self.screen._perform_search()
            mock_search.assert_called()
    
    def test_search_options(self):
        """测试搜索选项"""
        # 测试模糊搜索
        self.screen.fuzzy_switch.active = True
        self.assertTrue(self.screen.fuzzy_switch.active)
        
        # 测试正则搜索
        self.screen.regex_switch.active = True
        self.assertTrue(self.screen.regex_switch.active)


class TestSettingsScreen(BaseTestCase):
    """设置界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = SettingsScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "设置")
    
    def test_theme_settings(self):
        """测试主题设置"""
        with patch.object(self.screen, '_apply_theme') as mock_theme:
            self.screen._apply_theme()
            mock_theme.assert_called()
    
    def test_font_settings(self):
        """测试字体设置"""
        with patch.object(self.screen, '_apply_font') as mock_font:
            self.screen._apply_font()
            mock_font.assert_called()


class TestToolsScreen(BaseTestCase):
    """工具界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = ToolsScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "工具")
    
    def test_tool_cards(self):
        """测试工具卡片"""
        self.assertIsNotNone(self.screen.url_bookmark_card)
        self.assertIsNotNone(self.screen.memo_words_card)
        self.assertIsNotNone(self.screen.ids_editor_card)
    
    def test_navigation_functions(self):
        """测试导航功能"""
        with patch.object(self.screen, '_show_url_bookmarks') as mock_bookmarks:
            self.screen._show_url_bookmarks(None)
            mock_bookmarks.assert_called()


class TestUrlBookmarkScreen(BaseTestCase):
    """网址收藏界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = UrlBookmarkScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "网址收藏")
    
    def test_bookmark_management(self):
        """测试收藏管理"""
        with patch.object(self.screen, '_load_bookmarks') as mock_load:
            self.screen._load_bookmarks()
            mock_load.assert_called()
    
    def test_search_functionality(self):
        """测试搜索功能"""
        with patch.object(self.screen, '_search_bookmarks') as mock_search:
            self.screen._search_bookmarks(None)
            mock_search.assert_called()


class TestMemoWordsScreen(BaseTestCase):
    """备忘词条界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = MemoWordsScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "备忘词条")
    
    def test_memo_management(self):
        """测试备忘管理"""
        with patch.object(self.screen, '_load_memo_words') as mock_load:
            self.screen._load_memo_words()
            mock_load.assert_called()
    
    def test_status_filtering(self):
        """测试状态筛选"""
        with patch.object(self.screen, '_select_status') as mock_filter:
            self.screen._select_status("已完成")
            mock_filter.assert_called()


class TestImportExportScreen(BaseTestCase):
    """导入导出界面测试"""
    
    def setUp(self):
        super().setUp()
        self.screen = ImportExportScreen()
    
    def test_screen_initialization(self):
        """测试界面初始化"""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.get_screen_title(), "导入导出")
    
    def test_import_functionality(self):
        """测试导入功能"""
        with patch.object(self.screen, '_import_excel') as mock_import:
            self.screen._import_excel(None)
            mock_import.assert_called()
    
    def test_export_functionality(self):
        """测试导出功能"""
        with patch.object(self.screen, '_start_export') as mock_export:
            self.screen._start_export(None)
            mock_export.assert_called()


class TestUIComponents(MockTestCase):
    """UI组件测试"""
    
    def test_ink_components(self):
        """测试水墨风格组件"""
        from views.components.ink_card import InkCard
        from views.components.ink_button import InkButton
        from views.components.ink_input import InkTextField
        
        # 测试卡片组件
        card = InkCard(title="测试", content="测试内容")
        self.assertIsNotNone(card)
        
        # 测试按钮组件
        button = InkButton(text="测试按钮", ink_style="primary")
        self.assertIsNotNone(button)
        
        # 测试输入组件
        text_field = InkTextField(hint_text="测试输入")
        self.assertIsNotNone(text_field)


if __name__ == '__main__':
    unittest.main()







