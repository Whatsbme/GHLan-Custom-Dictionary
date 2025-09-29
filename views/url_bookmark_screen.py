"""
网址收藏管理界面
URL Bookmark Management Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock
import webbrowser
from datetime import datetime

from .base_screen import BaseScreen
from utils.logger import get_logger
from services.bookmark_service import bookmark_service


class UrlBookmarkScreen(BaseScreen):
    """网址收藏管理界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.bookmarks = []
        self.current_category = "全部"
        self.search_query = ""
        
        self._setup_ui()
        self._load_bookmarks()
    
    def get_screen_title(self) -> str:
        return "网址收藏"
    
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
        
        # 搜索和筛选卡片
        self.search_card = self._create_search_card()
        self.main_container.add_widget(self.search_card)
        
        # 收藏列表卡片
        self.bookmarks_card = self._create_bookmarks_card()
        self.main_container.add_widget(self.bookmarks_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 浮动添加按钮
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            on_release=self._show_add_bookmark_dialog
        )
        self.content_layout.add_widget(self.fab)
    
    def _create_search_card(self):
        """创建搜索卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 搜索框
        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.search_field = MDTextField(
            hint_text="搜索网址或标题...",
            mode="rectangle",
            size_hint_x=0.7,
            on_text_validate=self._search_bookmarks
        )
        search_layout.add_widget(self.search_field)
        
        search_btn = MDRaisedButton(
            text="搜索",
            size_hint_x=0.3,
            on_release=self._search_bookmarks
        )
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # 分类筛选
        filter_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        category_label = MDLabel(
            text="分类:",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.2
        )
        filter_layout.add_widget(category_label)
        
        self.category_btn = MDRaisedButton(
            text=self.current_category,
            size_hint_x=0.8,
            on_release=self._show_category_menu
        )
        filter_layout.add_widget(self.category_btn)
        
        layout.add_widget(filter_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_bookmarks_card(self):
        """创建收藏列表卡片"""
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
            text="收藏列表",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 收藏列表
        self.bookmarks_list = MDList()
        layout.add_widget(self.bookmarks_list)
        
        card.add_widget(layout)
        return card
    
    def _load_bookmarks(self):
        """加载收藏列表"""
        try:
            self.bookmarks = bookmark_service.get_all_bookmarks()
            self._update_bookmarks_display()
        except Exception as e:
            self.logger.error(f"加载收藏列表失败: {e}")
            self.show_snackbar("加载收藏列表失败")
    
    def _update_bookmarks_display(self):
        """更新收藏显示"""
        self.bookmarks_list.clear_widgets()
        
        # 筛选收藏
        filtered_bookmarks = self._filter_bookmarks()
        
        if not filtered_bookmarks:
            empty_item = OneLineListItem(
                text="暂无收藏",
                theme_text_color="Secondary"
            )
            self.bookmarks_list.add_widget(empty_item)
            return
        
        for bookmark in filtered_bookmarks:
            item = TwoLineListItem(
                text=bookmark.title,
                secondary_text=f"{bookmark.url} | {bookmark.category}",
                on_release=lambda x, b=bookmark: self._open_bookmark(b)
            )
            
            # 添加操作按钮
            item.add_widget(
                MDIconButton(
                    icon="pencil",
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, b=bookmark: self._edit_bookmark(b)
                )
            )
            
            item.add_widget(
                MDIconButton(
                    icon="delete",
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, b=bookmark: self._delete_bookmark(b)
                )
            )
            
            self.bookmarks_list.add_widget(item)
    
    def _filter_bookmarks(self):
        """筛选收藏"""
        filtered = self.bookmarks
        
        # 按分类筛选
        if self.current_category != "全部":
            filtered = [b for b in filtered if b.category == self.current_category]
        
        # 按搜索词筛选
        if self.search_query:
            query = self.search_query.lower()
            filtered = [b for b in filtered if 
                       query in b.title.lower() or 
                       query in b.url.lower() or 
                       query in (b.description or "").lower()]
        
        return filtered
    
    def _search_bookmarks(self, instance):
        """搜索收藏"""
        self.search_query = self.search_field.text
        self._update_bookmarks_display()
    
    def _show_category_menu(self, instance):
        """显示分类菜单"""
        categories = ["全部"] + list(set([b.category for b in self.bookmarks]))
        
        menu_items = []
        for category in categories:
            menu_items.append({
                "text": category,
                "on_release": lambda x, c=category: self._select_category(c)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _select_category(self, category):
        """选择分类"""
        self.current_category = category
        self.category_btn.text = category
        self._update_bookmarks_display()
    
    def _open_bookmark(self, bookmark):
        """打开收藏"""
        try:
            webbrowser.open(bookmark.url)
            self.logger.info(f"打开网址: {bookmark.url}")
        except Exception as e:
            self.logger.error(f"打开网址失败: {e}")
            self.show_snackbar("打开网址失败")
    
    def _edit_bookmark(self, bookmark):
        """编辑收藏"""
        self._show_edit_bookmark_dialog(bookmark)
    
    def _delete_bookmark(self, bookmark):
        """删除收藏"""
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="确认删除",
            text=f"确定要删除收藏 '{bookmark.title}' 吗？",
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="删除",
                    on_release=lambda x: self._confirm_delete_bookmark(dialog, bookmark)
                )
            ]
        )
        dialog.open()
    
    def _confirm_delete_bookmark(self, dialog, bookmark):
        """确认删除收藏"""
        try:
            bookmark_service.delete_bookmark(bookmark.id)
            dialog.dismiss()
            self._load_bookmarks()
            self.show_snackbar("收藏已删除")
        except Exception as e:
            self.logger.error(f"删除收藏失败: {e}")
            self.show_snackbar("删除收藏失败")
    
    def _show_add_bookmark_dialog(self, instance):
        """显示添加收藏对话框"""
        self._show_bookmark_dialog()
    
    def _show_edit_bookmark_dialog(self, bookmark):
        """显示编辑收藏对话框"""
        self._show_bookmark_dialog(bookmark)
    
    def _show_bookmark_dialog(self, bookmark=None):
        """显示收藏对话框"""
        # 创建表单
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(300)
        )
        
        # 标题
        title_field = MDTextField(
            hint_text="标题",
            mode="rectangle",
            text=bookmark.title if bookmark else ""
        )
        form_layout.add_widget(title_field)
        
        # 网址
        url_field = MDTextField(
            hint_text="网址",
            mode="rectangle",
            text=bookmark.url if bookmark else ""
        )
        form_layout.add_widget(url_field)
        
        # 分类
        category_field = MDTextField(
            hint_text="分类",
            mode="rectangle",
            text=bookmark.category if bookmark else ""
        )
        form_layout.add_widget(category_field)
        
        # 描述
        description_field = MDTextField(
            hint_text="描述",
            mode="rectangle",
            multiline=True,
            text=bookmark.description if bookmark else ""
        )
        form_layout.add_widget(description_field)
        
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="添加收藏" if not bookmark else "编辑收藏",
            type="custom",
            content_cls=form_layout,
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="保存",
                    on_release=lambda x: self._save_bookmark(dialog, title_field, url_field, category_field, description_field, bookmark)
                )
            ]
        )
        dialog.open()
    
    def _save_bookmark(self, dialog, title_field, url_field, category_field, description_field, bookmark=None):
        """保存收藏"""
        try:
            title = title_field.text.strip()
            url = url_field.text.strip()
            category = category_field.text.strip()
            description = description_field.text.strip()
            
            if not title or not url:
                self.show_snackbar("标题和网址不能为空")
                return
            
            if bookmark:
                # 编辑收藏
                bookmark.title = title
                bookmark.url = url
                bookmark.category = category
                bookmark.description = description
                bookmark.updated_at = datetime.now()
                bookmark_service.update_bookmark(bookmark)
                self.show_snackbar("收藏已更新")
            else:
                # 添加收藏
                bookmark_data = {
                    'title': title,
                    'url': url,
                    'category': category,
                    'description': description
                }
                bookmark_service.add_bookmark(bookmark_data)
                self.show_snackbar("收藏已添加")
            
            dialog.dismiss()
            self._load_bookmarks()
            
        except Exception as e:
            self.logger.error(f"保存收藏失败: {e}")
            self.show_snackbar("保存收藏失败")
    
    def refresh_data(self):
        """刷新数据"""
        self._load_bookmarks()
