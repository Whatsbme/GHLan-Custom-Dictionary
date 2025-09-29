"""
水墨风格输入组件
Ink Style Input Components
"""

from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.animation import Animation

from utils.ink_theme import ink_theme
from utils.logger import get_logger


class InkTextField(MDTextField):
    """水墨风格文本输入框"""
    
    def __init__(self, hint_text="", ink_style="default", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.hint_text = hint_text
        self.ink_style = ink_style
        
        self._setup_ink_style()
        self._setup_ink_animation()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.mode = "rectangle"
        self.radius = [dp(8), dp(8), dp(8), dp(8)]
        self.line_color_normal = ink_theme.get_color('border_light')
        self.line_color_focus = ink_theme.get_color('ink_black')
        self.hint_text_color_normal = ink_theme.get_color('ink_light')
        self.hint_text_color_focus = ink_theme.get_color('ink_medium')
        self.text_color = ink_theme.get_color('ink_black')
        
        # 根据样式设置颜色
        if self.ink_style == "primary":
            self.line_color_focus = ink_theme.get_color('cinnabar')
        elif self.ink_style == "secondary":
            self.line_color_focus = ink_theme.get_color('water_blue')
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('paper_white'))
            self.background_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius
            )
        
        self.bind(pos=self._update_background, size=self._update_background)
    
    def _update_background(self, *args):
        """更新背景"""
        if hasattr(self, 'background_rect'):
            self.background_rect.pos = self.pos
            self.background_rect.size = self.size
    
    def _setup_ink_animation(self):
        """设置水墨动画"""
        def on_focus(instance, value):
            if value:
                # 获得焦点时的动画
                Animation(
                    line_color_focus=ink_theme.get_color('cinnabar'),
                    duration=0.3
                ).start(instance)
            else:
                # 失去焦点时的动画
                Animation(
                    line_color_focus=ink_theme.get_color('ink_black'),
                    duration=0.3
                ).start(instance)
        
        self.bind(focus=on_focus)


class InkSearchField(InkTextField):
    """水墨风格搜索框"""
    
    def __init__(self, hint_text="搜索...", **kwargs):
        super().__init__(hint_text=hint_text, ink_style="primary", **kwargs)
        
        self._setup_search_style()
    
    def _setup_search_style(self):
        """设置搜索风格"""
        # 搜索框特殊设置
        self.icon_left = "magnify"
        self.icon_left_color = ink_theme.get_color('ink_medium')
        
        # 搜索动画效果
        def on_text(instance, value):
            if value:
                # 有文本时的动画
                Animation(
                    icon_left_color=ink_theme.get_color('cinnabar'),
                    duration=0.2
                ).start(instance)
            else:
                # 无文本时的动画
                Animation(
                    icon_left_color=ink_theme.get_color('ink_medium'),
                    duration=0.2
                ).start(instance)
        
        self.bind(text=on_text)


class InkPasswordField(InkTextField):
    """水墨风格密码输入框"""
    
    def __init__(self, hint_text="密码", **kwargs):
        super().__init__(hint_text=hint_text, **kwargs)
        
        self._setup_password_style()
    
    def _setup_password_style(self):
        """设置密码风格"""
        # 密码框设置
        self.password = True
        self.icon_left = "lock"
        self.icon_left_color = ink_theme.get_color('ink_medium')
        
        # 显示/隐藏密码按钮
        self.icon_right = "eye-off"
        self.icon_right_color = ink_theme.get_color('ink_medium')
        
        def toggle_password(instance):
            if instance.password:
                instance.password = False
                instance.icon_right = "eye"
            else:
                instance.password = True
                instance.icon_right = "eye-off"
        
        self.bind(on_icon_right_press=toggle_password)


class InkFormField(MDBoxLayout):
    """水墨风格表单字段"""
    
    def __init__(self, label="", field_type="text", required=False, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(80)
        
        self.label_text = label
        self.field_type = field_type
        self.required = required
        
        self._setup_form_field()
    
    def _setup_form_field(self):
        """设置表单字段"""
        # 标签
        if self.label_text:
            label_text = self.label_text
            if self.required:
                label_text += " *"
            
            self.label = MDLabel(
                text=label_text,
                theme_text_color="Primary",
                font_style="Body1",
                size_hint_y=None,
                height=dp(24)
            )
            self.add_widget(self.label)
        
        # 输入字段
        if self.field_type == "text":
            self.field = InkTextField(hint_text=f"请输入{self.label_text}")
        elif self.field_type == "password":
            self.field = InkPasswordField(hint_text=f"请输入{self.label_text}")
        elif self.field_type == "search":
            self.field = InkSearchField(hint_text=f"搜索{self.label_text}")
        else:
            self.field = InkTextField(hint_text=f"请输入{self.label_text}")
        
        self.add_widget(self.field)
    
    def get_value(self):
        """获取字段值"""
        return self.field.text if self.field else ""
    
    def set_value(self, value):
        """设置字段值"""
        if self.field:
            self.field.text = value
    
    def clear_value(self):
        """清空字段值"""
        if self.field:
            self.field.text = ""
    
    def set_error(self, error_message):
        """设置错误信息"""
        if hasattr(self, 'label'):
            self.label.text = f"{self.label_text} - {error_message}"
            self.label.theme_text_color = "Error"
    
    def clear_error(self):
        """清除错误信息"""
        if hasattr(self, 'label'):
            label_text = self.label_text
            if self.required:
                label_text += " *"
            self.label.text = label_text
            self.label.theme_text_color = "Primary"


class InkForm(MDBoxLayout):
    """水墨风格表单"""
    
    def __init__(self, fields=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.orientation = 'vertical'
        self.spacing = dp(16)
        self.padding = dp(16)
        
        self.fields = fields or []
        self.form_fields = {}
        
        self._setup_form()
    
    def _setup_form(self):
        """设置表单"""
        for field_config in self.fields:
            if isinstance(field_config, dict):
                field = InkFormField(
                    label=field_config.get('label', ''),
                    field_type=field_config.get('type', 'text'),
                    required=field_config.get('required', False)
                )
                self.form_fields[field_config.get('name', field_config.get('label', ''))] = field
                self.add_widget(field)
            else:
                self.add_widget(field_config)
    
    def add_field(self, name, label, field_type="text", required=False):
        """添加字段"""
        field = InkFormField(
            label=label,
            field_type=field_type,
            required=required
        )
        self.form_fields[name] = field
        self.add_widget(field)
        return field
    
    def get_values(self):
        """获取表单值"""
        values = {}
        for name, field in self.form_fields.items():
            values[name] = field.get_value()
        return values
    
    def set_values(self, values):
        """设置表单值"""
        for name, value in values.items():
            if name in self.form_fields:
                self.form_fields[name].set_value(value)
    
    def clear_form(self):
        """清空表单"""
        for field in self.form_fields.values():
            field.clear_value()
    
    def validate_form(self):
        """验证表单"""
        errors = []
        for name, field in self.form_fields.items():
            if field.required and not field.get_value():
                field.set_error("此字段为必填项")
                errors.append(f"{field.label_text} 为必填项")
            else:
                field.clear_error()
        return len(errors) == 0, errors
