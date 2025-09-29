"""
词条详情界面
Word Detail Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.image import Image as KivyImage

from .base_screen import BaseScreen
from utils.logger import get_logger
from utils.helpers import format_datetime, truncate_text
from services.dictionary_service import dictionary_service


class WordDetailScreen(BaseScreen):
    """词条详情界面"""
    
    def __init__(self, word_entry=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.word_entry = word_entry
        
        self._setup_ui()
        if word_entry:
            self.update_content(word_entry)
    
    def get_screen_title(self) -> str:
        return "词条详情"
    
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
        
        # 基本信息卡片
        self.basic_info_card = self._create_basic_info_card()
        self.main_container.add_widget(self.basic_info_card)
        
        # 释义卡片
        self.definitions_card = self._create_definitions_card()
        self.main_container.add_widget(self.definitions_card)
        
        # 例句卡片
        self.examples_card = self._create_examples_card()
        self.main_container.add_widget(self.examples_card)
        
        # 图片卡片
        self.images_card = self._create_images_card()
        self.main_container.add_widget(self.images_card)
        
        # 备注卡片
        self.notes_card = self._create_notes_card()
        self.main_container.add_widget(self.notes_card)
        
        # 时间信息卡片
        self.time_info_card = self._create_time_info_card()
        self.main_container.add_widget(self.time_info_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 浮动操作按钮
        self.fab_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            size_hint=(None, None),
            size=(dp(200), dp(56))
        )
        
        # 编辑按钮
        self.edit_fab = MDFloatingActionButton(
            icon="pencil",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            on_release=self._edit_word
        )
        self.fab_layout.add_widget(self.edit_fab)
        
        # 收藏按钮
        self.favorite_fab = MDFloatingActionButton(
            icon="heart-outline",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            on_release=self._toggle_favorite
        )
        self.fab_layout.add_widget(self.favorite_fab)
        
        # 删除按钮
        self.delete_fab = MDFloatingActionButton(
            icon="delete",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            md_bg_color=self.theme_cls.error_color,
            on_release=self._delete_word
        )
        self.fab_layout.add_widget(self.delete_fab)
        
        self.content_layout.add_widget(self.fab_layout)
    
    def _create_basic_info_card(self):
        """创建基本信息卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="基本信息",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 信息网格
        info_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        
        # 字序号
        self.word_id_label = MDLabel(
            text="字序号: ",
            theme_text_color="Primary",
            font_style="Body1"
        )
        info_grid.add_widget(self.word_id_label)
        
        # 拉丁写法
        self.latin_label = MDLabel(
            text="拉丁写法: ",
            theme_text_color="Primary",
            font_style="Body1"
        )
        info_grid.add_widget(self.latin_label)
        
        # 音标
        self.phonetic_label = MDLabel(
            text="音标: ",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        info_grid.add_widget(self.phonetic_label)
        
        # 词性
        self.word_type_label = MDLabel(
            text="词性: ",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        info_grid.add_widget(self.word_type_label)
        
        layout.add_widget(info_grid)
        card.add_widget(layout)
        
        return card
    
    def _create_definitions_card(self):
        """创建释义卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="释义",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 释义容器
        self.definitions_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None
        )
        self.definitions_container.bind(minimum_height=self.definitions_container.setter('height'))
        
        layout.add_widget(self.definitions_container)
        card.add_widget(layout)
        
        return card
    
    def _create_examples_card(self):
        """创建例句卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="例句",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 例句容器
        self.examples_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None
        )
        self.examples_container.bind(minimum_height=self.examples_container.setter('height'))
        
        layout.add_widget(self.examples_container)
        card.add_widget(layout)
        
        return card
    
    def _create_images_card(self):
        """创建图片卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="字型图片",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 图片容器
        self.images_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.images_container.bind(minimum_height=self.images_container.setter('height'))
        
        layout.add_widget(self.images_container)
        card.add_widget(layout)
        
        return card
    
    def _create_notes_card(self):
        """创建备注卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="备注",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 备注内容
        self.notes_label = MDLabel(
            text="暂无备注",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        layout.add_widget(self.notes_label)
        
        card.add_widget(layout)
        
        return card
    
    def _create_time_info_card(self):
        """创建时间信息卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 标题
        title = MDLabel(
            text="时间信息",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 时间信息
        self.time_info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        self.created_time_label = MDLabel(
            text="创建时间: ",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        self.time_info_layout.add_widget(self.created_time_label)
        
        self.updated_time_label = MDLabel(
            text="更新时间: ",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        self.time_info_layout.add_widget(self.updated_time_label)
        
        layout.add_widget(self.time_info_layout)
        card.add_widget(layout)
        
        return card
    
    def update_content(self, word_entry):
        """更新内容"""
        self.word_entry = word_entry
        
        # 更新基本信息
        self.word_id_label.text = f"字序号: {word_entry.word_id or '无'}"
        self.latin_label.text = f"拉丁写法: {word_entry.latin_form or '无'}"
        self.phonetic_label.text = f"音标: {word_entry.phonetic or '无'}"
        self.word_type_label.text = f"词性: {word_entry.word_type or '无'}"
        
        # 更新释义
        self._update_definitions()
        
        # 更新例句
        self._update_examples()
        
        # 更新图片
        self._update_images()
        
        # 更新备注
        if word_entry.notes:
            self.notes_label.text = word_entry.notes
        else:
            self.notes_label.text = "暂无备注"
        
        # 更新时间信息
        self.created_time_label.text = f"创建时间: {format_datetime(word_entry.created_at)}"
        self.updated_time_label.text = f"更新时间: {format_datetime(word_entry.updated_at)}"
        
        # 更新收藏按钮
        if word_entry.is_favorite:
            self.favorite_fab.icon = "heart"
            self.favorite_fab.md_bg_color = self.theme_cls.error_color
        else:
            self.favorite_fab.icon = "heart-outline"
            self.favorite_fab.md_bg_color = self.theme_cls.primary_color
    
    def _update_definitions(self):
        """更新释义"""
        self.definitions_container.clear_widgets()
        
        if self.word_entry.definitions:
            for i, definition in enumerate(self.word_entry.definitions, 1):
                definition_card = MDCard(
                    padding=dp(12),
                    radius=[8, 8, 8, 8],
                    size_hint_y=None,
                    height=dp(60)
                )
                
                definition_label = MDLabel(
                    text=f"{i}. {definition.definition_text}",
                    theme_text_color="Primary",
                    font_style="Body1",
                    size_hint_y=None,
                    text_size=(None, None),
                    halign="left",
                    valign="middle"
                )
                definition_card.add_widget(definition_label)
                self.definitions_container.add_widget(definition_card)
        else:
            no_def_label = MDLabel(
                text="暂无释义",
                theme_text_color="Secondary",
                font_style="Body1"
            )
            self.definitions_container.add_widget(no_def_label)
    
    def _update_examples(self):
        """更新例句"""
        self.examples_container.clear_widgets()
        
        if self.word_entry.examples:
            for i, example in enumerate(self.word_entry.examples, 1):
                example_card = MDCard(
                    padding=dp(12),
                    radius=[8, 8, 8, 8],
                    size_hint_y=None,
                    height=dp(80)
                )
                
                example_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(5)
                )
                
                example_label = MDLabel(
                    text=f"{i}. {example.example_text}",
                    theme_text_color="Primary",
                    font_style="Body1",
                    size_hint_y=None,
                    text_size=(None, None),
                    halign="left",
                    valign="top"
                )
                example_layout.add_widget(example_label)
                
                if example.translation:
                    translation_label = MDLabel(
                        text=f"翻译: {example.translation}",
                        theme_text_color="Secondary",
                        font_style="Body2",
                        size_hint_y=None,
                        text_size=(None, None),
                        halign="left",
                        valign="top"
                    )
                    example_layout.add_widget(translation_label)
                
                example_card.add_widget(example_layout)
                self.examples_container.add_widget(example_card)
        else:
            no_example_label = MDLabel(
                text="暂无例句",
                theme_text_color="Secondary",
                font_style="Body1"
            )
            self.examples_container.add_widget(no_example_label)
    
    def _update_images(self):
        """更新图片"""
        self.images_container.clear_widgets()
        
        if self.word_entry.images:
            for image in self.word_entry.images:
                image_card = MDCard(
                    padding=dp(12),
                    radius=[8, 8, 8, 8],
                    size_hint_y=None,
                    height=dp(200)
                )
                
                image_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(10)
                )
                
                # 图片显示
                image_widget = KivyImage(
                    size_hint_y=None,
                    height=dp(150),
                    allow_stretch=True,
                    keep_ratio=True
                )
                
                # 这里需要将blob数据转换为可显示的图片
                # 暂时显示占位符
                image_widget.source = "assets/icons/image_placeholder.png"
                
                image_layout.add_widget(image_widget)
                
                # 图片信息
                image_info = MDLabel(
                    text=f"图片类型: {image.image_type}",
                    theme_text_color="Secondary",
                    font_style="Caption",
                    size_hint_y=None,
                    height=dp(20)
                )
                image_layout.add_widget(image_info)
                
                image_card.add_widget(image_layout)
                self.images_container.add_widget(image_card)
        else:
            no_image_label = MDLabel(
                text="暂无图片",
                theme_text_color="Secondary",
                font_style="Body1"
            )
            self.images_container.add_widget(no_image_label)
    
    def _edit_word(self, instance):
        """编辑词条"""
        if self.word_entry:
            self.logger.info(f"编辑词条: {self.word_entry.word_id}")
            # 这里应该导航到编辑界面
            self.show_snackbar("编辑功能开发中...")
    
    def _toggle_favorite(self, instance):
        """切换收藏状态"""
        if self.word_entry:
            success = dictionary_service.toggle_favorite(self.word_entry.word_id)
            if success:
                # 更新UI
                if self.word_entry.is_favorite:
                    self.favorite_fab.icon = "heart-outline"
                    self.favorite_fab.md_bg_color = self.theme_cls.primary_color
                    self.word_entry.is_favorite = False
                else:
                    self.favorite_fab.icon = "heart"
                    self.favorite_fab.md_bg_color = self.theme_cls.error_color
                    self.word_entry.is_favorite = True
                
                self.logger.info(f"收藏状态已切换: {self.word_entry.word_id}")
                self.show_snackbar("收藏状态已更新")
    
    def _delete_word(self, instance):
        """删除词条"""
        if self.word_entry:
            from kivymd.uix.button import MDRaisedButton
            
            dialog = MDDialog(
                title="确认删除",
                text=f"确定要删除词条 '{self.word_entry.word_id}' 吗？\n此操作不可撤销。",
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
            success = dictionary_service.delete_word_entry(self.word_entry.word_id)
            if success:
                self.logger.info(f"词条已删除: {self.word_entry.word_id}")
                self.show_snackbar("词条已删除")
                # 这里应该返回上一页或刷新列表
            else:
                self.logger.error(f"删除词条失败: {self.word_entry.word_id}")
                self.show_snackbar("删除失败")
        
        dialog.dismiss()

