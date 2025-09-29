"""
搜索服务
Search Service
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
import re
import logging

from models import WordEntry, Definition, Example
from services.database_service import db_service


class SearchService:
    """搜索服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def search_words(self, query: str, search_type: str = 'all', 
                    case_sensitive: bool = False, fuzzy: bool = False) -> List[WordEntry]:
        """搜索词条"""
        try:
            with db_service.get_session() as session:
                if not query.strip():
                    return []
                
                # 构建搜索条件
                search_conditions = []
                
                if not case_sensitive:
                    query = query.lower()
                
                if search_type in ['all', 'word_id']:
                    if case_sensitive:
                        search_conditions.append(WordEntry.word_id.contains(query))
                    else:
                        search_conditions.append(func.lower(WordEntry.word_id).contains(query))
                
                if search_type in ['all', 'latin_form']:
                    if case_sensitive:
                        search_conditions.append(WordEntry.latin_form.contains(query))
                    else:
                        search_conditions.append(func.lower(WordEntry.latin_form).contains(query))
                
                if search_type in ['all', 'phonetic']:
                    if case_sensitive:
                        search_conditions.append(WordEntry.phonetic.contains(query))
                    else:
                        search_conditions.append(func.lower(WordEntry.phonetic).contains(query))
                
                if search_type in ['all', 'definitions']:
                    # 搜索释义
                    definition_query = session.query(WordEntry).join(Definition).filter(
                        func.lower(Definition.definition_text).contains(query)
                    )
                    if definition_query.count() > 0:
                        definition_results = definition_query.all()
                        return definition_results
                
                if search_type in ['all', 'examples']:
                    # 搜索例句
                    example_query = session.query(WordEntry).join(Example).filter(
                        or_(
                            func.lower(Example.example_text).contains(query),
                            func.lower(Example.translation).contains(query)
                        )
                    )
                    if example_query.count() > 0:
                        example_results = example_query.all()
                        return example_results
                
                # 执行搜索
                if search_conditions:
                    results = session.query(WordEntry).filter(
                        or_(*search_conditions)
                    ).order_by(WordEntry.word_id).all()
                    
                    # 模糊搜索处理
                    if fuzzy and results:
                        results = self._apply_fuzzy_search(results, query, case_sensitive)
                    
                    return results
                
                return []
                
        except Exception as e:
            self.logger.error(f"搜索词条失败: {e}")
            return []
    
    def _apply_fuzzy_search(self, results: List[WordEntry], query: str, case_sensitive: bool) -> List[WordEntry]:
        """应用模糊搜索算法"""
        try:
            scored_results = []
            
            for word_entry in results:
                score = 0
                
                # 计算匹配度分数
                if not case_sensitive:
                    word_id = word_entry.word_id.lower()
                    latin_form = word_entry.latin_form.lower()
                else:
                    word_id = word_entry.word_id
                    latin_form = word_entry.latin_form
                
                # 完全匹配得分最高
                if word_id == query or latin_form == query:
                    score += 100
                # 开头匹配
                elif word_id.startswith(query) or latin_form.startswith(query):
                    score += 80
                # 包含匹配
                elif query in word_id or query in latin_form:
                    score += 60
                
                # 长度相似度
                length_diff = abs(len(word_id) - len(query))
                score += max(0, 20 - length_diff)
                
                if score > 0:
                    scored_results.append((score, word_entry))
            
            # 按分数排序
            scored_results.sort(key=lambda x: x[0], reverse=True)
            return [result[1] for result in scored_results]
            
        except Exception as e:
            self.logger.error(f"模糊搜索处理失败: {e}")
            return results
    
    def search_by_pattern(self, pattern: str, search_fields: List[str] = None, 
                         case_sensitive: bool = False, search_translation: bool = True) -> List[WordEntry]:
        """正则表达式搜索"""
        try:
            if not pattern.strip():
                return []
            
            # 编译正则表达式
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
            
            with db_service.get_session() as session:
                all_words = session.query(WordEntry).all()
                matched_words = []
                
                for word_entry in all_words:
                    match_found = False
                    
                    # 检查指定字段
                    if search_fields is None:
                        search_fields = ['word_id', 'latin_form', 'phonetic']
                    
                    for field in search_fields:
                        value = getattr(word_entry, field, '')
                        if value and regex.search(str(value)):
                            match_found = True
                            break
                    
                    # 检查释义
                    if not match_found and 'definitions' in (search_fields or []):
                        for definition in word_entry.definitions:
                            if regex.search(definition.definition_text):
                                match_found = True
                                break
                    
                    # 检查例句
                    if not match_found and 'examples' in (search_fields or []):
                        for example in word_entry.examples:
                            if regex.search(example.example_text):
                                match_found = True
                                break
                            if search_translation and example.translation and regex.search(example.translation):
                                match_found = True
                                break
                    
                    if match_found:
                        matched_words.append(word_entry)
                
                return matched_words
                
        except Exception as e:
            self.logger.error(f"正则搜索失败: {e}")
            return []
    
    def get_search_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """获取搜索建议"""
        try:
            if not query.strip() or len(query) < 2:
                return []
            
            with db_service.get_session() as session:
                suggestions = set()
                
                # 从词条ID获取建议
                word_id_suggestions = session.query(WordEntry.word_id).filter(
                    func.lower(WordEntry.word_id).like(f"%{query.lower()}%")
                ).limit(limit).all()
                
                for suggestion in word_id_suggestions:
                    suggestions.add(suggestion[0])
                
                # 从拉丁写法获取建议
                latin_suggestions = session.query(WordEntry.latin_form).filter(
                    func.lower(WordEntry.latin_form).like(f"%{query.lower()}%")
                ).limit(limit).all()
                
                for suggestion in latin_suggestions:
                    suggestions.add(suggestion[0])
                
                return list(suggestions)[:limit]
                
        except Exception as e:
            self.logger.error(f"获取搜索建议失败: {e}")
            return []
    
    def get_recent_searches(self, limit: int = 10) -> List[str]:
        """获取最近搜索记录"""
        # 这里可以从用户设置中获取最近搜索记录
        # 暂时返回空列表，实际实现需要存储搜索历史
        return []
    
    def save_search_history(self, query: str):
        """保存搜索历史"""
        # 这里可以保存到用户设置中
        # 实际实现需要存储搜索历史
        pass
    
    def multi_field_search(self, query: str, search_fields: List[str], 
                          case_sensitive: bool = False, fuzzy: bool = False,
                          search_translation: bool = True) -> List[WordEntry]:
        """多字段搜索"""
        try:
            if not query.strip():
                return []
            
            with db_service.get_session() as session:
                all_words = session.query(WordEntry).all()
                matched_words = []
                
                for word_entry in all_words:
                    match_found = False
                    
                    # 检查基本字段
                    for field in search_fields:
                        if field in ['word_id', 'latin_form', 'phonetic']:
                            value = getattr(word_entry, field, '')
                            if value and self._match_text(str(value), query, case_sensitive, fuzzy):
                                match_found = True
                                break
                    
                    # 检查释义
                    if not match_found and 'definitions' in search_fields:
                        for definition in word_entry.definitions:
                            if self._match_text(definition.definition_text, query, case_sensitive, fuzzy):
                                match_found = True
                                break
                    
                    # 检查例句
                    if not match_found and 'examples' in search_fields:
                        for example in word_entry.examples:
                            if self._match_text(example.example_text, query, case_sensitive, fuzzy):
                                match_found = True
                                break
                            if search_translation and example.translation:
                                if self._match_text(example.translation, query, case_sensitive, fuzzy):
                                    match_found = True
                                    break
                    
                    if match_found:
                        matched_words.append(word_entry)
                
                return matched_words
                
        except Exception as e:
            self.logger.error(f"多字段搜索失败: {e}")
            return []
    
    def _match_text(self, text: str, query: str, case_sensitive: bool, fuzzy: bool) -> bool:
        """文本匹配"""
        if not text or not query:
            return False
        
        if not case_sensitive:
            text = text.lower()
            query = query.lower()
        
        if fuzzy:
            # 简单的模糊匹配
            return query in text
        else:
            # 精确匹配
            return text == query
    
    def advanced_search(self, search_params: dict) -> List[WordEntry]:
        """高级搜索"""
        try:
            query = search_params.get('query', '')
            search_mode = search_params.get('search_mode', 'fuzzy')
            search_fields = search_params.get('search_fields', ['word_id', 'latin_form'])
            case_sensitive = search_params.get('case_sensitive', False)
            search_translation = search_params.get('search_translation', True)
            
            if search_mode == 'regex':
                return self.search_by_pattern(
                    query, 
                    search_fields, 
                    case_sensitive, 
                    search_translation
                )
            else:
                fuzzy = search_mode == 'fuzzy'
                return self.multi_field_search(
                    query,
                    search_fields,
                    case_sensitive,
                    fuzzy,
                    search_translation
                )
                
        except Exception as e:
            self.logger.error(f"高级搜索失败: {e}")
            return []


# 全局搜索服务实例
search_service = SearchService()
