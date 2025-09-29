"""
工具服务
Utility Service
"""

import re
import requests
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urlparse
from PIL import Image
import io

from models import Bookmark, MemoWord
from services.database_service import db_service


class UtilityService:
    """工具服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_bookmark(self, title: str, url: str, description: str = "") -> bool:
        """添加书签"""
        try:
            # 验证URL格式
            if not self._is_valid_url(url):
                self.logger.warning(f"无效的URL: {url}")
                return False
            
            with db_service.get_session() as session:
                bookmark = Bookmark(
                    title=title,
                    url=url,
                    description=description
                )
                session.add(bookmark)
                session.commit()
                
                self.logger.info(f"书签添加成功: {title}")
                return True
                
        except Exception as e:
            self.logger.error(f"添加书签失败: {e}")
            return False
    
    def get_bookmarks(self) -> List[Bookmark]:
        """获取所有书签"""
        try:
            with db_service.get_session() as session:
                return session.query(Bookmark).order_by(Bookmark.created_at.desc()).all()
        except Exception as e:
            self.logger.error(f"获取书签失败: {e}")
            return []
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """删除书签"""
        try:
            with db_service.get_session() as session:
                bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
                if bookmark:
                    session.delete(bookmark)
                    session.commit()
                    self.logger.info(f"书签删除成功: {bookmark_id}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"删除书签失败: {e}")
            return False
    
    def add_memo_word(self, word_text: str, memo_text: str = "") -> bool:
        """添加备忘词条"""
        try:
            with db_service.get_session() as session:
                memo_word = MemoWord(
                    word_text=word_text,
                    memo_text=memo_text
                )
                session.add(memo_word)
                session.commit()
                
                self.logger.info(f"备忘词条添加成功: {word_text}")
                return True
                
        except Exception as e:
            self.logger.error(f"添加备忘词条失败: {e}")
            return False
    
    def get_memo_words(self) -> List[MemoWord]:
        """获取所有备忘词条"""
        try:
            with db_service.get_session() as session:
                return session.query(MemoWord).order_by(MemoWord.created_at.desc()).all()
        except Exception as e:
            self.logger.error(f"获取备忘词条失败: {e}")
            return []
    
    def delete_memo_word(self, memo_id: int) -> bool:
        """删除备忘词条"""
        try:
            with db_service.get_session() as session:
                memo_word = session.query(MemoWord).filter(MemoWord.id == memo_id).first()
                if memo_word:
                    session.delete(memo_word)
                    session.commit()
                    self.logger.info(f"备忘词条删除成功: {memo_id}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"删除备忘词条失败: {e}")
            return False
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """验证URL并获取页面信息"""
        try:
            if not self._is_valid_url(url):
                return {'valid': False, 'error': '无效的URL格式'}
            
            # 发送HEAD请求检查URL
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            result = {
                'valid': True,
                'status_code': response.status_code,
                'url': response.url,
                'content_type': response.headers.get('content-type', ''),
                'content_length': response.headers.get('content-length', ''),
                'title': ''
            }
            
            # 如果是HTML页面，尝试获取标题
            if 'text/html' in result['content_type']:
                try:
                    html_response = requests.get(url, timeout=10)
                    title_match = re.search(r'<title>(.*?)</title>', html_response.text, re.IGNORECASE)
                    if title_match:
                        result['title'] = title_match.group(1).strip()
                except:
                    pass
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {'valid': False, 'error': f'网络错误: {str(e)}'}
        except Exception as e:
            return {'valid': False, 'error': f'验证失败: {str(e)}'}
    
    def process_ids_symbol(self, ids_text: str) -> Dict[str, Any]:
        """处理IDS描述符号"""
        try:
            # 解析IDS符号
            components = self._parse_ids_components(ids_text)
            
            result = {
                'original': ids_text,
                'components': components,
                'structure': self._analyze_ids_structure(ids_text),
                'is_valid': self._validate_ids_format(ids_text)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"处理IDS符号失败: {e}")
            return {'original': ids_text, 'error': str(e)}
    
    def resize_image(self, image_data: bytes, max_size: tuple = (800, 600), 
                    quality: int = 85) -> bytes:
        """调整图片大小"""
        try:
            # 打开图片
            image = Image.open(io.BytesIO(image_data))
            
            # 计算新尺寸
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存为JPEG格式
            output = io.BytesIO()
            if image.mode in ('RGBA', 'LA', 'P'):
                # 转换为RGB
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = rgb_image
            
            image.save(output, format='JPEG', quality=quality, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            self.logger.error(f"调整图片大小失败: {e}")
            return image_data
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _parse_ids_components(self, ids_text: str) -> List[Dict[str, str]]:
        """解析IDS组件"""
        components = []
        
        # 简单的IDS解析（实际实现需要更复杂的解析逻辑）
        # 这里只是示例实现
        bracket_pattern = r'\[([^\]]+)\]'
        matches = re.findall(bracket_pattern, ids_text)
        
        for match in matches:
            components.append({
                'type': 'component',
                'value': match,
                'position': ids_text.find(f'[{match}]')
            })
        
        return components
    
    def _analyze_ids_structure(self, ids_text: str) -> Dict[str, Any]:
        """分析IDS结构"""
        return {
            'length': len(ids_text),
            'has_brackets': '[' in ids_text and ']' in ids_text,
            'bracket_count': ids_text.count('['),
            'complexity': 'high' if ids_text.count('[') > 3 else 'medium' if ids_text.count('[') > 1 else 'low'
        }
    
    def _validate_ids_format(self, ids_text: str) -> bool:
        """验证IDS格式"""
        # 基本的IDS格式验证
        if not ids_text:
            return False
        
        # 检查括号匹配
        bracket_count = 0
        for char in ids_text:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count < 0:
                    return False
        
        return bracket_count == 0


# 全局工具服务实例
utility_service = UtilityService()
