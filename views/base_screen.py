"""
基础屏幕类
Base Screen Class
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from utils.logger import get_logger


class BaseScreen(MDScreen):
    """基础屏幕类，提供通用功能"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self._setup_ui()
    
    def _setup_ui(self):
        """设置基础UI"""
        # 主布局
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        self.add_widget(self.main_layout)
        
        # 顶部工具栏
        self.toolbar = MDTopAppBar(
            title=self.get_screen_title(),
            elevation=2,
            md_bg_color=self.theme_cls.primary_color
        )
        self.main_layout.add_widget(self.toolbar)
        
        # 内容区域
        self.content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        self.main_layout.add_widget(self.content_layout)
    
    def get_screen_title(self) -> str:
        """获取屏幕标题，子类需要重写"""
        return "基础屏幕"
    
    def show_snackbar(self, text: str, duration: float = 2.0):
        """显示提示消息"""
        from kivymd.uix.snackbar import Snackbar
        from kivymd.uix.label import MDLabel
        
        # 创建带标签的Snackbar（KivyMD 1.2.0兼容）
        snackbar = Snackbar(
            duration=duration,
            snackbar_x=dp(10),
            snackbar_y=dp(10),
            size_hint_x=(self.width - dp(20)) / self.width
        )
        
        # 添加文本标签
        label = MDLabel(
            text=text,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30)
        )
        snackbar.add_widget(label)
        snackbar.open()
    
    def show_dialog(self, title: str, text: str, buttons: list = None):
        """显示对话框"""
        from kivymd.uix.dialog import MDDialog
        
        if buttons is None:
            from kivymd.uix.button import MDRaisedButton
            buttons = [
                MDRaisedButton(
                    text="确定",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=buttons
        )
        dialog.open()
        return dialog
    
    def show_loading(self, text: str = "加载中..."):
        """显示加载指示器"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.progressbar import MDProgressBar
        
        self.loading_dialog = MDDialog(
            title=text,
            type="custom",
            content_cls=MDProgressBar()
        )
        self.loading_dialog.open()
    
    def hide_loading(self):
        """隐藏加载指示器"""
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.dismiss()
    
    def on_enter(self):
        """屏幕进入时调用"""
        self.logger.info(f"进入屏幕: {self.name}")
    
    def on_leave(self):
        """屏幕离开时调用"""
        self.logger.info(f"离开屏幕: {self.name}")
    
    def refresh_data(self):
        """刷新数据，子类可以重写"""
        pass
