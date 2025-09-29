"""
词典服务
Dictionary Service
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
import logging

from models import WordEntry, Definition, Example, WordImage
from services.database_service import db_service


class DictionaryService:
    """词典服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_word_entry(self, word_data: Dict[str, Any]) -> Optional[WordEntry]:
        """添加词条"""
        try:
            with db_service.get_session() as session:
                # 检查词条是否已存在
                existing = session.query(WordEntry).filter(
                    WordEntry.word_id == word_data['word_id']
                ).first()
                
                if existing:
                    self.logger.warning(f"词条已存在: {word_data['word_id']}")
                    return None
                
                # 创建词条
                word_entry = WordEntry(
                    word_id=word_data['word_id'],
                    latin_form=word_data['latin_form'],
                    phonetic=word_data.get('phonetic'),
                    word_type=word_data.get('word_type'),
                    notes=word_data.get('notes'),
                    is_favorite=word_data.get('is_favorite', False),
                    sort_order=word_data.get('sort_order', 0)
                )
                
                session.add(word_entry)
                session.flush()  # 获取ID
                
                # 添加释义
                for i, definition_text in enumerate(word_data.get('definitions', [])):
                    definition = Definition(
                        word_entry_id=word_entry.id,
                        definition_text=definition_text,
                        definition_order=i + 1
                    )
                    session.add(definition)
                
                # 添加例句
                for i, example_data in enumerate(word_data.get('examples', [])):
                    example = Example(
                        word_entry_id=word_entry.id,
                        example_text=example_data.get('text', ''),
                        translation=example_data.get('translation'),
                        example_order=i + 1
                    )
                    session.add(example)
                
                session.commit()
                self.logger.info(f"词条添加成功: {word_entry.word_id}")
                return word_entry
                
        except Exception as e:
            self.logger.error(f"添加词条失败: {e}")
            return None
    
    def update_word_entry(self, word_id: str, word_data: Dict[str, Any]) -> bool:
        """更新词条"""
        try:
            with db_service.get_session() as session:
                word_entry = session.query(WordEntry).filter(
                    WordEntry.word_id == word_id
                ).first()
                
                if not word_entry:
                    self.logger.warning(f"词条不存在: {word_id}")
                    return False
                
                # 更新基本信息
                word_entry.latin_form = word_data.get('latin_form', word_entry.latin_form)
                word_entry.phonetic = word_data.get('phonetic', word_entry.phonetic)
                word_entry.word_type = word_data.get('word_type', word_entry.word_type)
                word_entry.notes = word_data.get('notes', word_entry.notes)
                word_entry.is_favorite = word_data.get('is_favorite', word_entry.is_favorite)
                word_entry.sort_order = word_data.get('sort_order', word_entry.sort_order)
                
                # 更新释义
                if 'definitions' in word_data:
                    # 删除旧释义
                    session.query(Definition).filter(
                        Definition.word_entry_id == word_entry.id
                    ).delete()
                    
                    # 添加新释义
                    for i, definition_text in enumerate(word_data['definitions']):
                        definition = Definition(
                            word_entry_id=word_entry.id,
                            definition_text=definition_text,
                            definition_order=i + 1
                        )
                        session.add(definition)
                
                # 更新例句
                if 'examples' in word_data:
                    # 删除旧例句
                    session.query(Example).filter(
                        Example.word_entry_id == word_entry.id
                    ).delete()
                    
                    # 添加新例句
                    for i, example_data in enumerate(word_data['examples']):
                        example = Example(
                            word_entry_id=word_entry.id,
                            example_text=example_data.get('text', ''),
                            translation=example_data.get('translation'),
                            example_order=i + 1
                        )
                        session.add(example)
                
                session.commit()
                self.logger.info(f"词条更新成功: {word_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"更新词条失败: {e}")
            return False
    
    def delete_word_entry(self, word_id: str) -> bool:
        """删除词条"""
        try:
            with db_service.get_session() as session:
                word_entry = session.query(WordEntry).filter(
                    WordEntry.word_id == word_id
                ).first()
                
                if not word_entry:
                    self.logger.warning(f"词条不存在: {word_id}")
                    return False
                
                session.delete(word_entry)
                session.commit()
                self.logger.info(f"词条删除成功: {word_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"删除词条失败: {e}")
            return False
    
    def get_word_entry(self, word_id: str) -> Optional[WordEntry]:
        """获取词条"""
        try:
            with db_service.get_session() as session:
                return session.query(WordEntry).filter(
                    WordEntry.word_id == word_id
                ).first()
        except Exception as e:
            self.logger.error(f"获取词条失败: {e}")
            return None
    
    def get_all_word_entries(self, limit: int = 100, offset: int = 0, 
                           sort_by: str = 'word_id', order: str = 'asc') -> List[WordEntry]:
        """获取所有词条"""
        try:
            with db_service.get_session() as session:
                query = session.query(WordEntry)
                
                # 排序
                if sort_by == 'word_id':
                    query = query.order_by(asc(WordEntry.word_id) if order == 'asc' else desc(WordEntry.word_id))
                elif sort_by == 'latin_form':
                    query = query.order_by(asc(WordEntry.latin_form) if order == 'asc' else desc(WordEntry.latin_form))
                elif sort_by == 'created_at':
                    query = query.order_by(asc(WordEntry.created_at) if order == 'asc' else desc(WordEntry.created_at))
                
                return query.offset(offset).limit(limit).all()
                
        except Exception as e:
            self.logger.error(f"获取词条列表失败: {e}")
            return []
    
    def get_favorite_word_entries(self) -> List[WordEntry]:
        """获取收藏的词条"""
        try:
            with db_service.get_session() as session:
                return session.query(WordEntry).filter(
                    WordEntry.is_favorite == True
                ).order_by(WordEntry.word_id).all()
        except Exception as e:
            self.logger.error(f"获取收藏词条失败: {e}")
            return []
    
    def toggle_favorite(self, word_id: str) -> bool:
        """切换收藏状态"""
        try:
            with db_service.get_session() as session:
                word_entry = session.query(WordEntry).filter(
                    WordEntry.word_id == word_id
                ).first()
                
                if not word_entry:
                    return False
                
                word_entry.is_favorite = not word_entry.is_favorite
                session.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"切换收藏状态失败: {e}")
            return False
    
    def get_word_count(self) -> int:
        """获取词条总数"""
        try:
            with db_service.get_session() as session:
                return session.query(WordEntry).count()
        except Exception as e:
            self.logger.error(f"获取词条总数失败: {e}")
            return 0


# 全局词典服务实例
dictionary_service = DictionaryService()
