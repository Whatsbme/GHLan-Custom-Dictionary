"""
水墨风格卡片组件
Ink Style Card Components
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation

from utils.ink_theme import ink_theme
from utils.logger import get_logger


class InkCard(MDCard):
    """水墨风格卡片"""
    
    def __init__(self, title="", subtitle="", content="", actions=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        # 水墨风格设置
        self.elevation = 2
        self.radius = [dp(12), dp(12), dp(12), dp(12)]
        self.md_bg_color = ink_theme.get_color('paper_white')
        self.padding = dp(16)
        self.spacing = dp(12)
        
        # 内容
        self.title = title
        self.subtitle = subtitle
        self.content_text = content
        self.actions = actions or []
        
        self._setup_ui()
        self._setup_ink_style()
    
    def _setup_ui(self):
        """设置UI"""
        # 主容器
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=self.spacing
        )
        
        # 标题区域
        if self.title:
            self.title_label = MDLabel(
                text=self.title,
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height=dp(32)
            )
            self.main_layout.add_widget(self.title_label)
        
        # 副标题区域
        if self.subtitle:
            self.subtitle_label = MDLabel(
                text=self.subtitle,
                theme_text_color="Secondary",
                font_style="Body2",
                size_hint_y=None,
                height=dp(24)
            )
            self.main_layout.add_widget(self.subtitle_label)
        
        # 内容区域
        if self.content_text:
            self.content_label = MDLabel(
                text=self.content_text,
                theme_text_color="Primary",
                font_style="Body1",
                text_size=(None, None),
                halign="left",
                valign="top"
            )
            self.main_layout.add_widget(self.content_label)
        
        # 操作按钮区域
        if self.actions:
            self.actions_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(8),
                size_hint_y=None,
                height=dp(40)
            )
            
            for action in self.actions:
                if isinstance(action, dict):
                    btn = MDRaisedButton(
                        text=action.get('text', ''),
                        on_release=action.get('on_release', None)
                    )
                    self.actions_layout.add_widget(btn)
                else:
                    self.actions_layout.add_widget(action)
            
            self.main_layout.add_widget(self.actions_layout)
        
        self.add_widget(self.main_layout)
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        with self.canvas.before:
            # 水墨边框
            Color(*ink_theme.get_color('border_light'))
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius
            )
            
            # 水墨阴影
            Color(*ink_theme.get_color('shadow_soft'))
            self.shadow_rect = RoundedRectangle(
                pos=(self.x - dp(2), self.y - dp(2)),
                size=(self.width + dp(4), self.height + dp(4)),
                radius=self.radius
            )
        
        self.bind(pos=self._update_ink_style, size=self._update_ink_style)
    
    def _update_ink_style(self, *args):
        """更新水墨风格"""
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = self.pos
            self.border_rect.size = self.size
        
        if hasattr(self, 'shadow_rect'):
            self.shadow_rect.pos = (self.x - dp(2), self.y - dp(2))
            self.shadow_rect.size = (self.width + dp(4), self.height + dp(4))
    
    def add_ink_animation(self):
        """添加水墨动画效果"""
        # 悬停效果
        def on_enter(instance):
            Animation(
                elevation=4,
                duration=0.2
            ).start(instance)
        
        def on_leave(instance):
            Animation(
                elevation=2,
                duration=0.2
            ).start(instance)
        
        self.bind(on_enter=on_enter, on_leave=on_leave)


class InkInfoCard(InkCard):
    """水墨风格信息卡片"""
    
    def __init__(self, icon="", title="", info="", **kwargs):
        super().__init__(title=title, **kwargs)
        
        self.icon = icon
        self.info = info
        
        self._setup_info_ui()
    
    def _setup_info_ui(self):
        """设置信息UI"""
        # 图标和标题布局
        header_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(12),
            size_hint_y=None,
            height=dp(40)
        )
        
        if self.icon:
            icon_btn = MDIconButton(
                icon=self.icon,
                theme_text_color="Primary",
                size_hint_x=None,
                width=dp(40)
            )
            header_layout.add_widget(icon_btn)
        
        if self.title:
            title_label = MDLabel(
                text=self.title,
                theme_text_color="Primary",
                font_style="H6",
                size_hint_x=0.7
            )
            header_layout.add_widget(title_label)
        
        self.main_layout.add_widget(header_layout)
        
        # 信息内容
        if self.info:
            info_label = MDLabel(
                text=self.info,
                theme_text_color="Secondary",
                font_style="Body1",
                text_size=(None, None),
                halign="left",
                valign="top"
            )
            self.main_layout.add_widget(info_label)


class InkActionCard(InkCard):
    """水墨风格操作卡片"""
    
    def __init__(self, title="", description="", primary_action=None, secondary_action=None, **kwargs):
        super().__init__(title=title, subtitle=description, **kwargs)
        
        self.primary_action = primary_action
        self.secondary_action = secondary_action
        
        self._setup_action_ui()
    
    def _setup_action_ui(self):
        """设置操作UI"""
        if self.primary_action or self.secondary_action:
            actions_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(12),
                size_hint_y=None,
                height=dp(48)
            )
            
            if self.secondary_action:
                secondary_btn = MDRaisedButton(
                    text=self.secondary_action.get('text', ''),
                    on_release=self.secondary_action.get('on_release', None),
                    size_hint_x=0.4,
                    md_bg_color=ink_theme.get_color('ink_light')
                )
                actions_layout.add_widget(secondary_btn)
            
            if self.primary_action:
                primary_btn = MDRaisedButton(
                    text=self.primary_action.get('text', ''),
                    on_release=self.primary_action.get('on_release', None),
                    size_hint_x=0.6,
                    md_bg_color=ink_theme.get_color('cinnabar')
                )
                actions_layout.add_widget(primary_btn)
            
            self.main_layout.add_widget(actions_layout)


class InkListCard(InkCard):
    """水墨风格列表卡片"""
    
    def __init__(self, title="", items=None, **kwargs):
        super().__init__(title=title, **kwargs)
        
        self.items = items or []
        
        self._setup_list_ui()
    
    def _setup_list_ui(self):
        """设置列表UI"""
        if self.items:
            for item in self.items:
                item_layout = MDBoxLayout(
                    orientation='horizontal',
                    spacing=dp(12),
                    size_hint_y=None,
                    height=dp(48)
                )
                
                # 项目图标
                if item.get('icon'):
                    icon_btn = MDIconButton(
                        icon=item['icon'],
                        theme_text_color="Primary",
                        size_hint_x=None,
                        width=dp(40)
                    )
                    item_layout.add_widget(icon_btn)
                
                # 项目内容
                content_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(4)
                )
                
                title_label = MDLabel(
                    text=item.get('title', ''),
                    theme_text_color="Primary",
                    font_style="Body1",
                    size_hint_y=None,
                    height=dp(20)
                )
                content_layout.add_widget(title_label)
                
                if item.get('subtitle'):
                    subtitle_label = MDLabel(
                        text=item['subtitle'],
                        theme_text_color="Secondary",
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(16)
                    )
                    content_layout.add_widget(subtitle_label)
                
                item_layout.add_widget(content_layout)
                
                # 项目操作
                if item.get('action'):
                    action_btn = MDIconButton(
                        icon=item['action'].get('icon', 'chevron-right'),
                        theme_text_color="Secondary",
                        size_hint_x=None,
                        width=dp(40),
                        on_release=item['action'].get('on_release', None)
                    )
                    item_layout.add_widget(action_btn)
                
                self.main_layout.add_widget(item_layout)
