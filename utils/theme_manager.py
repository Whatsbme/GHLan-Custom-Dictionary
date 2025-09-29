"""
主题管理器
Theme Manager
"""

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from utils.logger import get_logger
from utils.ink_theme import ink_theme
from app.config import config


class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.app = None
    
    def set_app(self, app):
        """设置应用实例"""
        self.app = app
    
    def apply_theme(self):
        """应用主题设置"""
        if not self.app:
            self.logger.warning("应用实例未设置")
            return
        
        try:
            # 获取主题设置
            theme_style = config.get('THEME', 'style', 'light')
            primary_palette = config.get('THEME', 'primary_palette', 'Blue')
            accent_palette = config.get('THEME', 'accent_palette', 'Orange')
            
            # 应用主题样式
            self.app.theme_cls.theme_style = "Light" if theme_style == 'light' else "Dark"
            self.app.theme_cls.primary_palette = primary_palette
            self.app.theme_cls.accent_palette = accent_palette
            
            # 不修改字体样式，使用KivyMD默认字体配置
            
            self.logger.info(f"主题已应用: {theme_style}, {primary_palette}, {accent_palette}")
            
        except Exception as e:
            self.logger.error(f"应用主题失败: {e}")
    
    def switch_theme_style(self, style):
        """切换主题样式"""
        if style not in ['light', 'dark']:
            self.logger.error(f"无效的主题样式: {style}")
            return
        
        try:
            # 更新配置
            config.set('THEME', 'style', style)
            
            # 应用主题
            if self.app:
                self.app.theme_cls.theme_style = "Light" if style == 'light' else "Dark"
            
            self.logger.info(f"主题样式已切换为: {style}")
            
        except Exception as e:
            self.logger.error(f"切换主题样式失败: {e}")
    
    def set_primary_palette(self, palette):
        """设置主色调"""
        valid_palettes = [
            'Blue', 'Red', 'Green', 'Purple', 'Orange',
            'Teal', 'Indigo', 'Pink', 'Brown', 'Grey'
        ]
        
        if palette not in valid_palettes:
            self.logger.error(f"无效的主色调: {palette}")
            return
        
        try:
            # 更新配置
            config.set('THEME', 'primary_palette', palette)
            
            # 应用主题
            if self.app:
                self.app.theme_cls.primary_palette = palette
            
            self.logger.info(f"主色调已设置为: {palette}")
            
        except Exception as e:
            self.logger.error(f"设置主色调失败: {e}")
    
    def set_accent_palette(self, palette):
        """设置强调色"""
        valid_palettes = [
            'Blue', 'Red', 'Green', 'Purple', 'Orange',
            'Teal', 'Indigo', 'Pink', 'Brown', 'Grey'
        ]
        
        if palette not in valid_palettes:
            self.logger.error(f"无效的强调色: {palette}")
            return
        
        try:
            # 更新配置
            config.set('THEME', 'accent_palette', palette)
            
            # 应用主题
            if self.app:
                self.app.theme_cls.accent_palette = palette
            
            self.logger.info(f"强调色已设置为: {palette}")
            
        except Exception as e:
            self.logger.error(f"设置强调色失败: {e}")
    
    def get_theme_info(self):
        """获取主题信息"""
        return {
            'style': config.get('THEME', 'style', 'light'),
            'primary_palette': config.get('THEME', 'primary_palette', 'Blue'),
            'accent_palette': config.get('THEME', 'accent_palette', 'Orange')
        }
    
    def reset_to_default(self):
        """重置为默认主题"""
        try:
            config.set('THEME', 'style', 'light')
            config.set('THEME', 'primary_palette', 'Blue')
            config.set('THEME', 'accent_palette', 'Orange')
            
            # 应用默认主题
            self.apply_theme()
            
            self.logger.info("主题已重置为默认")
            
        except Exception as e:
            self.logger.error(f"重置主题失败: {e}")
    
    def apply_ink_theme(self):
        """应用水墨主题"""
        if not self.app:
            self.logger.warning("ThemeManager: App instance not set.")
            return
        
        ink_theme.apply_ink_theme(self.app)
        self.logger.info("应用水墨主题成功")
    
    def toggle_ink_theme(self):
        """切换水墨主题"""
        current_style = config.get('THEME', 'style', 'light')
        if current_style == 'ink':
            # 切换回普通主题
            config.set('THEME', 'style', 'light')
            self.apply_theme()
        else:
            # 切换到水墨主题
            config.set('THEME', 'style', 'ink')
            self.apply_ink_theme()
        config.save()


# 全局主题管理器实例
theme_manager = ThemeManager()