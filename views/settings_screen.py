"""
设置界面
Settings Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.slider import MDSlider
from kivy.metrics import dp

from .base_screen import BaseScreen
from utils.logger import get_logger
from app.config import config


class SettingsScreen(BaseScreen):
    """设置界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self._setup_ui()
        self._load_settings()
    
    def get_screen_title(self) -> str:
        return "设置"
    
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
        
        # 基本设置卡片
        self.basic_settings_card = self._create_basic_settings_card()
        self.main_container.add_widget(self.basic_settings_card)
        
        # 主题设置卡片
        self.theme_settings_card = self._create_theme_settings_card()
        self.main_container.add_widget(self.theme_settings_card)
        
        # 字体设置卡片
        self.font_settings_card = self._create_font_settings_card()
        self.main_container.add_widget(self.font_settings_card)
        
        # 搜索设置卡片
        self.search_settings_card = self._create_search_settings_card()
        self.main_container.add_widget(self.search_settings_card)
        
        # 数据设置卡片
        self.data_settings_card = self._create_data_settings_card()
        self.main_container.add_widget(self.data_settings_card)
        
        # 关于卡片
        self.about_card = self._create_about_card()
        self.main_container.add_widget(self.about_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 保存按钮
        self.save_fab = MDFloatingActionButton(
            icon="content-save",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self._save_settings
        )
        self.content_layout.add_widget(self.save_fab)
    
    def _create_basic_settings_card(self):
        """创建基本设置卡片"""
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
            text="基本设置",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 应用名称
        app_name_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        app_name_label = MDLabel(
            text="应用名称",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        app_name_layout.add_widget(app_name_label)
        
        self.app_name_field = MDTextField(
            hint_text="GHLan自定义字典",
            mode="rectangle",
            size_hint_x=0.7
        )
        app_name_layout.add_widget(self.app_name_field)
        
        layout.add_widget(app_name_layout)
        
        # 自动保存
        auto_save_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        auto_save_label = MDLabel(
            text="自动保存",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        auto_save_layout.add_widget(auto_save_label)
        
        self.auto_save_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        auto_save_layout.add_widget(self.auto_save_switch)
        
        layout.add_widget(auto_save_layout)
        
        # 启动时显示欢迎页
        welcome_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        welcome_label = MDLabel(
            text="启动时显示欢迎页",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        welcome_layout.add_widget(welcome_label)
        
        self.welcome_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        welcome_layout.add_widget(self.welcome_switch)
        
        layout.add_widget(welcome_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_theme_settings_card(self):
        """创建主题设置卡片"""
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
            text="主题设置",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 主题样式
        theme_style_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        theme_style_label = MDLabel(
            text="主题样式",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        theme_style_layout.add_widget(theme_style_label)
        
        self.theme_style_btn = MDRaisedButton(
            text="浅色",
            size_hint_x=0.7,
            on_release=self._show_theme_style_menu
        )
        theme_style_layout.add_widget(self.theme_style_btn)
        
        layout.add_widget(theme_style_layout)
        
        # 主色调
        primary_color_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        primary_color_label = MDLabel(
            text="主色调",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        primary_color_layout.add_widget(primary_color_label)
        
        self.primary_color_btn = MDRaisedButton(
            text="蓝色",
            size_hint_x=0.7,
            on_release=self._show_primary_color_menu
        )
        primary_color_layout.add_widget(self.primary_color_btn)
        
        layout.add_widget(primary_color_layout)
        
        # 强调色
        accent_color_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        accent_color_label = MDLabel(
            text="强调色",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        accent_color_layout.add_widget(accent_color_label)
        
        self.accent_color_btn = MDRaisedButton(
            text="橙色",
            size_hint_x=0.7,
            on_release=self._show_accent_color_menu
        )
        accent_color_layout.add_widget(self.accent_color_btn)
        
        layout.add_widget(accent_color_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_font_settings_card(self):
        """创建字体设置卡片"""
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
            text="字体设置",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 字体大小
        font_size_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        font_size_label = MDLabel(
            text="字体大小",
            theme_text_color="Primary",
            font_style="Body1"
        )
        font_size_layout.add_widget(font_size_label)
        
        self.font_size_slider = MDSlider(
            min=12,
            max=24,
            value=16,
            step=1,
            size_hint_y=None,
            height=dp(40)
        )
        self.font_size_slider.bind(value=self._on_font_size_change)
        font_size_layout.add_widget(self.font_size_slider)
        
        self.font_size_value = MDLabel(
            text="16px",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20)
        )
        font_size_layout.add_widget(self.font_size_value)
        
        layout.add_widget(font_size_layout)
        
        # 字体族
        font_family_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        font_family_label = MDLabel(
            text="字体族",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        font_family_layout.add_widget(font_family_label)
        
        self.font_family_btn = MDRaisedButton(
            text="默认",
            size_hint_x=0.7,
            on_release=self._show_font_family_menu
        )
        font_family_layout.add_widget(self.font_family_btn)
        
        layout.add_widget(font_family_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_search_settings_card(self):
        """创建搜索设置卡片"""
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
            text="搜索设置",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 默认搜索类型
        default_search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        default_search_label = MDLabel(
            text="默认搜索类型",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.5
        )
        default_search_layout.add_widget(default_search_label)
        
        self.default_search_btn = MDRaisedButton(
            text="全部",
            size_hint_x=0.5,
            on_release=self._show_default_search_menu
        )
        default_search_layout.add_widget(self.default_search_btn)
        
        layout.add_widget(default_search_layout)
        
        # 搜索历史
        search_history_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        search_history_label = MDLabel(
            text="保存搜索历史",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        search_history_layout.add_widget(search_history_label)
        
        self.search_history_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        search_history_layout.add_widget(self.search_history_switch)
        
        layout.add_widget(search_history_layout)
        
        # 模糊搜索
        fuzzy_search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        fuzzy_search_label = MDLabel(
            text="默认启用模糊搜索",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        fuzzy_search_layout.add_widget(fuzzy_search_label)
        
        self.fuzzy_search_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        fuzzy_search_layout.add_widget(self.fuzzy_search_switch)
        
        layout.add_widget(fuzzy_search_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_data_settings_card(self):
        """创建数据设置卡片"""
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
            text="数据设置",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 数据备份
        backup_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        backup_btn = MDRaisedButton(
            text="备份数据",
            size_hint_x=0.5,
            on_release=self._backup_data
        )
        backup_layout.add_widget(backup_btn)
        
        restore_btn = MDRaisedButton(
            text="恢复数据",
            size_hint_x=0.5,
            on_release=self._restore_data
        )
        backup_layout.add_widget(restore_btn)
        
        layout.add_widget(backup_layout)
        
        # 清除数据
        clear_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        clear_cache_btn = MDRaisedButton(
            text="清除缓存",
            size_hint_x=0.5,
            on_release=self._clear_cache
        )
        clear_layout.add_widget(clear_cache_btn)
        
        clear_data_btn = MDRaisedButton(
            text="清除所有数据",
            size_hint_x=0.5,
            md_bg_color=self.theme_cls.error_color,
            on_release=self._clear_all_data
        )
        clear_layout.add_widget(clear_data_btn)
        
        layout.add_widget(clear_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_about_card(self):
        """创建关于卡片"""
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
            text="关于",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 应用信息
        app_info = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        app_name = MDLabel(
            text="GHLan自定义字典",
            theme_text_color="Primary",
            font_style="H6"
        )
        app_info.add_widget(app_name)
        
        app_version = MDLabel(
            text="版本 1.0.0",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        app_info.add_widget(app_version)
        
        app_description = MDLabel(
            text="一个功能完整的移动端Python离线词典应用",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        app_info.add_widget(app_description)
        
        layout.add_widget(app_info)
        
        # 功能按钮
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        help_btn = MDRaisedButton(
            text="帮助",
            size_hint_x=0.33,
            on_release=self._show_help
        )
        buttons_layout.add_widget(help_btn)
        
        feedback_btn = MDRaisedButton(
            text="反馈",
            size_hint_x=0.33,
            on_release=self._show_feedback
        )
        buttons_layout.add_widget(feedback_btn)
        
        update_btn = MDRaisedButton(
            text="检查更新",
            size_hint_x=0.33,
            on_release=self._check_update
        )
        buttons_layout.add_widget(update_btn)
        
        layout.add_widget(buttons_layout)
        
        card.add_widget(layout)
        return card
    
    def _load_settings(self):
        """加载设置"""
        try:
            # 加载基本设置
            self.app_name_field.text = config.get('APP', 'name', 'GHLan自定义字典')
            self.auto_save_switch.active = config.getboolean('APP', 'auto_save', True)
            self.welcome_switch.active = config.getboolean('APP', 'show_welcome', True)
            
            # 加载主题设置
            theme_style = config.get('THEME', 'style', 'light')
            self.theme_style_btn.text = "深色" if theme_style == 'dark' else "浅色"
            
            primary_palette = config.get('THEME', 'primary_palette', 'Blue')
            self.primary_color_btn.text = self._get_palette_name(primary_palette)
            
            accent_palette = config.get('THEME', 'accent_palette', 'Orange')
            self.accent_color_btn.text = self._get_palette_name(accent_palette)
            
            # 加载字体设置
            font_size = config.getint('FONT', 'size', 16)
            self.font_size_slider.value = font_size
            self.font_size_value.text = f"{font_size}px"
            
            font_family = config.get('FONT', 'family', 'default')
            self.font_family_btn.text = self._get_font_family_name(font_family)
            
            # 加载搜索设置
            default_search = config.get('SEARCH', 'default_type', 'all')
            self.default_search_btn.text = self._get_search_type_name(default_search)
            
            self.search_history_switch.active = config.getboolean('SEARCH', 'save_history', True)
            self.fuzzy_search_switch.active = config.getboolean('SEARCH', 'default_fuzzy', True)
            
        except Exception as e:
            self.logger.error(f"加载设置失败: {e}")
    
    def _save_settings(self, instance):
        """保存设置"""
        try:
            # 保存基本设置
            config.set('APP', 'name', self.app_name_field.text)
            config.set('APP', 'auto_save', str(self.auto_save_switch.active))
            config.set('APP', 'show_welcome', str(self.welcome_switch.active))
            
            # 保存主题设置
            theme_style = 'dark' if self.theme_style_btn.text == '深色' else 'light'
            config.set('THEME', 'style', theme_style)
            
            primary_palette = self._get_palette_key(self.primary_color_btn.text)
            config.set('THEME', 'primary_palette', primary_palette)
            
            accent_palette = self._get_palette_key(self.accent_color_btn.text)
            config.set('THEME', 'accent_palette', accent_palette)
            
            # 保存字体设置
            config.set('FONT', 'size', str(int(self.font_size_slider.value)))
            config.set('FONT', 'family', self._get_font_family_key(self.font_family_btn.text))
            
            # 保存搜索设置
            config.set('SEARCH', 'default_type', self._get_search_type_key(self.default_search_btn.text))
            config.set('SEARCH', 'save_history', str(self.search_history_switch.active))
            config.set('SEARCH', 'default_fuzzy', str(self.fuzzy_search_switch.active))
            
            # 保存配置
            config.save()
            
            self.show_snackbar("设置已保存")
            self.logger.info("设置保存成功")
            
        except Exception as e:
            self.logger.error(f"保存设置失败: {e}")
            self.show_snackbar("保存设置失败")
    
    def _show_theme_style_menu(self, instance):
        """显示主题样式菜单"""
        menu_items = [
            {
                "text": "浅色",
                "on_release": lambda x: self._set_theme_style('light', '浅色')
            },
            {
                "text": "深色",
                "on_release": lambda x: self._set_theme_style('dark', '深色')
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_theme_style(self, style, display_name):
        """设置主题样式"""
        self.theme_style_btn.text = display_name
        self.logger.info(f"主题样式已设置为: {display_name}")
    
    def _show_primary_color_menu(self, instance):
        """显示主色调菜单"""
        colors = [
            ('Blue', '蓝色'),
            ('Red', '红色'),
            ('Green', '绿色'),
            ('Purple', '紫色'),
            ('Orange', '橙色'),
            ('Teal', '青色'),
            ('Indigo', '靛蓝'),
            ('Pink', '粉色')
        ]
        
        menu_items = []
        for key, name in colors:
            menu_items.append({
                "text": name,
                "on_release": lambda x, k=key, n=name: self._set_primary_color(k, n)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_primary_color(self, color_key, color_name):
        """设置主色调"""
        self.primary_color_btn.text = color_name
        self.logger.info(f"主色调已设置为: {color_name}")
    
    def _show_accent_color_menu(self, instance):
        """显示强调色菜单"""
        colors = [
            ('Orange', '橙色'),
            ('Red', '红色'),
            ('Green', '绿色'),
            ('Blue', '蓝色'),
            ('Purple', '紫色'),
            ('Teal', '青色'),
            ('Indigo', '靛蓝'),
            ('Pink', '粉色')
        ]
        
        menu_items = []
        for key, name in colors:
            menu_items.append({
                "text": name,
                "on_release": lambda x, k=key, n=name: self._set_accent_color(k, n)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_accent_color(self, color_key, color_name):
        """设置强调色"""
        self.accent_color_btn.text = color_name
        self.logger.info(f"强调色已设置为: {color_name}")
    
    def _show_font_family_menu(self, instance):
        """显示字体族菜单"""
        fonts = [
            ('default', '默认'),
            ('Roboto', 'Roboto'),
            ('Arial', 'Arial'),
            ('Times', 'Times'),
            ('Courier', 'Courier')
        ]
        
        menu_items = []
        for key, name in fonts:
            menu_items.append({
                "text": name,
                "on_release": lambda x, k=key, n=name: self._set_font_family(k, n)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_font_family(self, font_key, font_name):
        """设置字体族"""
        self.font_family_btn.text = font_name
        self.logger.info(f"字体族已设置为: {font_name}")
    
    def _on_font_size_change(self, instance, value):
        """字体大小改变事件"""
        self.font_size_value.text = f"{int(value)}px"
    
    def _show_default_search_menu(self, instance):
        """显示默认搜索类型菜单"""
        search_types = [
            ('all', '全部'),
            ('word_id', '字序号'),
            ('latin_form', '拉丁写法'),
            ('phonetic', '音标'),
            ('definitions', '释义')
        ]
        
        menu_items = []
        for key, name in search_types:
            menu_items.append({
                "text": name,
                "on_release": lambda x, k=key, n=name: self._set_default_search_type(k, n)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_default_search_type(self, search_key, search_name):
        """设置默认搜索类型"""
        self.default_search_btn.text = search_name
        self.logger.info(f"默认搜索类型已设置为: {search_name}")
    
    def _backup_data(self, instance):
        """备份数据"""
        self.show_snackbar("数据备份功能开发中...")
    
    def _restore_data(self, instance):
        """恢复数据"""
        self.show_snackbar("数据恢复功能开发中...")
    
    def _clear_cache(self, instance):
        """清除缓存"""
        self.show_snackbar("缓存清除功能开发中...")
    
    def _clear_all_data(self, instance):
        """清除所有数据"""
        self.show_dialog(
            title="确认清除",
            text="确定要清除所有数据吗？此操作不可撤销！",
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: None
                ),
                MDRaisedButton(
                    text="清除",
                    md_bg_color=self.theme_cls.error_color,
                    on_release=lambda x: self._confirm_clear_data()
                )
            ]
        )
    
    def _confirm_clear_data(self):
        """确认清除数据"""
        self.show_snackbar("清除数据功能开发中...")
    
    def _show_help(self, instance):
        """显示帮助"""
        self.show_dialog(
            title="帮助",
            text="GHLan自定义字典使用帮助\n\n1. 词条管理：添加、编辑、删除词条\n2. 搜索功能：支持多字段搜索和正则表达式\n3. 设置：自定义主题、字体和搜索选项\n4. 数据管理：备份和恢复数据"
        )
    
    def _show_feedback(self, instance):
        """显示反馈"""
        self.show_snackbar("反馈功能开发中...")
    
    def _check_update(self, instance):
        """检查更新"""
        self.show_snackbar("当前已是最新版本")
    
    def _get_palette_name(self, palette_key):
        """获取调色板名称"""
        palette_names = {
            'Blue': '蓝色',
            'Red': '红色',
            'Green': '绿色',
            'Purple': '紫色',
            'Orange': '橙色',
            'Teal': '青色',
            'Indigo': '靛蓝',
            'Pink': '粉色'
        }
        return palette_names.get(palette_key, palette_key)
    
    def _get_palette_key(self, palette_name):
        """获取调色板键"""
        palette_keys = {
            '蓝色': 'Blue',
            '红色': 'Red',
            '绿色': 'Green',
            '紫色': 'Purple',
            '橙色': 'Orange',
            '青色': 'Teal',
            '靛蓝': 'Indigo',
            '粉色': 'Pink'
        }
        return palette_keys.get(palette_name, 'Blue')
    
    def _get_font_family_name(self, font_key):
        """获取字体族名称"""
        font_names = {
            'default': '默认',
            'Roboto': 'Roboto',
            'Arial': 'Arial',
            'Times': 'Times',
            'Courier': 'Courier'
        }
        return font_names.get(font_key, '默认')
    
    def _get_font_family_key(self, font_name):
        """获取字体族键"""
        font_keys = {
            '默认': 'default',
            'Roboto': 'Roboto',
            'Arial': 'Arial',
            'Times': 'Times',
            'Courier': 'Courier'
        }
        return font_keys.get(font_name, 'default')
    
    def _get_search_type_name(self, search_key):
        """获取搜索类型名称"""
        search_names = {
            'all': '全部',
            'word_id': '字序号',
            'latin_form': '拉丁写法',
            'phonetic': '音标',
            'definitions': '释义'
        }
        return search_names.get(search_key, '全部')
    
    def _get_search_type_key(self, search_name):
        """获取搜索类型键"""
        search_keys = {
            '全部': 'all',
            '字序号': 'word_id',
            '拉丁写法': 'latin_form',
            '音标': 'phonetic',
            '释义': 'definitions'
        }
        return search_keys.get(search_name, 'all')
    
    def refresh_data(self):
        """刷新数据"""
        self._load_settings()
