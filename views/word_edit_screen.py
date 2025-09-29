"""
词条编辑界面
Word Edit Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.metrics import dp

from .base_screen import BaseScreen
from .components.image_picker import ImagePicker
from utils.logger import get_logger
from utils.validators import Validators
from services.dictionary_service import dictionary_service


class WordEditScreen(BaseScreen):
    """词条编辑界面"""
    
    def __init__(self, word_entry=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.word_entry = word_entry
        self.is_edit_mode = word_entry is not None
        
        self._setup_ui()
        if word_entry:
            self._load_word_data(word_entry)
    
    def get_screen_title(self) -> str:
        return "编辑词条" if self.is_edit_mode else "添加词条"
    
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
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 保存按钮
        self.save_fab = MDFloatingActionButton(
            icon="content-save",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self._save_word
        )
        self.content_layout.add_widget(self.save_fab)
    
    def _create_basic_info_card(self):
        """创建基本信息卡片"""
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
            text="基本信息",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 字序号
        self.word_id_field = MDTextField(
            hint_text="字序号 *",
            mode="rectangle",
            required=True
        )
        layout.add_widget(self.word_id_field)
        
        # 拉丁写法
        self.latin_field = MDTextField(
            hint_text="拉丁写法 *",
            mode="rectangle",
            required=True
        )
        layout.add_widget(self.latin_field)
        
        # 音标和词性行
        meta_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        self.phonetic_field = MDTextField(
            hint_text="音标",
            mode="rectangle",
            size_hint_x=0.5
        )
        meta_layout.add_widget(self.phonetic_field)
        
        self.word_type_field = MDTextField(
            hint_text="词性",
            mode="rectangle",
            size_hint_x=0.5
        )
        meta_layout.add_widget(self.word_type_field)
        
        layout.add_widget(meta_layout)
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
            spacing=dp(16)
        )
        
        # 标题和添加按钮
        title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        title = MDLabel(
            text="释义",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.8
        )
        title_layout.add_widget(title)
        
        add_def_btn = MDRaisedButton(
            text="添加",
            size_hint_x=0.2,
            on_release=self._add_definition
        )
        title_layout.add_widget(add_def_btn)
        
        layout.add_widget(title_layout)
        
        # 释义容器
        self.definitions_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
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
            spacing=dp(16)
        )
        
        # 标题和添加按钮
        title_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        title = MDLabel(
            text="例句",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_x=0.8
        )
        title_layout.add_widget(title)
        
        add_example_btn = MDRaisedButton(
            text="添加",
            size_hint_x=0.2,
            on_release=self._add_example
        )
        title_layout.add_widget(add_example_btn)
        
        layout.add_widget(title_layout)
        
        # 例句容器
        self.examples_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
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
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="字型图片",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 图片选择器
        self.image_picker = ImagePicker()
        layout.add_widget(self.image_picker)
        
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
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="备注",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 备注输入框
        self.notes_field = MDTextField(
            hint_text="备注信息",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )
        layout.add_widget(self.notes_field)
        
        card.add_widget(layout)
        
        return card
    
    def _add_definition(self, instance):
        """添加释义"""
        definition_card = MDCard(
            padding=dp(12),
            radius=[8, 8, 8, 8],
            size_hint_y=None,
            height=dp(80)
        )
        
        definition_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        definition_field = MDTextField(
            hint_text="释义内容",
            mode="rectangle",
            size_hint_x=0.8,
            multiline=True
        )
        definition_layout.add_widget(definition_field)
        
        delete_btn = MDRaisedButton(
            text="删除",
            size_hint_x=0.2,
            md_bg_color=self.theme_cls.error_color,
            on_release=lambda x: self._remove_definition(definition_card)
        )
        definition_layout.add_widget(delete_btn)
        
        definition_card.add_widget(definition_layout)
        self.definitions_container.add_widget(definition_card)
    
    def _remove_definition(self, definition_card):
        """删除释义"""
        self.definitions_container.remove_widget(definition_card)
    
    def _add_example(self, instance):
        """添加例句"""
        example_card = MDCard(
            padding=dp(12),
            radius=[8, 8, 8, 8],
            size_hint_y=None,
            height=dp(120)
        )
        
        example_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 例句内容
        example_field = MDTextField(
            hint_text="例句内容",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(60)
        )
        example_layout.add_widget(example_field)
        
        # 翻译和删除按钮行
        bottom_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        translation_field = MDTextField(
            hint_text="翻译",
            mode="rectangle",
            size_hint_x=0.7
        )
        bottom_layout.add_widget(translation_field)
        
        delete_btn = MDRaisedButton(
            text="删除",
            size_hint_x=0.3,
            md_bg_color=self.theme_cls.error_color,
            on_release=lambda x: self._remove_example(example_card)
        )
        bottom_layout.add_widget(delete_btn)
        
        example_layout.add_widget(bottom_layout)
        example_card.add_widget(example_layout)
        self.examples_container.add_widget(example_card)
    
    def _remove_example(self, example_card):
        """删除例句"""
        self.examples_container.remove_widget(example_card)
    
    def _load_word_data(self, word_entry):
        """加载词条数据"""
        # 基本信息
        self.word_id_field.text = word_entry.word_id or ""
        self.latin_field.text = word_entry.latin_form or ""
        self.phonetic_field.text = word_entry.phonetic or ""
        self.word_type_field.text = word_entry.word_type or ""
        self.notes_field.text = word_entry.notes or ""
        
        # 释义
        for definition in word_entry.definitions:
            self._add_definition(None)
            # 获取最后一个添加的释义输入框
            last_card = self.definitions_container.children[0]
            definition_field = last_card.children[0].children[1]  # 获取输入框
            definition_field.text = definition.definition_text
        
        # 例句
        for example in word_entry.examples:
            self._add_example(None)
            # 获取最后一个添加的例句输入框
            last_card = self.examples_container.children[0]
            example_layout = last_card.children[0]
            example_field = example_layout.children[1]  # 例句输入框
            translation_field = example_layout.children[0].children[0]  # 翻译输入框
            example_field.text = example.example_text
            translation_field.text = example.translation or ""
        
        # 图片
        if word_entry.images:
            # 这里需要处理图片数据
            pass
    
    def _save_word(self, instance):
        """保存词条"""
        try:
            # 验证基本信息
            word_id = self.word_id_field.text.strip()
            latin_form = self.latin_field.text.strip()
            
            if not word_id or not latin_form:
                self.show_snackbar("字序号和拉丁写法不能为空")
                return
            
            # 验证字序号
            word_id_validation = Validators.validate_word_id(word_id)
            if not word_id_validation['valid']:
                self.show_snackbar(f"字序号验证失败: {', '.join(word_id_validation['errors'])}")
                return
            
            # 验证拉丁写法
            latin_validation = Validators.validate_latin_form(latin_form)
            if not latin_validation['valid']:
                self.show_snackbar(f"拉丁写法验证失败: {', '.join(latin_validation['errors'])}")
                return
            
            # 收集释义
            definitions = []
            for definition_card in self.definitions_container.children:
                definition_field = definition_card.children[0].children[1]
                definition_text = definition_field.text.strip()
                if definition_text:
                    definitions.append(definition_text)
            
            # 验证释义
            if not definitions:
                self.show_snackbar("至少需要一个释义")
                return
            
            definitions_validation = Validators.validate_definitions(definitions)
            if not definitions_validation['valid']:
                self.show_snackbar(f"释义验证失败: {', '.join(definitions_validation['errors'])}")
                return
            
            # 收集例句
            examples = []
            for example_card in self.examples_container.children:
                example_layout = example_card.children[0]
                example_field = example_layout.children[1]
                translation_field = example_layout.children[0].children[0]
                
                example_text = example_field.text.strip()
                translation_text = translation_field.text.strip()
                
                if example_text:
                    examples.append({
                        'text': example_text,
                        'translation': translation_text
                    })
            
            # 验证例句
            if examples:
                examples_validation = Validators.validate_examples(examples)
                if not examples_validation['valid']:
                    self.show_snackbar(f"例句验证失败: {', '.join(examples_validation['errors'])}")
                    return
            
            # 准备词条数据
            word_data = {
                'word_id': word_id,
                'latin_form': latin_form,
                'phonetic': self.phonetic_field.text.strip() or None,
                'word_type': self.word_type_field.text.strip() or None,
                'definitions': definitions,
                'examples': examples,
                'notes': self.notes_field.text.strip() or None
            }
            
            # 保存词条
            if self.is_edit_mode:
                success = dictionary_service.update_word_entry(self.word_entry.word_id, word_data)
                action = "更新"
            else:
                success = dictionary_service.add_word_entry(word_data)
                action = "添加"
            
            if success:
                self.logger.info(f"词条{action}成功: {word_id}")
                self.show_snackbar(f"词条{action}成功")
                # 这里应该返回上一页或刷新列表
            else:
                self.logger.error(f"词条{action}失败: {word_id}")
                self.show_snackbar(f"词条{action}失败")
                
        except Exception as e:
            self.logger.error(f"保存词条失败: {e}")
            self.show_snackbar("保存失败，请检查输入")
    
    def refresh_data(self):
        """刷新数据"""
        if self.word_entry:
            self._load_word_data(self.word_entry)

