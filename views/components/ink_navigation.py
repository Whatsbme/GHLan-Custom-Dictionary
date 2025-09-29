"""
水墨风格导航组件
Ink Style Navigation Components
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.animation import Animation

from utils.ink_theme import ink_theme
from utils.logger import get_logger


class InkToolbar(MDTopAppBar):
    """水墨风格工具栏"""
    
    def __init__(self, title="", ink_style="primary", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.title = title
        self.ink_style = ink_style
        
        self._setup_ink_style()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.elevation = 4
        self.md_bg_color = ink_theme.get_color('paper_white')
        self.specific_text_color = ink_theme.get_color('ink_black')
        
        # 根据样式设置颜色
        if self.ink_style == "primary":
            self.md_bg_color = ink_theme.get_color('ink_black')
            self.specific_text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "accent":
            self.md_bg_color = ink_theme.get_color('cinnabar')
            self.specific_text_color = ink_theme.get_color('paper_white')
        
        # 设置水墨边框
        with self.canvas.after:
            Color(*ink_theme.get_color('border_light'))
            self.border_line = Line(
                points=[0, 0, self.width, 0],
                width=dp(1)
            )
        
        self.bind(size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_line'):
            self.border_line.points = [0, 0, self.width, 0]


class InkNavigationDrawer(MDNavigationDrawer):
    """水墨风格导航抽屉"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self._setup_ink_style()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.md_bg_color = ink_theme.get_color('paper_white')
        self.elevation = 8
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('border_light'))
            self.border_rect = Rectangle(
                pos=(self.width - dp(1), 0),
                size=(dp(1), self.height)
            )
        
        self.bind(size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = (self.width - dp(1), 0)
            self.border_rect.size = (dp(1), self.height)


class InkNavigationItem(OneLineListItem):
    """水墨风格导航项"""
    
    def __init__(self, text="", icon="", on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.text = text
        self.icon = icon
        self.on_release = on_release
        
        self._setup_ink_style()
        self._setup_ink_animation()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.theme_text_color = "Primary"
        self.text_color = ink_theme.get_color('ink_black')
        self.bg_color = ink_theme.get_color('paper_white')
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('border_light'))
            self.border_line = Line(
                points=[0, 0, self.width, 0],
                width=dp(0.5)
            )
        
        self.bind(size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_line'):
            self.border_line.points = [0, 0, self.width, 0]
    
    def _setup_ink_animation(self):
        """设置水墨动画"""
        def on_enter(instance):
            Animation(
                bg_color=ink_theme.get_color('paper_cream'),
                duration=0.2
            ).start(instance)
        
        def on_leave(instance):
            Animation(
                bg_color=ink_theme.get_color('paper_white'),
                duration=0.2
            ).start(instance)
        
        self.bind(on_enter=on_enter, on_leave=on_leave)


class InkTabBar(MDBoxLayout):
    """水墨风格标签栏"""
    
    def __init__(self, tabs=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = 'horizontal'
        self.spacing = dp(8)
        self.padding = dp(16)
        self.size_hint_y = None
        self.height = dp(56)
        
        self.tabs = tabs or []
        self.active_tab = None
        self.tab_buttons = {}
        
        self._setup_tabs()
    
    def _setup_tabs(self):
        """设置标签"""
        for tab_config in self.tabs:
            if isinstance(tab_config, dict):
                tab_btn = MDRaisedButton(
                    text=tab_config.get('text', ''),
                    on_release=lambda x, tab=tab_config: self._select_tab(tab)
                )
                self.tab_buttons[tab_config.get('id', tab_config.get('text', ''))] = tab_btn
                self.add_widget(tab_btn)
            else:
                self.add_widget(tab_config)
    
    def _select_tab(self, tab):
        """选择标签"""
        # 重置所有标签样式
        for btn in self.tab_buttons.values():
            btn.md_bg_color = ink_theme.get_color('ink_light')
            btn.text_color = ink_theme.get_color('paper_white')
        
        # 设置活动标签样式
        if tab.get('id') in self.tab_buttons:
            active_btn = self.tab_buttons[tab['id']]
            active_btn.md_bg_color = ink_theme.get_color('cinnabar')
            active_btn.text_color = ink_theme.get_color('paper_white')
        
        self.active_tab = tab
        
        # 触发标签选择事件
        if tab.get('on_select'):
            tab['on_select'](tab)
    
    def add_tab(self, tab_id, text, on_select=None):
        """添加标签"""
        tab_config = {
            'id': tab_id,
            'text': text,
            'on_select': on_select
        }
        
        tab_btn = MDRaisedButton(
            text=text,
            on_release=lambda x: self._select_tab(tab_config)
        )
        self.tab_buttons[tab_id] = tab_btn
        self.add_widget(tab_btn)
        
        return tab_config


class InkBreadcrumb(MDBoxLayout):
    """水墨风格面包屑导航"""
    
    def __init__(self, items=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = 'horizontal'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(32)
        
        self.items = items or []
        self._setup_breadcrumb()
    
    def _setup_breadcrumb(self):
        """设置面包屑"""
        for i, item in enumerate(self.items):
            if i > 0:
                # 添加分隔符
                separator = MDLabel(
                    text=">",
                    theme_text_color="Secondary",
                    font_style="Caption"
                )
                self.add_widget(separator)
            
            # 添加面包屑项
            if isinstance(item, dict):
                breadcrumb_item = MDLabel(
                    text=item.get('text', ''),
                    theme_text_color="Primary" if i == len(self.items) - 1 else "Secondary",
                    font_style="Caption"
                )
                self.add_widget(breadcrumb_item)
            else:
                breadcrumb_item = MDLabel(
                    text=str(item),
                    theme_text_color="Primary" if i == len(self.items) - 1 else "Secondary",
                    font_style="Caption"
                )
                self.add_widget(breadcrumb_item)
    
    def add_item(self, text):
        """添加面包屑项"""
        self.items.append(text)
        self.clear_widgets()
        self._setup_breadcrumb()
    
    def set_items(self, items):
        """设置面包屑项"""
        self.items = items
        self.clear_widgets()
        self._setup_breadcrumb()


class InkPagination(MDBoxLayout):
    """水墨风格分页组件"""
    
    def __init__(self, current_page=1, total_pages=1, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = 'horizontal'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(48)
        
        self.current_page = current_page
        self.total_pages = total_pages
        
        self._setup_pagination()
    
    def _setup_pagination(self):
        """设置分页"""
        # 上一页按钮
        self.prev_btn = MDRaisedButton(
            text="上一页",
            on_release=self._prev_page,
            disabled=self.current_page <= 1
        )
        self.add_widget(self.prev_btn)
        
        # 页码显示
        self.page_label = MDLabel(
            text=f"{self.current_page} / {self.total_pages}",
            theme_text_color="Primary",
            font_style="Body1"
        )
        self.add_widget(self.page_label)
        
        # 下一页按钮
        self.next_btn = MDRaisedButton(
            text="下一页",
            on_release=self._next_page,
            disabled=self.current_page >= self.total_pages
        )
        self.add_widget(self.next_btn)
    
    def _prev_page(self, instance):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_pagination()
            self.dispatch('on_page_change', self.current_page)
    
    def _next_page(self, instance):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_pagination()
            self.dispatch('on_page_change', self.current_page)
    
    def _update_pagination(self):
        """更新分页"""
        self.page_label.text = f"{self.current_page} / {self.total_pages}"
        self.prev_btn.disabled = self.current_page <= 1
        self.next_btn.disabled = self.current_page >= self.total_pages
    
    def set_page(self, page):
        """设置页码"""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self._update_pagination()
            self.dispatch('on_page_change', self.current_page)
    
    def set_total_pages(self, total_pages):
        """设置总页数"""
        self.total_pages = total_pages
        if self.current_page > total_pages:
            self.current_page = total_pages
        self._update_pagination()
    
    def on_page_change(self, page):
        """页码改变事件"""
        pass
