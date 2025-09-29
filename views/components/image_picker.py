"""
图片选择组件
Image Picker Component
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image as KivyImage
from kivy.metrics import dp
from kivy.core.window import Window
import os
from pathlib import Path
import base64
import io

from utils.logger import get_logger
from utils.file_manager import file_manager


class ImagePicker(MDBoxLayout):
    """图片选择组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(200)
        
        self.image_data = None
        self.image_filename = None
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        # 图片显示区域
        self.image_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(10),
            radius=[10, 10, 10, 10]
        )
        
        self.image_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        # 图片预览
        self.image_preview = KivyImage(
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            allow_stretch=True,
            keep_ratio=True
        )
        self.image_layout.add_widget(self.image_preview)
        
        # 图片信息
        self.image_info = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        self.image_name_label = MDLabel(
            text="未选择图片",
            theme_text_color="Primary",
            font_style="Body1"
        )
        self.image_info.add_widget(self.image_name_label)
        
        self.image_size_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        self.image_info.add_widget(self.image_size_label)
        
        self.image_layout.add_widget(self.image_info)
        self.image_card.add_widget(self.image_layout)
        self.add_widget(self.image_card)
        
        # 按钮区域
        self.button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 选择图片按钮
        self.select_btn = MDRaisedButton(
            text="选择图片",
            size_hint_x=0.5,
            on_release=self._show_file_dialog
        )
        self.button_layout.add_widget(self.select_btn)
        
        # 清除图片按钮
        self.clear_btn = MDRaisedButton(
            text="清除",
            size_hint_x=0.5,
            on_release=self._clear_image
        )
        self.button_layout.add_widget(self.clear_btn)
        
        self.add_widget(self.button_layout)
    
    def _show_file_dialog(self, instance):
        """显示文件选择对话框"""
        try:
            from tkinter import filedialog
            import tkinter as tk
            
            # 创建隐藏的根窗口
            root = tk.Tk()
            root.withdraw()
            
            # 打开文件对话框
            file_path = filedialog.askopenfilename(
                title="选择图片文件",
                filetypes=[
                    ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("所有文件", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path:
                self._load_image(file_path)
                
        except ImportError:
            # 如果没有tkinter，使用简单的文件输入
            self._show_simple_file_input()
        except Exception as e:
            self.logger.error(f"显示文件对话框失败: {e}")
            self._show_simple_file_input()
    
    def _show_simple_file_input(self):
        """显示简单的文件输入对话框"""
        dialog = MDDialog(
            title="选择图片文件",
            text="请输入图片文件路径:",
            type="custom",
            content_cls=self._create_file_input_content()
        )
        dialog.open()
    
    def _create_file_input_content(self):
        """创建文件输入内容"""
        from kivymd.uix.textfield import MDTextField
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(100)
        )
        
        self.file_path_field = MDTextField(
            hint_text="图片文件路径",
            mode="rectangle"
        )
        content.add_widget(self.file_path_field)
        
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        ok_btn = MDRaisedButton(
            text="确定",
            size_hint_x=0.5,
            on_release=lambda x: self._load_image_from_path()
        )
        button_layout.add_widget(ok_btn)
        
        cancel_btn = MDRaisedButton(
            text="取消",
            size_hint_x=0.5,
            on_release=lambda x: self._close_dialog()
        )
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(button_layout)
        return content
    
    def _load_image_from_path(self):
        """从路径加载图片"""
        file_path = self.file_path_field.text.strip()
        if file_path:
            self._load_image(file_path)
        self._close_dialog()
    
    def _close_dialog(self):
        """关闭对话框"""
        # 这里需要获取当前打开的对话框并关闭
        pass
    
    def _load_image(self, file_path):
        """加载图片"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"文件不存在: {file_path}")
                return
            
            # 读取图片数据
            with open(file_path, 'rb') as f:
                image_data = f.read()
            
            # 验证图片格式
            from utils.validators import Validators
            validation_result = Validators.validate_image_data(image_data)
            if not validation_result['valid']:
                self.logger.error(f"图片验证失败: {validation_result['errors']}")
                return
            
            # 保存图片数据
            self.image_data = image_data
            self.image_filename = Path(file_path).name
            
            # 更新UI
            self._update_image_display()
            
            self.logger.info(f"图片加载成功: {self.image_filename}")
            
        except Exception as e:
            self.logger.error(f"加载图片失败: {e}")
    
    def _update_image_display(self):
        """更新图片显示"""
        try:
            if self.image_data:
                # 创建临时文件用于显示
                temp_path = file_manager.images_dir / f"temp_{self.image_filename}"
                with open(temp_path, 'wb') as f:
                    f.write(self.image_data)
                
                # 更新图片预览
                self.image_preview.source = str(temp_path)
                self.image_preview.reload()
                
                # 更新信息标签
                self.image_name_label.text = self.image_filename
                self.image_size_label.text = f"大小: {len(self.image_data) / 1024:.1f} KB"
            else:
                # 清除显示
                self.image_preview.source = ""
                self.image_name_label.text = "未选择图片"
                self.image_size_label.text = ""
                
        except Exception as e:
            self.logger.error(f"更新图片显示失败: {e}")
    
    def _clear_image(self, instance):
        """清除图片"""
        self.image_data = None
        self.image_filename = None
        self._update_image_display()
        self.logger.info("图片已清除")
    
    def get_image_data(self):
        """获取图片数据"""
        return self.image_data
    
    def get_image_filename(self):
        """获取图片文件名"""
        return self.image_filename
    
    def set_image_data(self, image_data, filename=None):
        """设置图片数据"""
        self.image_data = image_data
        self.image_filename = filename or "image.png"
        self._update_image_display()
    
    def has_image(self):
        """检查是否有图片"""
        return self.image_data is not None

