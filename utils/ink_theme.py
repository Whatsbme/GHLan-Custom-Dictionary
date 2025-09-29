"""
水墨色风格主题
Ink Style Theme
"""

from kivy.utils import get_color_from_hex
from kivymd.theming import ThemeManager


class InkTheme:
    """水墨色风格主题类"""
    
    # 水墨色配色方案
    INK_COLORS = {
        # 主色调 - 墨色系
        'ink_black': '#2C2C2C',      # 浓墨
        'ink_dark': '#4A4A4A',       # 深墨
        'ink_medium': '#6B6B6B',     # 中墨
        'ink_light': '#8A8A8A',      # 淡墨
        'ink_pale': '#B0B0B0',       # 浅墨
        
        # 辅助色 - 水墨系
        'water_blue': '#4A90A4',     # 水蓝
        'water_light': '#7BB3C4',    # 浅水蓝
        'water_pale': '#A8D0D9',     # 淡水蓝
        
        # 强调色 - 朱砂系
        'cinnabar': '#D2691E',       # 朱砂
        'cinnabar_light': '#E07B3A', # 浅朱砂
        'cinnabar_pale': '#F0A366',  # 淡朱砂
        
        # 背景色 - 宣纸系
        'paper_white': '#FEFEFE',    # 宣纸白
        'paper_cream': '#F5F5F0',    # 米色
        'paper_warm': '#F0F0E8',     # 暖白
        
        # 边框色
        'border_dark': '#8A8A8A',    # 深边框
        'border_light': '#D0D0D0',   # 浅边框
        
        # 阴影色
        'shadow_soft': '#E0E0E0',    # 柔和阴影
        'shadow_medium': '#C0C0C0',  # 中等阴影
        'shadow_dark': '#A0A0A0',    # 深阴影
    }
    
    @classmethod
    def get_color(cls, color_name):
        """获取颜色值"""
        return get_color_from_hex(cls.INK_COLORS.get(color_name, '#000000'))
    
    @classmethod
    def apply_ink_theme(cls, app):
        """应用水墨主题到应用"""
        if not app:
            return
        
        # 设置主题颜色
        app.theme_cls.primary_palette = "Blue"
        app.theme_cls.accent_palette = "Orange"
        app.theme_cls.theme_style = "Light"
        
        # 自定义颜色
        app.theme_cls.primary_color = cls.get_color('ink_black')
        app.theme_cls.accent_color = cls.get_color('cinnabar')
        app.theme_cls.bg_dark = cls.get_color('ink_black')
        app.theme_cls.bg_light = cls.get_color('paper_white')
        
        # 设置字体样式 - 使用系统默认字体
        font_size = 16
        font_family = "Arial"  # 使用系统默认字体
        app.theme_cls.font_styles.update({
            "H1": [font_family, font_size + 8, False, -1.5, None],
            "H2": [font_family, font_size + 6, False, -1.5, None],
            "H3": [font_family, font_size + 4, False, -1.5, None],
            "H4": [font_family, font_size + 2, False, -1.5, None],
            "H5": [font_family, font_size, False, -1.5, None],
            "H6": [font_family, font_size - 2, False, -1.5, None],
            "Subtitle1": [font_family, font_size - 2, False, -1.5, None],
            "Subtitle2": [font_family, font_size - 4, False, -1.5, None],
            "Body1": [font_family, font_size - 4, False, -1.5, None],
            "Body2": [font_family, font_size - 6, False, -1.5, None],
            "Button": [font_family, font_size - 6, True, 0.1, None],
            "Caption": [font_family, font_size - 8, False, 0.4, None],
            "Overline": [font_family, font_size - 10, True, 0.8, None],
            "Icon": [font_family, font_size, False, 0, None],
        })
    
    @classmethod
    def get_ink_style(cls):
        """获取水墨风格样式字典"""
        return {
            'primary_color': cls.get_color('ink_black'),
            'accent_color': cls.get_color('cinnabar'),
            'background_color': cls.get_color('paper_white'),
            'surface_color': cls.get_color('paper_cream'),
            'text_primary': cls.get_color('ink_black'),
            'text_secondary': cls.get_color('ink_medium'),
            'border_color': cls.get_color('border_light'),
            'shadow_color': cls.get_color('shadow_soft'),
        }


# 全局水墨主题实例
ink_theme = InkTheme()
