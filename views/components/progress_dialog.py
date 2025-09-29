"""
进度对话框组件
Progress Dialog Component
"""

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.clock import Clock

from utils.logger import get_logger


class ProgressDialog(MDDialog):
    """进度对话框"""
    
    def __init__(self, title="操作进行中", message="", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        
        self.title = title
        self.type = "custom"
        self.content_cls = self._create_content(message)
        
        # 进度相关
        self.progress_value = 0
        self.max_value = 100
        self.is_cancelled = False
        
        # 按钮
        self.buttons = [
            MDRaisedButton(
                text="取消",
                on_release=self._on_cancel
            )
        ]
    
    def _create_content(self, message):
        """创建内容"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(120)
        )
        
        # 消息标签
        self.message_label = MDLabel(
            text=message,
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign="center",
            valign="middle"
        )
        content.add_widget(self.message_label)
        
        # 进度条
        self.progress_bar = MDProgressBar(
            value=0,
            size_hint_y=None,
            height=dp(20)
        )
        content.add_widget(self.progress_bar)
        
        # 进度文本
        self.progress_label = MDLabel(
            text="0%",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        content.add_widget(self.progress_label)
        
        # 状态文本
        self.status_label = MDLabel(
            text="准备中...",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        content.add_widget(self.status_label)
        
        return content
    
    def update_progress(self, value, max_value=None, message=None, status=None):
        """更新进度"""
        if max_value is not None:
            self.max_value = max_value
        
        self.progress_value = min(value, self.max_value)
        
        # 更新进度条
        progress_percent = (self.progress_value / self.max_value) * 100
        self.progress_bar.value = progress_percent
        self.progress_label.text = f"{int(progress_percent)}%"
        
        # 更新消息
        if message is not None:
            self.message_label.text = message
        
        # 更新状态
        if status is not None:
            self.status_label.text = status
        
        self.logger.debug(f"进度更新: {self.progress_value}/{self.max_value} ({progress_percent:.1f}%)")
    
    def set_message(self, message):
        """设置消息"""
        self.message_label.text = message
    
    def set_status(self, status):
        """设置状态"""
        self.status_label.text = status
    
    def _on_cancel(self, instance):
        """取消操作"""
        self.is_cancelled = True
        self.set_status("正在取消...")
        self.logger.info("用户取消了操作")
    
    def is_operation_cancelled(self):
        """检查操作是否被取消"""
        return self.is_cancelled


class BatchOperationDialog(ProgressDialog):
    """批量操作对话框"""
    
    def __init__(self, operation_type="批量操作", total_items=0, **kwargs):
        super().__init__(
            title=f"{operation_type}进行中",
            message=f"正在处理 {total_items} 个项目...",
            **kwargs
        )
        
        self.operation_type = operation_type
        self.total_items = total_items
        self.current_item = 0
        self.processed_items = 0
        self.failed_items = 0
        
        # 更新最大值为项目总数
        self.max_value = total_items
    
    def update_item_progress(self, current_item, item_name="", success=True):
        """更新项目进度"""
        self.current_item = current_item
        
        if success:
            self.processed_items += 1
        else:
            self.failed_items += 1
        
        # 更新进度
        self.update_progress(
            value=current_item,
            message=f"正在处理: {item_name}" if item_name else f"正在处理第 {current_item} 项",
            status=f"已处理: {self.processed_items}, 失败: {self.failed_items}"
        )
    
    def complete_operation(self):
        """完成操作"""
        self.update_progress(
            value=self.max_value,
            message=f"{self.operation_type}完成",
            status=f"总计: {self.total_items}, 成功: {self.processed_items}, 失败: {self.failed_items}"
        )
        
        # 更新按钮
        self.buttons = [
            MDRaisedButton(
                text="确定",
                on_release=lambda x: self.dismiss()
            )
        ]
        
        self.logger.info(f"{self.operation_type}完成: 成功 {self.processed_items}, 失败 {self.failed_items}")


class ImportProgressDialog(BatchOperationDialog):
    """导入进度对话框"""
    
    def __init__(self, file_path="", total_items=0, **kwargs):
        super().__init__(
            operation_type="导入",
            total_items=total_items,
            **kwargs
        )
        
        self.file_path = file_path
        self.set_message(f"正在从 {file_path} 导入数据...")
    
    def update_import_progress(self, current_item, item_name="", success=True):
        """更新导入进度"""
        self.update_item_progress(current_item, item_name, success)
        
        if success:
            self.set_status(f"已导入: {self.processed_items}, 失败: {self.failed_items}")
        else:
            self.set_status(f"导入失败: {item_name}")


class ExportProgressDialog(BatchOperationDialog):
    """导出进度对话框"""
    
    def __init__(self, format_type="", total_items=0, **kwargs):
        super().__init__(
            operation_type=f"导出{format_type.upper()}",
            total_items=total_items,
            **kwargs
        )
        
        self.format_type = format_type
        self.set_message(f"正在导出为 {format_type.upper()} 格式...")
    
    def update_export_progress(self, current_item, item_name="", success=True):
        """更新导出进度"""
        self.update_item_progress(current_item, item_name, success)
        
        if success:
            self.set_status(f"已导出: {self.processed_items}, 失败: {self.failed_items}")
        else:
            self.set_status(f"导出失败: {item_name}")


class ImageImportDialog(ProgressDialog):
    """图片导入对话框"""
    
    def __init__(self, image_count=0, **kwargs):
        super().__init__(
            title="图片导入中",
            message=f"正在导入 {image_count} 张图片...",
            **kwargs
        )
        
        self.image_count = image_count
        self.max_value = image_count
        self.current_image = 0
    
    def update_image_progress(self, current_image, image_name="", success=True):
        """更新图片导入进度"""
        self.current_image = current_image
        
        self.update_progress(
            value=current_image,
            message=f"正在导入: {image_name}" if image_name else f"正在导入第 {current_image} 张图片",
            status=f"已导入: {current_image}/{self.image_count}"
        )
        
        if not success:
            self.set_status(f"导入失败: {image_name}")
    
    def complete_import(self):
        """完成导入"""
        self.update_progress(
            value=self.max_value,
            message="图片导入完成",
            status=f"成功导入 {self.current_image} 张图片"
        )
        
        # 更新按钮
        self.buttons = [
            MDRaisedButton(
                text="确定",
                on_release=lambda x: self.dismiss()
            )
        ]

