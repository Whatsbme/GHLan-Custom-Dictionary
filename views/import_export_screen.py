"""
导入导出界面
Import Export Screen
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
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock
import threading
import os
from pathlib import Path

from .base_screen import BaseScreen
from utils.logger import get_logger
from services.import_service import import_service
from services.export_service import export_service
from services.dictionary_service import dictionary_service


class ImportExportScreen(BaseScreen):
    """导入导出界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.current_operation = None
        self.operation_thread = None
        self.progress_dialog = None
        
        self._setup_ui()
    
    def get_screen_title(self) -> str:
        return "导入导出"
    
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
        
        # 导入卡片
        self.import_card = self._create_import_card()
        self.main_container.add_widget(self.import_card)
        
        # 导出卡片
        self.export_card = self._create_export_card()
        self.main_container.add_widget(self.export_card)
        
        # 批量操作卡片
        self.batch_card = self._create_batch_card()
        self.main_container.add_widget(self.batch_card)
        
        # 操作历史卡片
        self.history_card = self._create_history_card()
        self.main_container.add_widget(self.history_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
    
    def _create_import_card(self):
        """创建导入卡片"""
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
            text="导入功能",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 字型图片导入
        image_import_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        image_title = MDLabel(
            text="字型图片导入",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        image_import_layout.add_widget(image_title)
        
        # 图片导入选项
        image_options_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        # 选择词条
        word_selection_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        word_label = MDLabel(
            text="选择词条",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        word_selection_layout.add_widget(word_label)
        
        self.word_selection_btn = MDRaisedButton(
            text="选择词条",
            size_hint_x=0.7,
            on_release=self._select_word_for_image_import
        )
        word_selection_layout.add_widget(self.word_selection_btn)
        
        image_options_layout.add_widget(word_selection_layout)
        
        # 图片文件选择
        file_selection_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        file_label = MDLabel(
            text="图片文件",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        file_selection_layout.add_widget(file_label)
        
        self.image_file_btn = MDRaisedButton(
            text="选择图片文件",
            size_hint_x=0.7,
            on_release=self._select_image_file
        )
        file_selection_layout.add_widget(self.image_file_btn)
        
        image_options_layout.add_widget(file_selection_layout)
        
        # 图片类型
        type_selection_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        type_label = MDLabel(
            text="图片类型",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        type_selection_layout.add_widget(type_label)
        
        self.image_type_btn = MDRaisedButton(
            text="字型图片",
            size_hint_x=0.7,
            on_release=self._select_image_type
        )
        type_selection_layout.add_widget(self.image_type_btn)
        
        image_options_layout.add_widget(type_selection_layout)
        
        # 导入按钮
        import_btn = MDRaisedButton(
            text="导入图片",
            on_release=self._import_image
        )
        image_options_layout.add_widget(import_btn)
        
        image_import_layout.add_widget(image_options_layout)
        layout.add_widget(image_import_layout)
        
        # 批量导入
        batch_import_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        batch_title = MDLabel(
            text="批量导入",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        batch_import_layout.add_widget(batch_title)
        
        # 批量导入选项
        batch_options_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        excel_import_btn = MDRaisedButton(
            text="导入Excel",
            size_hint_x=0.5,
            on_release=self._import_excel
        )
        batch_options_layout.add_widget(excel_import_btn)
        
        csv_import_btn = MDRaisedButton(
            text="导入CSV",
            size_hint_x=0.5,
            on_release=self._import_csv
        )
        batch_options_layout.add_widget(csv_import_btn)
        
        batch_import_layout.add_widget(batch_options_layout)
        layout.add_widget(batch_import_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_export_card(self):
        """创建导出卡片"""
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
            text="导出功能",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 导出格式选择
        format_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        format_label = MDLabel(
            text="导出格式",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.3
        )
        format_layout.add_widget(format_label)
        
        self.export_format_btn = MDRaisedButton(
            text="Excel",
            size_hint_x=0.7,
            on_release=self._select_export_format
        )
        format_layout.add_widget(self.export_format_btn)
        
        layout.add_widget(format_layout)
        
        # 导出选项
        options_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 包含图片
        include_images_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        include_images_label = MDLabel(
            text="包含图片",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        include_images_layout.add_widget(include_images_label)
        
        self.include_images_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        include_images_layout.add_widget(self.include_images_switch)
        
        options_layout.add_widget(include_images_layout)
        
        # 包含例句
        include_examples_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        include_examples_label = MDLabel(
            text="包含例句",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        include_examples_layout.add_widget(include_examples_label)
        
        self.include_examples_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        include_examples_layout.add_widget(self.include_examples_switch)
        
        options_layout.add_widget(include_examples_layout)
        
        # 包含备注
        include_notes_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        include_notes_label = MDLabel(
            text="包含备注",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.7
        )
        include_notes_layout.add_widget(include_notes_label)
        
        self.include_notes_switch = MDSwitch(
            active=True,
            size_hint_x=0.3
        )
        include_notes_layout.add_widget(self.include_notes_switch)
        
        options_layout.add_widget(include_notes_layout)
        
        layout.add_widget(options_layout)
        
        # 导出按钮
        export_btn = MDRaisedButton(
            text="开始导出",
            on_release=self._start_export
        )
        layout.add_widget(export_btn)
        
        card.add_widget(layout)
        return card
    
    def _create_batch_card(self):
        """创建批量操作卡片"""
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
            text="批量操作",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 批量操作选项
        batch_operations_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # 批量删除
        batch_delete_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        batch_delete_btn = MDRaisedButton(
            text="批量删除",
            size_hint_x=0.5,
            md_bg_color=self.theme_cls.error_color,
            on_release=self._batch_delete
        )
        batch_delete_layout.add_widget(batch_delete_btn)
        
        # 批量编辑
        batch_edit_btn = MDRaisedButton(
            text="批量编辑",
            size_hint_x=0.5,
            on_release=self._batch_edit
        )
        batch_delete_layout.add_widget(batch_edit_btn)
        
        batch_operations_layout.add_widget(batch_delete_layout)
        
        # 批量导出
        batch_export_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )
        
        batch_export_selected_btn = MDRaisedButton(
            text="导出选中",
            size_hint_x=0.5,
            on_release=self._export_selected
        )
        batch_export_layout.add_widget(batch_export_selected_btn)
        
        # 批量导入
        batch_import_btn = MDRaisedButton(
            text="批量导入",
            size_hint_x=0.5,
            on_release=self._batch_import
        )
        batch_export_layout.add_widget(batch_import_btn)
        
        batch_operations_layout.add_widget(batch_export_layout)
        
        layout.add_widget(batch_operations_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_history_card(self):
        """创建操作历史卡片"""
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
            text="操作历史",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 历史列表
        self.history_list = MDList()
        layout.add_widget(self.history_list)
        
        # 清除历史按钮
        clear_history_btn = MDRaisedButton(
            text="清除历史",
            on_release=self._clear_history
        )
        layout.add_widget(clear_history_btn)
        
        card.add_widget(layout)
        return card
    
    def _select_word_for_image_import(self, instance):
        """选择词条进行图片导入"""
        # 这里应该显示词条选择对话框
        self.show_snackbar("词条选择功能开发中...")
    
    def _select_image_file(self, instance):
        """选择图片文件"""
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
                self.image_file_btn.text = Path(file_path).name
                self.selected_image_file = file_path
                self.logger.info(f"选择图片文件: {file_path}")
            else:
                self.show_snackbar("未选择文件")
                
        except ImportError:
            self.show_snackbar("文件选择功能需要tkinter支持")
        except Exception as e:
            self.logger.error(f"选择图片文件失败: {e}")
            self.show_snackbar("选择文件失败")
    
    def _select_image_type(self, instance):
        """选择图片类型"""
        menu_items = [
            {
                "text": "字型图片",
                "on_release": lambda x: self._set_image_type("字型图片")
            },
            {
                "text": "示例图片",
                "on_release": lambda x: self._set_image_type("示例图片")
            },
            {
                "text": "其他图片",
                "on_release": lambda x: self._set_image_type("其他图片")
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_image_type(self, image_type):
        """设置图片类型"""
        self.image_type_btn.text = image_type
        self.selected_image_type = image_type
    
    def _import_image(self, instance):
        """导入图片"""
        if not hasattr(self, 'selected_image_file'):
            self.show_snackbar("请先选择图片文件")
            return
        
        if not hasattr(self, 'selected_image_type'):
            self.show_snackbar("请先选择图片类型")
            return
        
        # 这里应该实现图片导入逻辑
        self.show_snackbar("图片导入功能开发中...")
    
    def _import_excel(self, instance):
        """导入Excel文件"""
        try:
            from tkinter import filedialog
            import tkinter as tk
            
            # 创建隐藏的根窗口
            root = tk.Tk()
            root.withdraw()
            
            # 打开文件对话框
            file_path = filedialog.askopenfilename(
                title="选择Excel文件",
                filetypes=[
                    ("Excel文件", "*.xlsx *.xls"),
                    ("所有文件", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path:
                self._start_import_operation("excel", file_path)
            else:
                self.show_snackbar("未选择文件")
                
        except ImportError:
            self.show_snackbar("文件选择功能需要tkinter支持")
        except Exception as e:
            self.logger.error(f"选择Excel文件失败: {e}")
            self.show_snackbar("选择文件失败")
    
    def _import_csv(self, instance):
        """导入CSV文件"""
        try:
            from tkinter import filedialog
            import tkinter as tk
            
            # 创建隐藏的根窗口
            root = tk.Tk()
            root.withdraw()
            
            # 打开文件对话框
            file_path = filedialog.askopenfilename(
                title="选择CSV文件",
                filetypes=[
                    ("CSV文件", "*.csv"),
                    ("所有文件", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path:
                self._start_import_operation("csv", file_path)
            else:
                self.show_snackbar("未选择文件")
                
        except ImportError:
            self.show_snackbar("文件选择功能需要tkinter支持")
        except Exception as e:
            self.logger.error(f"选择CSV文件失败: {e}")
            self.show_snackbar("选择文件失败")
    
    def _select_export_format(self, instance):
        """选择导出格式"""
        menu_items = [
            {
                "text": "Excel",
                "on_release": lambda x: self._set_export_format("Excel")
            },
            {
                "text": "PDF",
                "on_release": lambda x: self._set_export_format("PDF")
            },
            {
                "text": "CSV",
                "on_release": lambda x: self._set_export_format("CSV")
            }
        ]
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _set_export_format(self, format_name):
        """设置导出格式"""
        self.export_format_btn.text = format_name
        self.selected_export_format = format_name.lower()
    
    def _start_export(self, instance):
        """开始导出"""
        if not hasattr(self, 'selected_export_format'):
            self.show_snackbar("请先选择导出格式")
            return
        
        # 获取导出选项
        export_options = {
            'include_images': self.include_images_switch.active,
            'include_examples': self.include_examples_switch.active,
            'include_notes': self.include_notes_switch.active
        }
        
        self._start_export_operation(self.selected_export_format, export_options)
    
    def _batch_delete(self, instance):
        """批量删除"""
        self.show_snackbar("批量删除功能开发中...")
    
    def _batch_edit(self, instance):
        """批量编辑"""
        self.show_snackbar("批量编辑功能开发中...")
    
    def _export_selected(self, instance):
        """导出选中项"""
        self.show_snackbar("导出选中功能开发中...")
    
    def _batch_import(self, instance):
        """批量导入"""
        self.show_snackbar("批量导入功能开发中...")
    
    def _clear_history(self, instance):
        """清除历史"""
        self.history_list.clear_widgets()
        self.show_snackbar("历史已清除")
    
    def _start_import_operation(self, format_type, file_path):
        """开始导入操作"""
        self.current_operation = f"import_{format_type}"
        
        # 显示进度对话框
        self._show_progress_dialog(f"正在导入{format_type.upper()}文件...")
        
        # 在后台线程中执行导入
        self.operation_thread = threading.Thread(
            target=self._execute_import_operation,
            args=(format_type, file_path)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
    
    def _start_export_operation(self, format_type, options):
        """开始导出操作"""
        self.current_operation = f"export_{format_type}"
        
        # 显示进度对话框
        self._show_progress_dialog(f"正在导出{format_type.upper()}文件...")
        
        # 在后台线程中执行导出
        self.operation_thread = threading.Thread(
            target=self._execute_export_operation,
            args=(format_type, options)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
    
    def _execute_import_operation(self, format_type, file_path):
        """执行导入操作"""
        try:
            if format_type == "excel":
                result = import_service.import_from_excel(file_path)
            elif format_type == "csv":
                result = import_service.import_from_csv(file_path)
            else:
                result = {"success": False, "message": "不支持的格式"}
            
            # 在主线程中更新UI
            Clock.schedule_once(
                lambda dt: self._on_operation_complete(result),
                0
            )
            
        except Exception as e:
            self.logger.error(f"导入操作失败: {e}")
            Clock.schedule_once(
                lambda dt: self._on_operation_complete({
                    "success": False,
                    "message": f"导入失败: {str(e)}"
                }),
                0
            )
    
    def _execute_export_operation(self, format_type, options):
        """执行导出操作"""
        try:
            if format_type == "excel":
                result = export_service.export_to_excel(options)
            elif format_type == "pdf":
                result = export_service.export_to_pdf(options)
            elif format_type == "csv":
                result = export_service.export_to_csv(options)
            else:
                result = {"success": False, "message": "不支持的格式"}
            
            # 在主线程中更新UI
            Clock.schedule_once(
                lambda dt: self._on_operation_complete(result),
                0
            )
            
        except Exception as e:
            self.logger.error(f"导出操作失败: {e}")
            Clock.schedule_once(
                lambda dt: self._on_operation_complete({
                    "success": False,
                    "message": f"导出失败: {str(e)}"
                }),
                0
            )
    
    def _show_progress_dialog(self, message):
        """显示进度对话框"""
        from kivymd.uix.button import MDRaisedButton
        
        self.progress_dialog = MDDialog(
            title="操作进行中",
            text=message,
            type="custom",
            content_cls=MDProgressBar(),
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=self._cancel_operation
                )
            ]
        )
        self.progress_dialog.open()
    
    def _cancel_operation(self, instance):
        """取消操作"""
        if self.operation_thread and self.operation_thread.is_alive():
            # 这里可以实现取消逻辑
            self.logger.info("用户取消了操作")
        
        if self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None
        
        self.current_operation = None
        self.show_snackbar("操作已取消")
    
    def _on_operation_complete(self, result):
        """操作完成回调"""
        if self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None
        
        if result["success"]:
            self.show_snackbar(f"操作成功: {result.get('message', '')}")
            self._add_to_history(result)
        else:
            self.show_snackbar(f"操作失败: {result.get('message', '')}")
        
        self.current_operation = None
    
    def _add_to_history(self, result):
        """添加到操作历史"""
        from datetime import datetime
        
        operation_type = self.current_operation or "unknown"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_item = OneLineListItem(
            text=f"{timestamp} - {operation_type} - {result.get('message', '完成')}"
        )
        self.history_list.add_widget(history_item)
    
    def refresh_data(self):
        """刷新数据"""
        # 重新加载操作历史
        pass

