"""
水墨风格按钮组件
Ink Style Button Components
"""

from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation

from utils.ink_theme import ink_theme
from utils.logger import get_logger


class InkButton(MDRaisedButton):
    """水墨风格按钮"""
    
    def __init__(self, text="", ink_style="primary", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.text = text
        self.ink_style = ink_style
        
        self._setup_ink_style()
        self._setup_ink_animation()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.radius = [dp(8), dp(8), dp(8), dp(8)]
        self.elevation = 2
        
        # 根据样式设置颜色
        if self.ink_style == "primary":
            self.md_bg_color = ink_theme.get_color('ink_black')
            self.text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "accent":
            self.md_bg_color = ink_theme.get_color('cinnabar')
            self.text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "secondary":
            self.md_bg_color = ink_theme.get_color('water_blue')
            self.text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "outline":
            self.md_bg_color = ink_theme.get_color('paper_white')
            self.text_color = ink_theme.get_color('ink_black')
            self.line_color = ink_theme.get_color('ink_black')
        else:
            self.md_bg_color = ink_theme.get_color('ink_light')
            self.text_color = ink_theme.get_color('paper_white')
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('border_light'))
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius
            )
        
        self.bind(pos=self._update_border, size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = self.pos
            self.border_rect.size = self.size
    
    def _setup_ink_animation(self):
        """设置水墨动画"""
        def on_press(instance):
            Animation(
                elevation=4,
                duration=0.1
            ).start(instance)
        
        def on_release(instance):
            Animation(
                elevation=2,
                duration=0.2
            ).start(instance)
        
        self.bind(on_press=on_press, on_release=on_release)


class InkIconButton(MDIconButton):
    """水墨风格图标按钮"""
    
    def __init__(self, icon="", ink_style="primary", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.icon = icon
        self.ink_style = ink_style
        
        self._setup_ink_style()
        self._setup_ink_animation()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.radius = [dp(20), dp(20), dp(20), dp(20)]
        self.size_hint = (None, None)
        self.size = (dp(48), dp(48))
        
        # 根据样式设置颜色
        if self.ink_style == "primary":
            self.md_bg_color = ink_theme.get_color('ink_black')
            self.theme_text_color = "Custom"
            self.text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "accent":
            self.md_bg_color = ink_theme.get_color('cinnabar')
            self.theme_text_color = "Custom"
            self.text_color = ink_theme.get_color('paper_white')
        elif self.ink_style == "secondary":
            self.md_bg_color = ink_theme.get_color('water_blue')
            self.theme_text_color = "Custom"
            self.text_color = ink_theme.get_color('paper_white')
        else:
            self.md_bg_color = ink_theme.get_color('paper_white')
            self.theme_text_color = "Primary"
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('border_light'))
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius
            )
        
        self.bind(pos=self._update_border, size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = self.pos
            self.border_rect.size = self.size
    
    def _setup_ink_animation(self):
        """设置水墨动画"""
        def on_press(instance):
            Animation(
                scale=0.95,
                duration=0.1
            ).start(instance)
        
        def on_release(instance):
            Animation(
                scale=1.0,
                duration=0.2
            ).start(instance)
        
        self.bind(on_press=on_press, on_release=on_release)


class InkFloatingButton(InkIconButton):
    """水墨风格浮动按钮"""
    
    def __init__(self, icon="plus", **kwargs):
        super().__init__(icon=icon, ink_style="accent", **kwargs)
        
        self._setup_floating_style()
    
    def _setup_floating_style(self):
        """设置浮动风格"""
        self.elevation = 6
        self.size = (dp(56), dp(56))
        self.radius = [dp(28), dp(28), dp(28), dp(28)]
        
        # 浮动按钮特殊效果
        with self.canvas.after:
            Color(*ink_theme.get_color('shadow_medium'))
            self.shadow_rect = RoundedRectangle(
                pos=(self.x - dp(2), self.y - dp(2)),
                size=(self.width + dp(4), self.height + dp(4)),
                radius=self.radius
            )
        
        self.bind(pos=self._update_shadow, size=self._update_shadow)
    
    def _update_shadow(self, *args):
        """更新阴影"""
        if hasattr(self, 'shadow_rect'):
            self.shadow_rect.pos = (self.x - dp(2), self.y - dp(2))
            self.shadow_rect.size = (self.width + dp(4), self.height + dp(4))


class InkButtonGroup(MDBoxLayout):
    """水墨风格按钮组"""
    
    def __init__(self, buttons=None, orientation="horizontal", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = orientation
        self.spacing = dp(8)
        self.buttons = buttons or []
        
        self._setup_buttons()
    
    def _setup_buttons(self):
        """设置按钮"""
        for button_config in self.buttons:
            if isinstance(button_config, dict):
                btn = InkButton(
                    text=button_config.get('text', ''),
                    ink_style=button_config.get('style', 'primary'),
                    on_release=button_config.get('on_release', None)
                )
                self.add_widget(btn)
            else:
                self.add_widget(button_config)
    
    def add_button(self, text, style="primary", on_release=None):
        """添加按钮"""
        btn = InkButton(
            text=text,
            ink_style=style,
            on_release=on_release
        )
        self.add_widget(btn)
        return btn
    
    def clear_buttons(self):
        """清空按钮"""
        self.clear_widgets()


class InkToggleButton(InkButton):
    """水墨风格切换按钮"""
    
    def __init__(self, text="", **kwargs):
        super().__init__(text=text, **kwargs)
        
        self.is_toggled = False
        self._setup_toggle_style()
    
    def _setup_toggle_style(self):
        """设置切换风格"""
        self.bind(on_release=self._toggle)
    
    def _toggle(self, instance):
        """切换状态"""
        self.is_toggled = not self.is_toggled
        
        if self.is_toggled:
            # 选中状态
            self.md_bg_color = ink_theme.get_color('cinnabar')
            self.text_color = ink_theme.get_color('paper_white')
        else:
            # 未选中状态
            self.md_bg_color = ink_theme.get_color('ink_light')
            self.text_color = ink_theme.get_color('paper_white')
        
        # 触发切换事件
        self.dispatch('on_toggle', self.is_toggled)
    
    def on_toggle(self, is_toggled):
        """切换事件"""
        pass







