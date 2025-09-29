"""
数据验证器
Data Validators
"""

import re
from typing import Any, List, Dict, Optional
from datetime import datetime


class Validators:
    """数据验证器类"""
    
    @staticmethod
    def validate_word_id(word_id: str) -> Dict[str, Any]:
        """验证字序号"""
        result = {'valid': True, 'errors': []}
        
        if not word_id:
            result['valid'] = False
            result['errors'].append('字序号不能为空')
            return result
        
        if len(word_id) > 50:
            result['valid'] = False
            result['errors'].append('字序号长度不能超过50个字符')
        
        # 检查是否包含特殊字符
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fff_-]+$', word_id):
            result['valid'] = False
            result['errors'].append('字序号只能包含字母、数字、中文、下划线和连字符')
        
        return result
    
    @staticmethod
    def validate_latin_form(latin_form: str) -> Dict[str, Any]:
        """验证拉丁写法"""
        result = {'valid': True, 'errors': []}
        
        if not latin_form:
            result['valid'] = False
            result['errors'].append('拉丁写法不能为空')
            return result
        
        if len(latin_form) > 200:
            result['valid'] = False
            result['errors'].append('拉丁写法长度不能超过200个字符')
        
        # 检查是否包含非法字符
        if re.search(r'[<>"\']', latin_form):
            result['valid'] = False
            result['errors'].append('拉丁写法不能包含特殊字符')
        
        return result
    
    @staticmethod
    def validate_phonetic(phonetic: str) -> Dict[str, Any]:
        """验证音标"""
        result = {'valid': True, 'errors': []}
        
        if not phonetic:
            return result  # 音标可以为空
        
        if len(phonetic) > 200:
            result['valid'] = False
            result['errors'].append('音标长度不能超过200个字符')
        
        return result
    
    @staticmethod
    def validate_word_type(word_type: str) -> Dict[str, Any]:
        """验证词性"""
        result = {'valid': True, 'errors': []}
        
        if not word_type:
            return result  # 词性可以为空
        
        if len(word_type) > 50:
            result['valid'] = False
            result['errors'].append('词性长度不能超过50个字符')
        
        # 常见的词性类型
        valid_types = [
            '名词', '动词', '形容词', '副词', '介词', '连词', '感叹词',
            'noun', 'verb', 'adjective', 'adverb', 'preposition', 'conjunction', 'interjection',
            'n.', 'v.', 'adj.', 'adv.', 'prep.', 'conj.', 'interj.'
        ]
        
        if word_type not in valid_types:
            result['warnings'] = result.get('warnings', [])
            result['warnings'].append('词性可能不在常见类型中')
        
        return result
    
    @staticmethod
    def validate_definitions(definitions: List[str]) -> Dict[str, Any]:
        """验证释义列表"""
        result = {'valid': True, 'errors': []}
        
        if not definitions:
            result['valid'] = False
            result['errors'].append('至少需要一个释义')
            return result
        
        if len(definitions) > 10:
            result['valid'] = False
            result['errors'].append('释义数量不能超过10个')
            return result
        
        for i, definition in enumerate(definitions):
            if not definition or not definition.strip():
                result['valid'] = False
                result['errors'].append(f'第{i+1}个释义不能为空')
            elif len(definition) > 1000:
                result['valid'] = False
                result['errors'].append(f'第{i+1}个释义长度不能超过1000个字符')
        
        return result
    
    @staticmethod
    def validate_examples(examples: List[Dict[str, str]]) -> Dict[str, Any]:
        """验证例句列表"""
        result = {'valid': True, 'errors': []}
        
        if not examples:
            return result  # 例句可以为空
        
        if len(examples) > 20:
            result['valid'] = False
            result['errors'].append('例句数量不能超过20个')
            return result
        
        for i, example in enumerate(examples):
            if not isinstance(example, dict):
                result['valid'] = False
                result['errors'].append(f'第{i+1}个例句格式不正确')
                continue
            
            example_text = example.get('text', '')
            translation = example.get('translation', '')
            
            if not example_text or not example_text.strip():
                result['valid'] = False
                result['errors'].append(f'第{i+1}个例句内容不能为空')
            elif len(example_text) > 500:
                result['valid'] = False
                result['errors'].append(f'第{i+1}个例句长度不能超过500个字符')
            
            if translation and len(translation) > 500:
                result['valid'] = False
                result['errors'].append(f'第{i+1}个例句翻译长度不能超过500个字符')
        
        return result
    
    @staticmethod
    def validate_notes(notes: str) -> Dict[str, Any]:
        """验证备注"""
        result = {'valid': True, 'errors': []}
        
        if not notes:
            return result  # 备注可以为空
        
        if len(notes) > 2000:
            result['valid'] = False
            result['errors'].append('备注长度不能超过2000个字符')
        
        return result
    
    @staticmethod
    def validate_url(url: str) -> Dict[str, Any]:
        """验证URL"""
        result = {'valid': True, 'errors': []}
        
        if not url:
            result['valid'] = False
            result['errors'].append('URL不能为空')
            return result
        
        # URL格式验证
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            result['valid'] = False
            result['errors'].append('URL格式不正确')
        
        return result
    
    @staticmethod
    def validate_image_data(image_data: bytes) -> Dict[str, Any]:
        """验证图片数据"""
        result = {'valid': True, 'errors': []}
        
        if not image_data:
            result['valid'] = False
            result['errors'].append('图片数据不能为空')
            return result
        
        # 检查文件大小（5MB限制）
        max_size = 5 * 1024 * 1024  # 5MB
        if len(image_data) > max_size:
            result['valid'] = False
            result['errors'].append('图片大小不能超过5MB')
        
        # 检查文件格式
        valid_formats = [b'\xff\xd8\xff', b'\x89PNG', b'GIF8', b'BM']
        if not any(image_data.startswith(fmt) for fmt in valid_formats):
            result['valid'] = False
            result['errors'].append('不支持的图片格式，请使用JPG、PNG、GIF或BMP格式')
        
        return result
    
    @staticmethod
    def validate_word_entry_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """验证完整词条数据"""
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        # 验证各个字段
        validations = [
            ('word_id', Validators.validate_word_id),
            ('latin_form', Validators.validate_latin_form),
            ('phonetic', Validators.validate_phonetic),
            ('word_type', Validators.validate_word_type),
            ('definitions', Validators.validate_definitions),
            ('examples', Validators.validate_examples),
            ('notes', Validators.validate_notes)
        ]
        
        for field, validator in validations:
            if field in data:
                field_result = validator(data[field])
                if not field_result['valid']:
                    result['valid'] = False
                    result['errors'].extend([f"{field}: {error}" for error in field_result['errors']])
                
                if 'warnings' in field_result:
                    result['warnings'].extend([f"{field}: {warning}" for warning in field_result['warnings']])
        
        return result
