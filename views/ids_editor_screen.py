"""
IDS符号编辑器界面
IDS Symbol Editor Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.metrics import dp
from kivy.clock import Clock
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

from .base_screen import BaseScreen
from utils.logger import get_logger
from services.ids_service import ids_service


class IdsCanvas(Widget):
    """IDS符号画布"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = []
        self.current_symbol = None
        self.drawing = False
        self.bind(size=self._update_canvas)
    
    def _update_canvas(self, *args):
        """更新画布"""
        self.canvas.clear()
        with self.canvas:
            # 背景
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # 绘制符号
            for symbol in self.symbols:
                self._draw_symbol(symbol)
    
    def _draw_symbol(self, symbol):
        """绘制符号"""
        if symbol['type'] == 'rectangle':
            Color(0, 0, 0, 1)
            Rectangle(pos=symbol['pos'], size=symbol['size'])
        elif symbol['type'] == 'line':
            Color(0, 0, 0, 1)
            Line(points=symbol['points'], width=2)
        elif symbol['type'] == 'circle':
            Color(0, 0, 0, 1)
            Ellipse(pos=symbol['pos'], size=symbol['size'])
    
    def on_touch_down(self, touch):
        """触摸开始"""
        if self.collide_point(*touch.pos):
            self.drawing = True
            self.current_symbol = {
                'type': 'line',
                'points': [touch.x, touch.y]
            }
            return True
        return False
    
    def on_touch_move(self, touch):
        """触摸移动"""
        if self.drawing and self.current_symbol:
            self.current_symbol['points'].extend([touch.x, touch.y])
            self._update_canvas()
            return True
        return False
    
    def on_touch_up(self, touch):
        """触摸结束"""
        if self.drawing and self.current_symbol:
            self.symbols.append(self.current_symbol)
            self.current_symbol = None
            self.drawing = False
            return True
        return False
    
    def clear_canvas(self):
        """清空画布"""
        self.symbols = []
        self._update_canvas()
    
    def add_rectangle(self, pos, size):
        """添加矩形"""
        self.symbols.append({
            'type': 'rectangle',
            'pos': pos,
            'size': size
        })
        self._update_canvas()
    
    def add_circle(self, pos, size):
        """添加圆形"""
        self.symbols.append({
            'type': 'circle',
            'pos': pos,
            'size': size
        })
        self._update_canvas()


