"""
高亮标签组件
Highlighted Label Component
"""

from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import re

from utils.logger import get_logger


class HighlightedLabel(MDLabel):
    """支持高亮的标签组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.highlight_query = ""
        self.highlight_color = [1, 1, 0, 0.3]  # 黄色高亮
        self.case_sensitive = False
    
    def set_highlight(self, query, case_sensitive=False):
        """设置高亮查询"""
        self.highlight_query = query
        self.case_sensitive = case_sensitive
        self._apply_highlight()
    
    def _apply_highlight(self):
        """应用高亮效果"""
        if not self.highlight_query or not self.text:
            return
        
        try:
            # 由于KivyMD标签的限制，这里使用简单的文本标记
            # 在实际应用中，可以使用更复杂的文本渲染
            original_text = self.text
            
            if self.case_sensitive:
                pattern = re.escape(self.highlight_query)
            else:
                pattern = re.escape(self.highlight_query)
                flags = re.IGNORECASE
                pattern = f"(?i){pattern}"
            
            # 使用特殊标记来标识高亮文本
            highlighted_text = re.sub(
                pattern,
                f"[HIGHLIGHT]{self.highlight_query}[/HIGHLIGHT]",
                original_text,
                flags=re.IGNORECASE if not self.case_sensitive else 0
            )
            
            # 这里可以进一步处理高亮文本的显示
            # 由于KivyMD的限制，暂时使用简单的标记
            
        except Exception as e:
            self.logger.error(f"应用高亮失败: {e}")
    
    def get_highlighted_text(self):
        """获取高亮后的文本"""
        if not self.highlight_query or not self.text:
            return self.text
        
        try:
            original_text = self.text
            
            if self.case_sensitive:
                pattern = re.escape(self.highlight_query)
            else:
                pattern = re.escape(self.highlight_query)
                flags = re.IGNORECASE
                pattern = f"(?i){pattern}"
            
            # 使用HTML标记来标识高亮文本
            highlighted_text = re.sub(
                pattern,
                f'<span style="background-color: yellow; color: black;">{self.highlight_query}</span>',
                original_text,
                flags=re.IGNORECASE if not self.case_sensitive else 0
            )
            
            return highlighted_text
            
        except Exception as e:
            self.logger.error(f"获取高亮文本失败: {e}")
            return self.text


class SearchResultCard(MDLabel):
    """搜索结果卡片组件"""
    
    def __init__(self, word_entry=None, highlight_query="", **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.word_entry = word_entry
        self.highlight_query = highlight_query
        
        if word_entry:
            self._setup_content()
    
    def _setup_content(self):
        """设置内容"""
        if not self.word_entry:
            return
        
        # 构建显示文本
        content_parts = []
        
        # 基本信息
        basic_info = f"{self.word_entry.word_id} - {self.word_entry.latin_form}"
        if self.word_entry.phonetic:
            basic_info += f" [{self.word_entry.phonetic}]"
        content_parts.append(basic_info)
        
        # 词性
        if self.word_entry.word_type:
            content_parts.append(f"词性: {self.word_entry.word_type}")
        
        # 释义
        if self.word_entry.definitions:
            definition_text = self.word_entry.definitions[0].definition_text
            content_parts.append(f"释义: {definition_text}")
        
        # 例句
        if self.word_entry.examples:
            example_text = self.word_entry.examples[0].example_text
            content_parts.append(f"例句: {example_text}")
        
        # 组合文本
        self.text = "\n".join(content_parts)
        
        # 应用高亮
        if self.highlight_query:
            self._apply_highlight()
    
    def _apply_highlight(self):
        """应用高亮效果"""
        if not self.highlight_query or not self.text:
            return
        
        try:
            # 使用简单的文本替换来模拟高亮
            # 在实际应用中，可以使用更复杂的文本渲染
            original_text = self.text
            
            # 不区分大小写的搜索
            pattern = re.escape(self.highlight_query)
            highlighted_text = re.sub(
                pattern,
                f"**{self.highlight_query}**",
                original_text,
                flags=re.IGNORECASE
            )
            
            self.text = highlighted_text
            
        except Exception as e:
            self.logger.error(f"应用高亮失败: {e}")
    
    def set_highlight_query(self, query):
        """设置高亮查询"""
        self.highlight_query = query
        self._apply_highlight()

