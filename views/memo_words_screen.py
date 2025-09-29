"""
备忘词条界面
Memo Words Screen
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime

from .base_screen import BaseScreen
from utils.logger import get_logger
from services.memo_service import memo_service


class MemoWordsScreen(BaseScreen):
    """备忘词条界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.memo_words = []
        self.current_status = "全部"
        self.search_query = ""
        
        self._setup_ui()
        self._load_memo_words()
    
    def get_screen_title(self) -> str:
        return "备忘词条"
    
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
        
        # 搜索和筛选卡片
        self.search_card = self._create_search_card()
        self.main_container.add_widget(self.search_card)
        
        # 备忘列表卡片
        self.memo_card = self._create_memo_card()
        self.main_container.add_widget(self.memo_card)
        
        self.scroll_view.add_widget(self.main_container)
        self.content_layout.add_widget(self.scroll_view)
        
        # 浮动添加按钮
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            on_release=self._show_add_memo_dialog
        )
        self.content_layout.add_widget(self.fab)
    
    def _create_search_card(self):
        """创建搜索卡片"""
        card = MDCard(
            padding=dp(16),
            radius=[15, 15, 15, 15]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        # 搜索框
        search_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.search_field = MDTextField(
            hint_text="搜索备忘内容...",
            mode="rectangle",
            size_hint_x=0.7,
            on_text_validate=self._search_memo_words
        )
        search_layout.add_widget(self.search_field)
        
        search_btn = MDRaisedButton(
            text="搜索",
            size_hint_x=0.3,
            on_release=self._search_memo_words
        )
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # 状态筛选
        filter_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        status_label = MDLabel(
            text="状态:",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.2
        )
        filter_layout.add_widget(status_label)
        
        self.status_btn = MDRaisedButton(
            text=self.current_status,
            size_hint_x=0.8,
            on_release=self._show_status_menu
        )
        filter_layout.add_widget(self.status_btn)
        
        layout.add_widget(filter_layout)
        
        card.add_widget(layout)
        return card
    
    def _create_memo_card(self):
        """创建备忘列表卡片"""
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
            text="备忘列表",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(title)
        
        # 备忘列表
        self.memo_list = MDList()
        layout.add_widget(self.memo_list)
        
        card.add_widget(layout)
        return card
    
    def _load_memo_words(self):
        """加载备忘列表"""
        try:
            self.memo_words = memo_service.get_all_memo_words()
            self._update_memo_display()
        except Exception as e:
            self.logger.error(f"加载备忘列表失败: {e}")
            self.show_snackbar("加载备忘列表失败")
    
    def _update_memo_display(self):
        """更新备忘显示"""
        self.memo_list.clear_widgets()
        
        # 筛选备忘
        filtered_memos = self._filter_memo_words()
        
        if not filtered_memos:
            empty_item = OneLineListItem(
                text="暂无备忘",
                theme_text_color="Secondary"
            )
            self.memo_list.add_widget(empty_item)
            return
        
        for memo in filtered_memos:
            status_text = "已完成" if memo.is_completed else "待处理"
            created_time = memo.created_at.strftime("%Y-%m-%d %H:%M")
            
            item = TwoLineListItem(
                text=memo.content,
                secondary_text=f"{status_text} | {created_time}",
                on_release=lambda x, m=memo: self._view_memo_detail(m)
            )
            
            # 添加操作按钮
            if not memo.is_completed:
                item.add_widget(
                    MDIconButton(
                        icon="check",
                        pos_hint={"center_y": 0.5},
                        on_release=lambda x, m=memo: self._complete_memo(m)
                    )
                )
            
            item.add_widget(
                MDIconButton(
                    icon="pencil",
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, m=memo: self._edit_memo(m)
                )
            )
            
            item.add_widget(
                MDIconButton(
                    icon="delete",
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, m=memo: self._delete_memo(m)
                )
            )
            
            self.memo_list.add_widget(item)
    
    def _filter_memo_words(self):
        """筛选备忘"""
        filtered = self.memo_words
        
        # 按状态筛选
        if self.current_status == "已完成":
            filtered = [m for m in filtered if m.is_completed]
        elif self.current_status == "待处理":
            filtered = [m for m in filtered if not m.is_completed]
        
        # 按搜索词筛选
        if self.search_query:
            query = self.search_query.lower()
            filtered = [m for m in filtered if query in m.content.lower()]
        
        return filtered
    
    def _search_memo_words(self, instance):
        """搜索备忘"""
        self.search_query = self.search_field.text
        self._update_memo_display()
    
    def _show_status_menu(self, instance):
        """显示状态菜单"""
        statuses = ["全部", "待处理", "已完成"]
        
        menu_items = []
        for status in statuses:
            menu_items.append({
                "text": status,
                "on_release": lambda x, s=status: self._select_status(s)
            })
        
        menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    
    def _select_status(self, status):
        """选择状态"""
        self.current_status = status
        self.status_btn.text = status
        self._update_memo_display()
    
    def _view_memo_detail(self, memo):
        """查看备忘详情"""
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="备忘详情",
            text=f"内容: {memo.content}\n\n状态: {'已完成' if memo.is_completed else '待处理'}\n创建时间: {memo.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            buttons=[
                MDRaisedButton(
                    text="关闭",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def _complete_memo(self, memo):
        """完成备忘"""
        try:
            memo.is_completed = True
            memo.completed_at = datetime.now()
            memo_service.update_memo_word(memo)
            self._load_memo_words()
            self.show_snackbar("备忘已标记为完成")
        except Exception as e:
            self.logger.error(f"完成备忘失败: {e}")
            self.show_snackbar("完成备忘失败")
    
    def _edit_memo(self, memo):
        """编辑备忘"""
        self._show_edit_memo_dialog(memo)
    
    def _delete_memo(self, memo):
        """删除备忘"""
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="确认删除",
            text=f"确定要删除备忘 '{memo.content[:20]}...' 吗？",
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="删除",
                    on_release=lambda x: self._confirm_delete_memo(dialog, memo)
                )
            ]
        )
        dialog.open()
    
    def _confirm_delete_memo(self, dialog, memo):
        """确认删除备忘"""
        try:
            memo_service.delete_memo_word(memo.id)
            dialog.dismiss()
            self._load_memo_words()
            self.show_snackbar("备忘已删除")
        except Exception as e:
            self.logger.error(f"删除备忘失败: {e}")
            self.show_snackbar("删除备忘失败")
    
    def _show_add_memo_dialog(self, instance):
        """显示添加备忘对话框"""
        self._show_memo_dialog()
    
    def _show_edit_memo_dialog(self, memo):
        """显示编辑备忘对话框"""
        self._show_memo_dialog(memo)
    
    def _show_memo_dialog(self, memo=None):
        """显示备忘对话框"""
        # 创建表单
        form_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(200)
        )
        
        # 内容
        content_field = MDTextField(
            hint_text="备忘内容",
            mode="rectangle",
            multiline=True,
            text=memo.content if memo else ""
        )
        form_layout.add_widget(content_field)
        
        # 优先级
        priority_field = MDTextField(
            hint_text="优先级 (1-5)",
            mode="rectangle",
            text=str(memo.priority) if memo else "3"
        )
        form_layout.add_widget(priority_field)
        
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="添加备忘" if not memo else "编辑备忘",
            type="custom",
            content_cls=form_layout,
            buttons=[
                MDRaisedButton(
                    text="取消",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="保存",
                    on_release=lambda x: self._save_memo(dialog, content_field, priority_field, memo)
                )
            ]
        )
        dialog.open()
    
    def _save_memo(self, dialog, content_field, priority_field, memo=None):
        """保存备忘"""
        try:
            content = content_field.text.strip()
            priority = int(priority_field.text.strip() or "3")
            
            if not content:
                self.show_snackbar("备忘内容不能为空")
                return
            
            if priority < 1 or priority > 5:
                self.show_snackbar("优先级必须在1-5之间")
                return
            
            if memo:
                # 编辑备忘
                memo.content = content
                memo.priority = priority
                memo.updated_at = datetime.now()
                memo_service.update_memo_word(memo)
                self.show_snackbar("备忘已更新")
            else:
                # 添加备忘
                memo_data = {
                    'content': content,
                    'priority': priority
                }
                memo_service.add_memo_word(memo_data)
                self.show_snackbar("备忘已添加")
            
            dialog.dismiss()
            self._load_memo_words()
            
        except ValueError:
            self.show_snackbar("优先级必须是数字")
        except Exception as e:
            self.logger.error(f"保存备忘失败: {e}")
            self.show_snackbar("保存备忘失败")
    
    def refresh_data(self):
        """刷新数据"""
        self._load_memo_words()

