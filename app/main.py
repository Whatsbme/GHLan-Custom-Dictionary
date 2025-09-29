"""
应用主入口
Application Main Entry Point
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivymd.app import MDApp
from kivymd.theming import ThemeManager

from app.config import config
from utils.logger import setup_logger
from utils.theme_manager import theme_manager


class OfflineDictionaryApp(MDApp):
    """GHLan自定义字典应用主类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "GHLan自定义字典"
        self.icon = "assets/icons/app_icon.png"
        
        # 设置主题管理器
        theme_manager.set_app(self)
        theme_manager.apply_theme()
        
        # 设置字体大小
        font_size = config.get_int('APP', 'font_size', 16)
        self.theme_cls.font_styles.update({
            "H1": ["RobotoLight", font_size + 8, False, -1.5, None],
            "H2": ["RobotoLight", font_size + 6, False, -0.5, None],
            "H3": ["Roboto", font_size + 4, False, -1.5, None],
            "H4": ["Roboto", font_size + 2, False, 0.25, None],
            "H5": ["Roboto", font_size, False, 0, None],
            "H6": ["RobotoMedium", font_size - 2, False, 0.15, None],
            "Subtitle1": ["Roboto", font_size, False, 0.15, None],
            "Subtitle2": ["RobotoMedium", font_size - 2, False, 0.1, None],
            "Body1": ["Roboto", font_size, False, 0.5, None],
            "Body2": ["Roboto", font_size - 2, False, 0.25, None],
            "Button": ["RobotoMedium", font_size - 2, True, 1.25, None],
            "Caption": ["Roboto", font_size - 4, False, 1.5, None],
            "Overline": ["Roboto", font_size - 6, True, 1.5, None],
        })
    
    def build(self):
        """构建应用界面"""
        try:
            # 设置窗口大小（开发时使用）
            if sys.platform != 'android':
                Window.size = (400, 800)  # 手机屏幕比例
            
            # 导入主界面
            from views.main_screen import MainScreen
            
            # 创建主界面
            main_screen = MainScreen()
            
            Logger.info("应用启动成功")
            return main_screen
            
        except Exception as e:
            Logger.error(f"应用启动失败: {e}")
            raise
    
    def on_start(self):
        """应用启动时的初始化"""
        try:
            # 初始化数据库
            from services.database_service import db_service
            Logger.info("数据库服务已初始化")
            
            # 检查数据库连接
            db_info = db_service.get_database_info()
            if db_info:
                Logger.info(f"数据库信息: {db_info}")
            
        except Exception as e:
            Logger.error(f"应用初始化失败: {e}")
    
    def on_pause(self):
        """应用暂停时调用（Android）"""
        Logger.info("应用暂停")
        return True
    
    def on_resume(self):
        """应用恢复时调用（Android）"""
        Logger.info("应用恢复")
    
    def on_stop(self):
        """应用停止时调用"""
        try:
            # 关闭数据库连接
            from services.database_service import db_service
            db_service.close()
            Logger.info("应用已停止")
        except Exception as e:
            Logger.error(f"应用停止时出错: {e}")


def main():
    """主函数"""
    try:
        # 设置日志
        setup_logger()
        
        # 创建并运行应用
        app = OfflineDictionaryApp()
        app.run()
        
    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
