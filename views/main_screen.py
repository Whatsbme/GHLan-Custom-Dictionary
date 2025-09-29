"""
主界面
Main Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from .base_screen import BaseScreen
from utils.logger import get_logger


class MainScreen(BaseScreen):
    """主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self._setup_navigation()
        self._setup_content()
    
    def get_screen_title(self) -> str:
        return "离线词典"
    
    def _setup_navigation(self):
        """设置导航抽屉"""
        # 导航布局
        self.nav_layout = MDNavigationLayout()
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.nav_layout)
        
        # 导航抽屉
        self.nav_drawer = MDNavigationDrawer(
            id="nav_drawer",
            radius=[0, 16, 16, 0],
        )
        
        # 抽屉内容
        drawer_content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8)
        )
        
        # 用户信息区域
        user_info = MDCard(
            size_hint_y=None,
            height=dp(100),
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        user_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )
        
        # 用户头像
        avatar = MDIconButton(
            icon="account-circle",
            size_hint=(None, None),
            size=(dp(48), dp(48))
        )
        user_layout.add_widget(avatar)
        
        # 用户信息
        user_text = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )
        user_text.add_widget(MDLabel(
            text="离线词典用户",
            theme_text_color="Primary",
            font_style="H6"
        ))
        user_text.add_widget(MDLabel(
            text="本地词库管理",
            theme_text_color="Secondary",
            font_style="Caption"
        ))
        user_layout.add_widget(user_text)
        
        user_info.add_widget(user_layout)
        drawer_content.add_widget(user_info)
        
        # 导航菜单
        nav_list = MDList()
        
        # 主菜单项
        menu_items = [
            ("home", "词库首页", "home"),
            ("search", "搜索词条", "magnify"),
            ("favorites", "收藏夹", "heart"),
            ("add", "添加词条", "plus"),
            ("tools", "工具", "tools"),
            ("settings", "设置", "cog"),
            ("about", "关于", "information")
        ]
        
        for screen_name, title, icon in menu_items:
            item = OneLineListItem(
                text=title,
                on_release=lambda x, name=screen_name: self._navigate_to_screen(name)
            )
            item.add_widget(MDIconButton(
                icon=icon,
                pos_hint={"center_y": 0.5},
                x=dp(12)
            ))
            nav_list.add_widget(item)
        
        drawer_content.add_widget(nav_list)
        self.nav_drawer.add_widget(drawer_content)
        
        # 主内容区域
        self.screen_manager = MDScreenManager()
        self.nav_layout.add_widget(self.screen_manager)
        
        # 添加导航抽屉
        self.nav_layout.add_widget(self.nav_drawer)
    
    def _setup_content(self):
        """设置主内容"""
        # 创建主屏幕内容
        main_content = MDScreen(name="home")
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(16)
        )
        
        # 搜索区域
        search_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        search_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )
        
        # 搜索标题
        search_title = MDLabel(
            text="快速搜索",
            theme_text_color="Primary",
            font_style="H6"
        )
        search_layout.add_widget(search_title)
        
        # 搜索框
        search_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )
        
        self.search_field = MDTextField(
            hint_text="输入词条ID、拉丁写法或释义关键词",
            mode="rectangle",
            size_hint_x=0.8
        )
        search_box.add_widget(self.search_field)
        
        search_btn = MDRaisedButton(
            text="搜索",
            size_hint_x=0.2,
            on_release=self._on_search
        )
        search_box.add_widget(search_btn)
        
        search_layout.add_widget(search_box)
        search_card.add_widget(search_layout)
        main_layout.add_widget(search_card)
        
        # 统计信息
        stats_card = MDCard(
            size_hint_y=None,
            height=dp(100),
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        stats_layout = MDGridLayout(
            cols=3,
            spacing=dp(20),
            size_hint_y=None,
            height=dp(60)
        )
        
        # 词条总数
        total_item = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )
        total_item.add_widget(MDLabel(
            text="0",
            theme_text_color="Primary",
            font_style="H4",
            halign="center"
        ))
        total_item.add_widget(MDLabel(
            text="总词条",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center"
        ))
        stats_layout.add_widget(total_item)
        
        # 收藏数
        favorite_item = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )
        favorite_item.add_widget(MDLabel(
            text="0",
            theme_text_color="Primary",
            font_style="H4",
            halign="center"
        ))
        favorite_item.add_widget(MDLabel(
            text="收藏",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center"
        ))
        stats_layout.add_widget(favorite_item)
        
        # 最近添加
        recent_item = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )
        recent_item.add_widget(MDLabel(
            text="0",
            theme_text_color="Primary",
            font_style="H4",
            halign="center"
        ))
        recent_item.add_widget(MDLabel(
            text="最近",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center"
        ))
        stats_layout.add_widget(recent_item)
        
        stats_card.add_widget(stats_layout)
        main_layout.add_widget(stats_card)
        
        # 最近词条
        recent_card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        recent_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )
        
        recent_title = MDLabel(
            text="最近添加的词条",
            theme_text_color="Primary",
            font_style="H6"
        )
        recent_layout.add_widget(recent_title)
        
        # 最近词条列表
        self.recent_list = MDList()
        recent_layout.add_widget(self.recent_list)
        
        recent_card.add_widget(recent_layout)
        main_layout.add_widget(recent_card)
        
        main_content.add_widget(main_layout)
        self.screen_manager.add_widget(main_content)
        
        # 加载数据
        self._load_home_data()
    
    def _navigate_to_screen(self, screen_name: str):
        """导航到指定屏幕"""
        self.logger.info(f"导航到屏幕: {screen_name}")
        
        # 关闭导航抽屉
        self.nav_drawer.set_state("close")
        
        # 根据屏幕名称执行相应操作
        if screen_name == "home":
            self.screen_manager.current = "home"
        elif screen_name == "search":
            self._show_search_screen()
        elif screen_name == "favorites":
            self._show_favorites_screen()
        elif screen_name == "add":
            self._show_add_word_screen()
        elif screen_name == "tools":
            self._show_tools_screen()
        elif screen_name == "settings":
            self._show_settings_screen()
        elif screen_name == "about":
            self._show_about_screen()
    
    def _on_search(self, instance):
        """搜索按钮点击事件"""
        query = self.search_field.text.strip()
        if query:
            self.logger.info(f"搜索: {query}")
            # 这里实现搜索逻辑
            self.show_snackbar(f"搜索: {query}")
        else:
            self.show_snackbar("请输入搜索关键词")
    
    def _load_home_data(self):
        """加载首页数据"""
        try:
            # 这里加载统计数据
            # 暂时使用模拟数据
            pass
        except Exception as e:
            self.logger.error(f"加载首页数据失败: {e}")
    
    def _show_search_screen(self):
        """显示搜索屏幕"""
        self.show_snackbar("搜索功能开发中...")
    
    def _show_favorites_screen(self):
        """显示收藏夹屏幕"""
        self.show_snackbar("收藏夹功能开发中...")
    
    def _show_add_word_screen(self):
        """显示添加词条屏幕"""
        self.show_snackbar("添加词条功能开发中...")
    
    def _show_tools_screen(self):
        """显示工具屏幕"""
        self.show_snackbar("工具功能开发中...")
    
    def _show_settings_screen(self):
        """显示设置屏幕"""
        self.show_snackbar("设置功能开发中...")
    
    def _show_about_screen(self):
        """显示关于屏幕"""
        self.show_dialog(
            title="关于离线词典",
            text="离线词典 v1.0.0\n\n一个功能完整的移动端Python离线词典应用\n支持本地词库管理、搜索、编辑、导出等功能"
        )