class IdsEditorScreen(BaseScreen):
    """IDS符号编辑器界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.current_tool = "draw"
        self.canvas_size = (400, 400)
        
        self._setup_ui()
    
    def get_screen_title(self) -> str:
        return "IDS符号编辑器"
    
    def _setup_ui(self):
        """设置UI"""
        # 主容器
        main_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # 左侧工具栏
        self.toolbar = self._create_toolbar()
        main_layout.add_widget(self.toolbar)
        
        # 右侧画布区域
        self.canvas_area = self._create_canvas_area()
        main_layout.add_widget(self.canvas_area)
        
        self.content_layout.add_widget(main_layout)
    
    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_x=0.3
        )
        
        # 工具选择卡片
        tools_card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        tools_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="绘图工具",
            theme_text_color="Primary",
            font_style="H6"
        )
        tools_layout.add_widget(title)
        
        # 工具按钮
        draw_btn = MDRaisedButton(
            text="画笔",
            on_release=lambda x: self._select_tool("draw")
        )
        tools_layout.add_widget(draw_btn)
        
        rectangle_btn = MDRaisedButton(
            text="矩形",
            on_release=lambda x: self._select_tool("rectangle")
        )
        tools_layout.add_widget(rectangle_btn)
        
        circle_btn = MDRaisedButton(
            text="圆形",
            on_release=lambda x: self._select_tool("circle")
        )
        tools_layout.add_widget(circle_btn)
        
        tools_card.add_widget(tools_layout)
        toolbar.add_widget(tools_card)
        
        # 操作卡片
        actions_card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="操作",
            theme_text_color="Primary",
            font_style="H6"
        )
        actions_layout.add_widget(title)
        
        # 操作按钮
        clear_btn = MDRaisedButton(
            text="清空画布",
            on_release=self._clear_canvas
        )
        actions_layout.add_widget(clear_btn)
        
        save_btn = MDRaisedButton(
            text="保存符号",
            on_release=self._save_symbol
        )
        actions_layout.add_widget(save_btn)
        
        export_btn = MDRaisedButton(
            text="导出图片",
            on_release=self._export_image
        )
        actions_layout.add_widget(export_btn)
        
        actions_card.add_widget(actions_layout)
        toolbar.add_widget(actions_card)
        
        # 模板卡片
        templates_card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        templates_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="常用模板",
            theme_text_color="Primary",
            font_style="H6"
        )
        templates_layout.add_widget(title)
        
        # 模板按钮
        template_btn1 = MDRaisedButton(
            text="基本结构",
            on_release=lambda x: self._load_template("basic")
        )
        templates_layout.add_widget(template_btn1)
        
        template_btn2 = MDRaisedButton(
            text="复合结构",
            on_release=lambda x: self._load_template("complex")
        )
        templates_layout.add_widget(template_btn2)
        
        template_btn3 = MDRaisedButton(
            text="自定义",
            on_release=lambda x: self._load_template("custom")
        )
        templates_layout.add_widget(template_btn3)
        
        templates_card.add_widget(templates_layout)
        toolbar.add_widget(templates_card)
        
        return toolbar
    
    def _create_canvas_area(self):
        """创建画布区域"""
        canvas_area = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_x=0.7
        )
        
        # 画布卡片
        canvas_card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        canvas_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 标题
        title = MDLabel(
            text="IDS符号画布",
            theme_text_color="Primary",
            font_style="H6"
        )
        canvas_layout.add_widget(title)
        
        # 画布
        self.canvas_widget = IdsCanvas()
        self.canvas_widget.size_hint = (1, 0.8)
        canvas_layout.add_widget(self.canvas_widget)
        
        # 状态栏
        status_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.status_label = MDLabel(
            text="当前工具: 画笔",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        status_layout.add_widget(self.status_label)
        
        canvas_layout.add_widget(status_layout)
        
        canvas_card.add_widget(canvas_layout)
        canvas_area.add_widget(canvas_card)
        
        return canvas_area
    
    def _select_tool(self, tool):
        """选择工具"""
        self.current_tool = tool
        tool_names = {
            "draw": "画笔",
            "rectangle": "矩形",
            "circle": "圆形"
        }
        self.status_label.text = f"当前工具: {tool_names.get(tool, tool)}"
        self.logger.info(f"选择工具: {tool}")
    
    def _clear_canvas(self, instance):
        """清空画布"""
        self.canvas_widget.clear_canvas()
        self.show_snackbar("画布已清空")
    
    def _save_symbol(self, instance):
        """保存符号"""
        try:
            if not self.canvas_widget.symbols:
                self.show_snackbar("画布为空，无法保存")
                return
            
            # 显示保存对话框
            self._show_save_dialog()
            
        except Exception as e:
            self.logger.error(f"保存符号失败: {e}")
            self.show_snackbar("保存符号失败")
    
    def _export_image(self, instance):
        """导出图片"""
        try:
            if not self.canvas_widget.symbols:
                self.show_snackbar("画布为空，无法导出")
                return
            
            # 创建PIL图像
            img = Image.new('RGB', self.canvas_size, 'white')
            draw = ImageDraw.Draw(img)
            
            # 绘制符号
            for symbol in self.canvas_widget.symbols:
                if symbol['type'] == 'rectangle':
                    pos = symbol['pos']
                    size = symbol['size']
                    draw.rectangle([pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]], outline='black')
                elif symbol['type'] == 'circle':
                    pos = symbol['pos']
                    size = symbol['size']
                    draw.ellipse([pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]], outline='black')
                elif symbol['type'] == 'line':
                    points = symbol['points']
                    if len(points) >= 4:
                        for i in range(0, len(points) - 2, 2):
                            draw.line([points[i], points[i+1], points[i+2], points[i+3]], fill='black', width=2)
            
            # 保存图片
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ids_symbol_{timestamp}.png"
            filepath = os.path.join("exports", filename)
            
            # 确保目录存在
            os.makedirs("exports", exist_ok=True)
            
            img.save(filepath)
            self.show_snackbar(f"图片已导出: {filename}")
            
        except Exception as e:
            self.logger.error(f"导出图片失败: {e}")
            self.show_snackbar("导出图片失败")
    
    def _load_template(self, template_type):
        """加载模板"""
        try:
            self.canvas_widget.clear_canvas()
            
            if template_type == "basic":
                # 基本结构模板
                self.canvas_widget.add_rectangle((50, 50), (100, 100))
                self.canvas_widget.add_rectangle((200, 50), (100, 100))
                self.show_snackbar("已加载基本结构模板")
            elif template_type == "complex":
                # 复合结构模板
                self.canvas_widget.add_rectangle((50, 50), (80, 80))
                self.canvas_widget.add_rectangle((150, 50), (80, 80))
                self.canvas_widget.add_rectangle((250, 50), (80, 80))
                self.canvas_widget.add_rectangle((100, 150), (80, 80))
                self.show_snackbar("已加载复合结构模板")
            elif template_type == "custom":
                # 自定义模板
                self.canvas_widget.add_circle((100, 100), (100, 100))
                self.canvas_widget.add_rectangle((50, 200), (200, 50))
                self.show_snackbar("已加载自定义模板")
            
        except Exception as e:
            self.logger.error(f"加载模板失败: {e}")
            self.show_snackbar("加载模板失败")
    
    def _show_save_dialog(self):
        """显示保存对话框"""
        # 创建表单
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(200)
        )
        
        # 符号名称
        name_field = MDTextField(
            hint_text="符号名称",
            mode="rectangle"
        )
        form_layout.add_widget(name_field)
        
        # 符号描述
        description_field = MDTextField(
            hint_text="符号描述",
            mode="rectangle",
            multiline=True
        )
        form_layout.add_widget(description_field)
        
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="保存IDS符号",
            type="custom",
            content_cls=form_layout,
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="保存",
                    on_release=lambda x: self._confirm_save_symbol(dialog, name_field, description_field)
                )
            ]
        )
        dialog.open()
    
    def _confirm_save_symbol(self, dialog, name_field, description_field):
        """确认保存符号"""
        try:
            name = name_field.text.strip()
            description = description_field.text.strip()
            
            if not name:
                self.show_snackbar("符号名称不能为空")
                return
            
            # 保存符号数据
            symbol_data = {
                'name': name,
                'description': description,
                'symbols': self.canvas_widget.symbols,
                'canvas_size': self.canvas_size
            }
            
            ids_service.save_symbol(symbol_data)
            
            dialog.dismiss()
            self.show_snackbar("符号已保存")
            
        except Exception as e:
            self.logger.error(f"保存符号失败: {e}")
            self.show_snackbar("保存符号失败")
    
    def refresh_data(self):
        """刷新数据"""
        pass

