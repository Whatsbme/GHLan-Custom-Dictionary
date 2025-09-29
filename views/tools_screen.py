"""
工具界面
Tools Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp

from .base_screen import BaseScreen
from utils.logger import get_logger


class ToolsScreen(BaseScreen):
    """工具界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self._setup_ui()
    
    def get_screen_title(self) -> str:
        return "工具"
    
    def _setup_ui(self):
        """设置UI"""
        # 主滚动视图
        self.scroll_view = MDScrollView()
        
        # 主容器
        self.main_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None
        )
        self.main_container.bind(minimum_height=self.main_container.setter('height'))
        
        # 网址收藏卡片
        self.url_bookmark_card = self._create_url_bookmark_card()
        self.main_container.add_widget(self.url_bookmark_card)
        
        # 备忘词条卡片
        self.memo_words_card = self._create_memo_words_card()
        self.main_container.add_widget(self.memo_words_card)
        
        # IDS符号编辑器卡片
        self.ids_editor_card = self._create_ids_editor_card()
        self.main_container.add_widget(self.ids_editor_card)
        
        # 其他工具卡片
        self.other_tools_card = self._create_other_tools_card()
        self.main_container.add_widget(self.other_tools_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
    
    def _create_url_bookmark_card(self):
        """创建网址收藏卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="网址收藏管理",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 描述
        description = MDLabel(
            text="管理收藏的网址，支持分类和快速访问",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        layout.add_widget(description)
        
        # 功能按钮
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        view_bookmarks_btn = MDRaisedButton(
            text="查看收藏",
            size_hint_x=0.5,
            on_release=self._show_url_bookmarks
        )
        buttons_layout.add_widget(view_bookmarks_btn)
        
        add_bookmark_btn = MDRaisedButton(
            text="添加收藏",
            size_hint_x=0.5,
            on_release=self._add_url_bookmark
        )
        buttons_layout.add_widget(add_bookmark_btn)
        
        layout.add_widget(buttons_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_memo_words_card(self):
        """创建备忘词条卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="备忘词条",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 描述
        description = MDLabel(
            text="管理临时备忘的词条，支持快速添加和查看",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        layout.add_widget(description)
        
        # 功能按钮
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        view_memos_btn = MDRaisedButton(
            text="查看备忘",
            size_hint_x=0.5,
            on_release=self._show_memo_words
        )
        buttons_layout.add_widget(view_memos_btn)
        
        add_memo_btn = MDRaisedButton(
            text="添加备忘",
            size_hint_x=0.5,
            on_release=self._add_memo_word
        )
        buttons_layout.add_widget(add_memo_btn)
        
        layout.add_widget(buttons_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_ids_editor_card(self):
        """创建IDS符号编辑器卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="IDS符号编辑器",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 描述
        description = MDLabel(
            text="编辑和创建IDS（Ideographic Description Sequence）符号，支持导出为图片",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        layout.add_widget(description)
        
        # 功能按钮
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        open_editor_btn = MDRaisedButton(
            text="打开编辑器",
            size_hint_x=0.5,
            on_release=self._open_ids_editor
        )
        buttons_layout.add_widget(open_editor_btn)
        
        view_templates_btn = MDRaisedButton(
            text="查看模板",
            size_hint_x=0.5,
            on_release=self._view_ids_templates
        )
        buttons_layout.add_widget(view_templates_btn)
        
        layout.add_widget(buttons_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_other_tools_card(self):
        """创建其他工具卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="其他工具",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 功能按钮网格
        buttons_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        
        # 数据备份
        backup_btn = MDRaisedButton(
            text="数据备份",
            on_release=self._backup_data
        )
        buttons_grid.add_widget(backup_btn)
        
        # 数据恢复
        restore_btn = MDRaisedButton(
            text="数据恢复",
            on_release=self._restore_data
        )
        buttons_grid.add_widget(restore_btn)
        
        # 统计信息
        stats_btn = MDRaisedButton(
            text="统计信息",
            on_release=self._show_statistics
        )
        buttons_grid.add_widget(stats_btn)
        
        # 清理工具
        cleanup_btn = MDRaisedButton(
            text="清理工具",
            on_release=self._cleanup_tools
        )
        buttons_grid.add_widget(cleanup_btn)
        
        layout.add_widget(buttons_grid)
        
        card.add_widget(layout)
        return card
    
    def _show_url_bookmarks(self, instance):
        """显示网址收藏界面"""
        try:
            from .url_bookmark_screen import UrlBookmarkScreen
            bookmark_screen = UrlBookmarkScreen(name="url_bookmarks")
            self.screen_manager.add_widget(bookmark_screen)
            self.screen_manager.current = "url_bookmarks"
        except Exception as e:
            self.logger.error(f"显示网址收藏界面失败: {e}")
            self.show_snackbar("网址收藏界面加载失败")
    
    def _add_url_bookmark(self, instance):
        """添加网址收藏"""
        try:
            from .url_bookmark_screen import UrlBookmarkScreen
            bookmark_screen = UrlBookmarkScreen(name="add_bookmark")
            self.screen_manager.add_widget(bookmark_screen)
            self.screen_manager.current = "add_bookmark"
        except Exception as e:
            self.logger.error(f"添加网址收藏失败: {e}")
            self.show_snackbar("添加网址收藏失败")
    
    def _show_memo_words(self, instance):
        """显示备忘词条界面"""
        try:
            from .memo_words_screen import MemoWordsScreen
            memo_screen = MemoWordsScreen(name="memo_words")
            self.screen_manager.add_widget(memo_screen)
            self.screen_manager.current = "memo_words"
        except Exception as e:
            self.logger.error(f"显示备忘词条界面失败: {e}")
            self.show_snackbar("备忘词条界面加载失败")
    
    def _add_memo_word(self, instance):
        """添加备忘词条"""
        try:
            from .memo_words_screen import MemoWordsScreen
            memo_screen = MemoWordsScreen(name="add_memo")
            self.screen_manager.add_widget(memo_screen)
            self.screen_manager.current = "add_memo"
        except Exception as e:
            self.logger.error(f"添加备忘词条失败: {e}")
            self.show_snackbar("添加备忘词条失败")
    
    def _open_ids_editor(self, instance):
        """打开IDS符号编辑器"""
        try:
            from .ids_editor_screen import IdsEditorScreen
            ids_screen = IdsEditorScreen(name="ids_editor")
            self.screen_manager.add_widget(ids_screen)
            self.screen_manager.current = "ids_editor"
        except Exception as e:
            self.logger.error(f"打开IDS编辑器失败: {e}")
            self.show_snackbar("IDS编辑器加载失败")
    
    def _view_ids_templates(self, instance):
        """查看IDS模板"""
        self.show_snackbar("IDS模板功能开发中...")
    
    def _backup_data(self, instance):
        """数据备份"""
        self.show_snackbar("数据备份功能开发中...")
    
    def _restore_data(self, instance):
        """数据恢复"""
        self.show_snackbar("数据恢复功能开发中...")
    
    def _show_statistics(self, instance):
        """显示统计信息"""
        self.show_snackbar("统计信息功能开发中...")
    
    def _cleanup_tools(self, instance):
        """清理工具"""
        self.show_snackbar("清理工具功能开发中...")
    
    def refresh_data(self):
        """刷新数据"""
        pass
