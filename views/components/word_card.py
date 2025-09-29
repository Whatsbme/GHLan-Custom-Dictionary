"""
词条卡片组件
Word Card Component
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.tooltip import MDTooltip
from kivy.metrics import dp
from kivy.uix.image import Image as KivyImage
from kivy.core.window import Window

from utils.logger import get_logger
from utils.helpers import truncate_text, format_datetime


class WordCard(MDCard):
    """词条卡片组件"""
    
    def __init__(self, word_entry=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.word_entry = word_entry
        
        # 设置卡片属性
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(16)
        self.radius = [15, 15, 15, 15]
        self.elevation = 2
        
        self._setup_ui()
        if word_entry:
            self.update_content(word_entry)
    
    def _setup_ui(self):
        """设置UI"""
        # 主布局
        self.main_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        # 左侧内容区域
        self.content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_x=0.8
        )
        
        # 标题行
        self.title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(30)
        )
        
        # 字序号
        self.word_id_label = MDLabel(
            text="",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.3
        )
        self.title_layout.add_widget(self.word_id_label)
        
        # 拉丁写法
        self.latin_label = MDLabel(
            text="",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.7
        )
        self.title_layout.add_widget(self.latin_label)
        
        self.content_layout.add_widget(self.title_layout)
        
        # 音标和词性行
        self.meta_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(25)
        )
        
        # 音标
        self.phonetic_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=0.5
        )
        self.meta_layout.add_widget(self.phonetic_label)
        
        # 词性
        self.word_type_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_x=0.5
        )
        self.meta_layout.add_widget(self.word_type_label)
        
        self.content_layout.add_widget(self.meta_layout)
        
        # 释义行
        self.definition_label = MDLabel(
            text="",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30),
            text_size=(None, None),
            halign="left",
            valign="middle"
        )
        self.content_layout.add_widget(self.definition_label)
        
        # 时间信息
        self.time_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20)
        )
        self.content_layout.add_widget(self.time_label)
        
        self.main_layout.add_widget(self.content_layout)
        
        # 右侧操作区域
        self.action_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(100)
        )
        
        # 图片指示器
        self.image_indicator = MDIconButton(
            icon="image",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_icon_color="Secondary"
        )
        self.image_indicator.opacity = 0.3  # 默认隐藏
        self.action_layout.add_widget(self.image_indicator)
        
        # 收藏按钮
        self.favorite_btn = MDIconButton(
            icon="heart-outline",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_icon_color="Secondary",
            on_release=self._toggle_favorite
        )
        self.action_layout.add_widget(self.favorite_btn)
        
        # 更多操作按钮
        self.more_btn = MDIconButton(
            icon="dots-vertical",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_icon_color="Secondary",
            on_release=self._show_more_options
        )
        self.action_layout.add_widget(self.more_btn)
        
        self.main_layout.add_widget(self.action_layout)
        
        self.add_widget(self.main_layout)
    
    def update_content(self, word_entry):
        """更新卡片内容"""
        self.word_entry = word_entry
        
        # 更新基本信息
        self.word_id_label.text = word_entry.word_id or ""
        self.latin_label.text = word_entry.latin_form or ""
        self.phonetic_label.text = word_entry.phonetic or ""
        self.word_type_label.text = word_entry.word_type or ""
        
        # 更新释义（显示第一个释义）
        if word_entry.definitions:
            definition_text = word_entry.definitions[0].definition_text
            self.definition_label.text = truncate_text(definition_text, 60)
        else:
            self.definition_label.text = "暂无释义"
        
        # 更新时间信息
        self.time_label.text = format_datetime(word_entry.created_at, "%m-%d %H:%M")
        
        # 更新图片指示器
        if word_entry.images:
            self.image_indicator.opacity = 1.0
            self.image_indicator.theme_icon_color = "Primary"
        else:
            self.image_indicator.opacity = 0.3
            self.image_indicator.theme_icon_color = "Secondary"
        
        # 更新收藏按钮
        if word_entry.is_favorite:
            self.favorite_btn.icon = "heart"
            self.favorite_btn.theme_icon_color = "Error"
        else:
            self.favorite_btn.icon = "heart-outline"
            self.favorite_btn.theme_icon_color = "Secondary"
    
    def _toggle_favorite(self, instance):
        """切换收藏状态"""
        if self.word_entry:
            from services.dictionary_service import dictionary_service
            success = dictionary_service.toggle_favorite(self.word_entry.word_id)
            if success:
                # 更新UI
                if self.word_entry.is_favorite:
                    self.favorite_btn.icon = "heart-outline"
                    self.favorite_btn.theme_icon_color = "Secondary"
                    self.word_entry.is_favorite = False
                else:
                    self.favorite_btn.icon = "heart"
                    self.favorite_btn.theme_icon_color = "Error"
                    self.word_entry.is_favorite = True
                
                self.logger.info(f"收藏状态已切换: {self.word_entry.word_id}")
    
    def _show_more_options(self, instance):
        """显示更多操作选项"""
        if self.word_entry:
            from kivymd.uix.menu import MDDropdownMenu
            
            menu_items = [
                {
                    "text": "查看详情",
                    "icon": "eye",
                    "on_release": lambda x: self._view_details()
                },
                {
                    "text": "编辑词条",
                    "icon": "pencil",
                    "on_release": lambda x: self._edit_word()
                },
                {
                    "text": "删除词条",
                    "icon": "delete",
                    "on_release": lambda x: self._delete_word()
                }
            ]
            
            menu = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=4,
            )
            menu.open()
    
    def _view_details(self):
        """查看词条详情"""
        if self.word_entry:
            # 这里应该导航到详情页面
            self.logger.info(f"查看词条详情: {self.word_entry.word_id}")
    
    def _edit_word(self):
        """编辑词条"""
        if self.word_entry:
            # 这里应该导航到编辑页面
            self.logger.info(f"编辑词条: {self.word_entry.word_id}")
    
    def _delete_word(self):
        """删除词条"""
        if self.word_entry:
            from kivymd.uix.dialog import MDDialog
            
            from kivymd.uix.button import MDRaisedButton
            
            dialog = MDDialog(
                title="确认删除",
                text=f"确定要删除词条 '{self.word_entry.word_id}' 吗？",
                buttons=[
                    MDRaisedButton(
                        text="取消",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="删除",
                        on_release=lambda x: self._confirm_delete(dialog)
                    )
                ]
            )
            dialog.open()
    
    def _confirm_delete(self, dialog):
        """确认删除"""
        if self.word_entry:
            from services.dictionary_service import dictionary_service
            success = dictionary_service.delete_word_entry(self.word_entry.word_id)
            if success:
                self.logger.info(f"词条已删除: {self.word_entry.word_id}")
                # 这里应该刷新列表或移除卡片
            else:
                self.logger.error(f"删除词条失败: {self.word_entry.word_id}")
        
        dialog.dismiss()
    
    def on_touch_down(self, touch):
        """处理触摸事件"""
        if self.collide_point(*touch.pos):
            # 点击卡片时显示详情
            if self.word_entry:
                self._view_details()
            return True
        return super().on_touch_down(touch)

