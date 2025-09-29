"""
高级搜索界面
Advanced Search Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, OneLineListItem
from kivy.metrics import dp

from .base_screen import BaseScreen
from .components.search_bar import SearchBar
from .components.word_card import WordCard
from utils.logger import get_logger
from services.search_service import search_service
from services.dictionary_service import dictionary_service


class AdvancedSearchScreen(BaseScreen):
    """高级搜索界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.search_results = []
        self.current_search_params = {}
        self.search_history = []
        
        self._setup_ui()
    
    def get_screen_title(self) -> str:
        return "高级搜索"
    
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
        
        # 快速搜索栏
        self.quick_search_card = self._create_quick_search_card()
        self.main_container.add_widget(self.quick_search_card)
        
        # 高级搜索选项
        self.advanced_options_card = self._create_advanced_options_card()
        self.main_container.add_widget(self.advanced_options_card)
        
        # 搜索历史
        self.history_card = self._create_history_card()
        self.main_container.add_widget(self.history_card)
        
        # 搜索结果
        self.results_card = self._create_results_card()
        self.main_container.add_widget(self.results_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 搜索按钮
        self.search_fab = MDFloatingActionButton(
            icon="magnify",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self._perform_search
        )
        self.content_layout.add_widget(self.search_fab)
    
    def _create_quick_search_card(self):
        """创建快速搜索卡片"""
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
            text="快速搜索",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 搜索栏
        self.search_bar = SearchBar()
        layout.add_widget(self.search_bar)
        
        card.add_widget(layout)
        return card
    
    def _create_advanced_options_card(self):
        """创建高级选项卡片"""
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
            text="高级搜索选项",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 多字段搜索选项
        fields_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        fields_title = MDLabel(
            text="搜索字段",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        fields_layout.add_widget(fields_title)
        
        # 字段选择开关
        self.field_switches = {}
        field_options = [
            ('word_id', '字序号'),
            ('latin_form', '拉丁写法'),
            ('phonetic', '音标'),
            ('definitions', '释义'),
            ('examples', '例句')
        ]
        
        for field_key, field_name in field_options:
            field_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(40)
            )
            
            field_label = MDLabel(
                text=field_name,
                theme_text_color="Primary",
                font_style="Body1",
                size_hint_x=0.7
            )
            field_layout.add_widget(field_label)
            
            field_switch = MDSwitch(
                active=True,
                size_hint_x=0.3
            )
            self.field_switches[field_key] = field_switch
            field_layout.add_widget(field_switch)
            
            fields_layout.add_widget(field_layout)
        
        layout.add_widget(fields_layout)
        
        # 搜索模式选项
        mode_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        mode_title = MDLabel(
            text="搜索模式",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        mode_layout.add_widget(mode_title)
        
        # 搜索模式选择
        self.search_mode = 'fuzzy'  # fuzzy, regex, exact
        
        mode_buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        self.fuzzy_btn = MDRaisedButton(
            text="模糊搜索",
            size_hint_x=0.33,
            on_release=lambda x: self._set_search_mode('fuzzy')
        )
        mode_buttons_layout.add_widget(self.fuzzy_btn)
        
        self.regex_btn = MDRaisedButton(
            text="正则表达式",
            size_hint_x=0.33,
            on_release=lambda x: self._set_search_mode('regex')
        )
        mode_buttons_layout.add_widget(self.regex_btn)
        
        self.exact_btn = MDRaisedButton(
            text="精确匹配",
            size_hint_x=0.33,
            on_release=lambda x: self._set_search_mode('exact')
        )
        mode_buttons_layout.add_widget(self.exact_btn)
        
        mode_layout.add_widget(mode_buttons_layout)
        layout.add_widget(mode_layout)
        
        # 其他选项
        options_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        options_title = MDLabel(
            text="其他选项",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        options_layout.add_widget(options_title)
        
        # 区分大小写
        case_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        case_label = MDLabel(
            text="区分大小写",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        case_layout.add_widget(case_label)
        
        self.case_sensitive_switch = MDSwitch(
            active=False,
            size_hint_x=0.3
        )
        case_layout.add_widget(self.case_sensitive_switch)
        
        options_layout.add_widget(case_layout)
        
        # 包含例句翻译
        translation_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        translation_label = MDLabel(
            text="搜索例句翻译",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        translation_layout.add_widget(translation_label)
        
        self.search_translation_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        translation_layout.add_widget(self.search_translation_switch)
        
        options_layout.add_widget(translation_layout)
        
        layout.add_widget(options_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_history_card(self):
        """创建搜索历史卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题和清除按钮
        title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        title = MDLabel(
            text="搜索历史",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.8
        )
        title_layout.add_widget(title)
        
        clear_btn = MDRaisedButton(
            text="清除",
            size_hint_x=0.2,
            on_release=self._clear_history
        )
        title_layout.add_widget(clear_btn)
        
        layout.add_widget(title_layout)
        
        # 历史列表
        self.history_list = MDList()
        layout.add_widget(self.history_list)
        
        card.add_widget(layout)
        return card
    
    def _create_results_card(self):
        """创建搜索结果卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题和统计
        title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        self.results_title = MDLabel(
            text="搜索结果",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.7
        )
        title_layout.add_widget(self.results_title)
        
        self.results_count = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=0.3
        )
        title_layout.add_widget(self.results_count)
        
        layout.add_widget(title_layout)
        
        # 结果列表
        self.results_scroll = MDScrollView()
        self.results_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.results_container.bind(minimum_height=self.results_container.setter('height'))
        
        self.results_scroll.add_widget(self.results_container)
        layout.add_widget(self.results_scroll)
        
        card.add_widget(layout)
        return card
    
    def _set_search_mode(self, mode):
        """设置搜索模式"""
        self.search_mode = mode
        
        # 更新按钮状态
        self.fuzzy_btn.md_bg_color = self.theme_cls.primary_color if mode == 'fuzzy' else self.theme_cls.primary_light
        self.regex_btn.md_bg_color = self.theme_cls.primary_color if mode == 'regex' else self.theme_cls.primary_light
        self.exact_btn.md_bg_color = self.theme_cls.primary_color if mode == 'exact' else self.theme_cls.primary_light
        
        self.logger.info(f"搜索模式已设置为: {mode}")
    
    def _perform_search(self, instance):
        """执行搜索"""
        query = self.search_bar.search_field.text.strip()
        if not query:
            self.show_snackbar("请输入搜索关键词")
            return
        
        try:
            # 收集搜索参数
            search_params = {
                'query': query,
                'search_type': self.search_bar.search_type,
                'case_sensitive': self.case_sensitive_switch.active,
                'fuzzy_search': self.search_mode == 'fuzzy',
                'search_mode': self.search_mode,
                'search_fields': [field for field, switch in self.field_switches.items() if switch.active],
                'search_translation': self.search_translation_switch.active
            }
            
            self.current_search_params = search_params
            
            # 添加到搜索历史
            self._add_to_history(query, search_params)
            
            # 执行搜索
            results = search_service.advanced_search(search_params)
            
            # 显示结果
            self._display_results(results)
            
            self.logger.info(f"搜索完成，找到 {len(results)} 条结果")
            
        except Exception as e:
            self.logger.error(f"搜索失败: {e}")
            self.show_snackbar("搜索失败，请检查搜索条件")
    
    
    def _display_results(self, results):
        """显示搜索结果"""
        # 清空结果容器
        self.results_container.clear_widgets()
        
        # 更新统计信息
        self.results_count.text = f"共 {len(results)} 条"
        
        if not results:
            no_results_label = MDLabel(
                text="未找到匹配的词条",
                theme_text_color="Secondary",
                font_style="Body1",
                halign="center"
            )
            self.results_container.add_widget(no_results_label)
            return
        
        # 显示结果
        for word_entry in results:
            word_card = WordCard(word_entry=word_entry)
            # 这里可以添加高亮功能
            self._highlight_search_results(word_card, self.current_search_params['query'])
            self.results_container.add_widget(word_card)
    
    def _highlight_search_results(self, word_card, query):
        """高亮搜索结果"""
        # 这里可以实现文本高亮功能
        # 由于KivyMD的限制，这里先记录高亮信息
        word_card.highlight_query = query
        pass
    
    def _add_to_history(self, query, params):
        """添加到搜索历史"""
        history_item = {
            'query': query,
            'params': params,
            'timestamp': self._get_current_time()
        }
        
        # 避免重复
        for item in self.search_history:
            if item['query'] == query:
                self.search_history.remove(item)
                break
        
        self.search_history.insert(0, history_item)
        
        # 限制历史记录数量
        if len(self.search_history) > 10:
            self.search_history = self.search_history[:10]
        
        self._update_history_display()
    
    def _update_history_display(self):
        """更新历史显示"""
        self.history_list.clear_widgets()
        
        for item in self.search_history:
            history_list_item = OneLineListItem(
                text=f"{item['query']} ({item['timestamp']})",
                on_release=lambda x, item=item: self._use_history_item(item)
            )
            self.history_list.add_widget(history_list_item)
    
    def _use_history_item(self, item):
        """使用历史搜索项"""
        self.search_bar.set_search_text(item['query'])
        
        # 恢复搜索参数
        params = item['params']
        self.case_sensitive_switch.active = params['case_sensitive']
        self.search_translation_switch.active = params['search_translation']
        self._set_search_mode(params['search_mode'])
        
        # 恢复字段选择
        for field, switch in self.field_switches.items():
            switch.active = field in params.get('search_fields', [])
        
        self.logger.info(f"使用历史搜索: {item['query']}")
    
    def _clear_history(self, instance):
        """清除搜索历史"""
        self.search_history = []
        self._update_history_display()
        self.logger.info("搜索历史已清除")
    
    def _get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M")
    
    def refresh_data(self):
        """刷新数据"""
        # 重新加载搜索历史
        self._update_history_display()
