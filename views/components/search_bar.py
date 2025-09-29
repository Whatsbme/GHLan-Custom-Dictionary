"""
搜索栏组件
Search Bar Component
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivy.metrics import dp

from utils.logger import get_logger


class SearchBar(MDBoxLayout):
    """搜索栏组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.orientation = 'horizontal'
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(60)
        
        # 搜索配置
        self.search_type = 'all'  # all, word_id, latin_form, phonetic, definitions
        self.case_sensitive = False
        self.fuzzy_search = True
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        # 搜索类型按钮
        self.search_type_btn = MDRaisedButton(
            text="全部",
            size_hint_x=None,
            width=dp(80),
            on_release=self._show_search_type_menu
        )
        self.add_widget(self.search_type_btn)
        
        # 搜索输入框
        self.search_field = MDTextField(
            hint_text="输入搜索关键词",
            mode="rectangle",
            size_hint_x=0.7,
            on_text_validate=self._on_search
        )
        self.add_widget(self.search_field)
        
        # 搜索按钮
        self.search_btn = MDIconButton(
            icon="magnify",
            size_hint_x=None,
            width=dp(48),
            on_release=self._on_search
        )
        self.add_widget(self.search_btn)
        
        # 高级选项按钮
        self.options_btn = MDIconButton(
            icon="tune",
            size_hint_x=None,
            width=dp(48),
            on_release=self._show_options_menu
        )
        self.add_widget(self.options_btn)
    
    def _show_search_type_menu(self, instance):
        """显示搜索类型菜单"""
        menu_items = [
            {
                "text": "全部",
                "on_release": lambda x: self._set_search_type('all', '全部')
            },
            {
                "text": "字序号",
                "on_release": lambda x: self._set_search_type('word_id', '字序号')
            },
            {
                "text": "拉丁写法",
                "on_release": lambda x: self._set_search_type('latin_form', '拉丁写法')
            },
            {
                "text": "音标",
                "on_release": lambda x: self._set_search_type('phonetic', '音标')
            },
            {
                "text": "释义",
                "on_release": lambda x: self._set_search_type('definitions', '释义')
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_search_type(self, search_type, display_text):
        """设置搜索类型"""
        self.search_type = search_type
        self.search_type_btn.text = display_text
        self.logger.info(f"搜索类型已设置为: {display_text}")
    
    def _show_options_menu(self, instance):
        """显示高级选项菜单"""
        menu_items = [
            {
                "text": f"区分大小写: {'开启' if self.case_sensitive else '关闭'}",
                "on_release": lambda x: self._toggle_case_sensitive()
            },
            {
                "text": f"模糊搜索: {'开启' if self.fuzzy_search else '关闭'}",
                "on_release": lambda x: self._toggle_fuzzy_search()
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _toggle_case_sensitive(self):
        """切换区分大小写"""
        self.case_sensitive = not self.case_sensitive
        self.logger.info(f"区分大小写: {'开启' if self.case_sensitive else '关闭'}")
    
    def _toggle_fuzzy_search(self):
        """切换模糊搜索"""
        self.fuzzy_search = not self.fuzzy_search
        self.logger.info(f"模糊搜索: {'开启' if self.fuzzy_search else '关闭'}")
    
    def _on_search(self, instance):
        """执行搜索"""
        query = self.search_field.text.strip()
        if query:
            self.logger.info(f"搜索: {query}, 类型: {self.search_type}")
            # 这里应该触发搜索事件
            self._trigger_search_event(query)
        else:
            self.logger.warning("搜索关键词为空")
    
    def _trigger_search_event(self, query):
        """触发搜索事件"""
        # 这里可以发送事件给父组件
        if hasattr(self.parent, 'on_search'):
            self.parent.on_search(query, self.search_type, self.case_sensitive, self.fuzzy_search)
    
    def get_search_params(self):
        """获取搜索参数"""
        return {
            'query': self.search_field.text.strip(),
            'search_type': self.search_type,
            'case_sensitive': self.case_sensitive,
            'fuzzy_search': self.fuzzy_search
        }
    
    def set_search_text(self, text):
        """设置搜索文本"""
        self.search_field.text = text
    
    def clear_search(self):
        """清除搜索"""
        self.search_field.text = ""
        self.search_type = 'all'
        self.search_type_btn.text = "全部"
        self.case_sensitive = False
        self.fuzzy_search = True
