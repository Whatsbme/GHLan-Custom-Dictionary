"""
词条列表界面
Word List Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.progressbar import MDProgressBar
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from .base_screen import BaseScreen
from .components.search_bar import SearchBar
from .components.word_card import WordCard
from utils.logger import get_logger
from services.dictionary_service import dictionary_service
from services.search_service import search_service


class WordListScreen(BaseScreen):
    """词条列表界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.word_entries = []
        self.current_page = 0
        self.page_size = 20
        self.sort_by = 'word_id'
        self.sort_order = 'asc'
        self.filter_favorites = False
        self.current_search_query = ""
        
        self._setup_ui()
        self._load_word_entries()
    
    def get_screen_title(self) -> str:
        return "词条列表"
    
    def _setup_ui(self):
        """设置UI"""
        # 主布局
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(16)
        )
        
        # 搜索栏
        self.search_bar = SearchBar()
        main_layout.add_widget(self.search_bar)
        
        # 工具栏
        toolbar_card = MDCard(
            size_hint_y=None,
            height=dp(60),
            padding=dp(16),
            radius=[10, 10, 10, 10]
        )
        
        toolbar_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        # 排序按钮
        self.sort_btn = MDRaisedButton(
            text="排序: 字序号 ↑",
            size_hint_x=None,
            width=dp(120),
            on_release=self._show_sort_menu
        )
        toolbar_layout.add_widget(self.sort_btn)
        
        # 筛选按钮
        self.filter_btn = MDRaisedButton(
            text="全部",
            size_hint_x=None,
            width=dp(80),
            on_release=self._show_filter_menu
        )
        toolbar_layout.add_widget(self.filter_btn)
        
        # 统计信息
        self.stats_label = MDLabel(
            text="共 0 条词条",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=0.5
        )
        toolbar_layout.add_widget(self.stats_label)
        
        # 刷新按钮
        self.refresh_btn = MDRaisedButton(
            text="刷新",
            size_hint_x=None,
            width=dp(80),
            on_release=self._refresh_list
        )
        toolbar_layout.add_widget(self.refresh_btn)
        
        toolbar_card.add_widget(toolbar_layout)
        main_layout.add_widget(toolbar_card)
        
        # 词条列表区域
        self.list_scroll = MDScrollView()
        self.list_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.list_container.bind(minimum_height=self.list_container.setter('height'))
        
        self.list_scroll.add_widget(self.list_container)
        main_layout.add_widget(self.list_scroll)
        
        # 分页控件
        self.pagination_card = MDCard(
            size_hint_y=None,
            height=dp(60),
            padding=dp(16),
            radius=[10, 10, 10, 10]
        )
        
        pagination_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        # 上一页按钮
        self.prev_btn = MDRaisedButton(
            text="上一页",
            size_hint_x=0.3,
            on_release=self._prev_page
        )
        pagination_layout.add_widget(self.prev_btn)
        
        # 页码信息
        self.page_label = MDLabel(
            text="第 1 页",
            theme_text_color="Primary",
            font_style="Body1",
            halign="center",
            size_hint_x=0.4
        )
        pagination_layout.add_widget(self.page_label)
        
        # 下一页按钮
        self.next_btn = MDRaisedButton(
            text="下一页",
            size_hint_x=0.3,
            on_release=self._next_page
        )
        pagination_layout.add_widget(self.next_btn)
        
        self.pagination_card.add_widget(pagination_layout)
        main_layout.add_widget(self.pagination_card)
        
        # 添加词条按钮
        self.add_fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self._add_word
        )
        main_layout.add_widget(self.add_fab)
        
        self.content_layout.add_widget(main_layout)
    
    def _show_sort_menu(self, instance):
        """显示排序菜单"""
        menu_items = [
            {
                "text": "字序号 ↑",
                "on_release": lambda x: self._set_sort('word_id', 'asc')
            },
            {
                "text": "字序号 ↓",
                "on_release": lambda x: self._set_sort('word_id', 'desc')
            },
            {
                "text": "拉丁写法 ↑",
                "on_release": lambda x: self._set_sort('latin_form', 'asc')
            },
            {
                "text": "拉丁写法 ↓",
                "on_release": lambda x: self._set_sort('latin_form', 'desc')
            },
            {
                "text": "创建时间 ↑",
                "on_release": lambda x: self._set_sort('created_at', 'asc')
            },
            {
                "text": "创建时间 ↓",
                "on_release": lambda x: self._set_sort('created_at', 'desc')
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_sort(self, sort_by, sort_order):
        """设置排序"""
        self.sort_by = sort_by
        self.sort_order = sort_order
        
        # 更新按钮文本
        order_symbol = "↑" if sort_order == 'asc' else "↓"
        sort_names = {
            'word_id': '字序号',
            'latin_form': '拉丁写法',
            'created_at': '创建时间'
        }
        self.sort_btn.text = f"排序: {sort_names[sort_by]} {order_symbol}"
        
        self._refresh_list()
        self.logger.info(f"排序已设置为: {sort_by} {sort_order}")
    
    def _show_filter_menu(self, instance):
        """显示筛选菜单"""
        menu_items = [
            {
                "text": "全部",
                "on_release": lambda x: self._set_filter(False)
            },
            {
                "text": "仅收藏",
                "on_release": lambda x: self._set_filter(True)
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_filter(self, favorites_only):
        """设置筛选"""
        self.filter_favorites = favorites_only
        self.filter_btn.text = "仅收藏" if favorites_only else "全部"
        self.current_page = 0  # 重置页码
        self._refresh_list()
        self.logger.info(f"筛选已设置为: {'仅收藏' if favorites_only else '全部'}")
    
    def _load_word_entries(self):
        """加载词条列表"""
        try:
            if self.current_search_query:
                # 执行搜索
                self.word_entries = search_service.search_words(
                    self.current_search_query,
                    search_type=self.search_bar.search_type,
                    case_sensitive=self.search_bar.case_sensitive,
                    fuzzy=self.search_bar.fuzzy_search
                )
            else:
                # 加载所有词条
                if self.filter_favorites:
                    self.word_entries = dictionary_service.get_favorite_word_entries()
                else:
                    self.word_entries = dictionary_service.get_all_word_entries(
                        limit=1000,  # 获取所有词条
                        sort_by=self.sort_by,
                        order=self.sort_order
                    )
            
            self._update_display()
            self.logger.info(f"加载了 {len(self.word_entries)} 条词条")
            
        except Exception as e:
            self.logger.error(f"加载词条列表失败: {e}")
            self.show_snackbar("加载词条列表失败")
    
    def _update_display(self):
        """更新显示"""
        # 清空列表
        self.list_container.clear_widgets()
        
        # 计算分页
        total_entries = len(self.word_entries)
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, total_entries)
        
        # 显示当前页的词条
        for i in range(start_idx, end_idx):
            word_entry = self.word_entries[i]
            word_card = WordCard(word_entry=word_entry)
            self.list_container.add_widget(word_card)
        
        # 更新统计信息
        self.stats_label.text = f"共 {total_entries} 条词条"
        
        # 更新分页信息
        total_pages = (total_entries + self.page_size - 1) // self.page_size
        self.page_label.text = f"第 {self.current_page + 1} 页 / 共 {total_pages} 页"
        
        # 更新分页按钮状态
        self.prev_btn.disabled = self.current_page == 0
        self.next_btn.disabled = self.current_page >= total_pages - 1
    
    def _prev_page(self, instance):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_display()
    
    def _next_page(self, instance):
        """下一页"""
        total_entries = len(self.word_entries)
        total_pages = (total_entries + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._update_display()
    
    def _refresh_list(self, instance=None):
        """刷新列表"""
        self.current_page = 0
        self._load_word_entries()
    
    def _add_word(self, instance):
        """添加词条"""
        self.logger.info("导航到添加词条界面")
        # 这里应该导航到添加词条界面
        self.show_snackbar("添加词条功能开发中...")
    
    def on_search(self, query, search_type, case_sensitive, fuzzy_search):
        """处理搜索事件"""
        self.current_search_query = query
        self.current_page = 0
        self._load_word_entries()
    
    def refresh_data(self):
        """刷新数据"""
        self._refresh_list()

