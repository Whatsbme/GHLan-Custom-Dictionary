"""
辅助函数
Helper Functions
"""

import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import json


def generate_unique_id(prefix: str = "") -> str:
    """生成唯一ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = hashlib.md5(str(datetime.now().microsecond).encode()).hexdigest()[:8]
    return f"{prefix}{timestamp}_{random_part}"


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    if dt is None:
        return ""
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """解析日期时间字符串"""
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def safe_filename(filename: str) -> str:
    """生成安全的文件名"""
    # 移除或替换不安全的字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 限制长度
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename


def encode_image_to_base64(image_path: str) -> str:
    """将图片编码为Base64字符串"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception:
        return ""


def decode_base64_to_image(base64_str: str, output_path: str) -> bool:
    """将Base64字符串解码为图片"""
    try:
        image_data = base64.b64decode(base64_str)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        return True
    except Exception:
        return False


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length-len(suffix)] + suffix


def clean_text(text: str) -> str:
    """清理文本（移除多余空白字符）"""
    if not text:
        return ""
    
    # 移除首尾空白
    text = text.strip()
    
    # 将多个连续空白字符替换为单个空格
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text


def extract_keywords(text: str, min_length: int = 2) -> List[str]:
    """从文本中提取关键词"""
    if not text:
        return []
    
    # 简单的关键词提取（实际应用中可能需要更复杂的算法）
    import re
    
    # 移除标点符号，分割单词
    words = re.findall(r'\b\w+\b', text.lower())
    
    # 过滤长度和常见停用词
    stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
    
    keywords = [word for word in words if len(word) >= min_length and word not in stop_words]
    
    # 去重并保持顺序
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """合并多个字典"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """深度合并字典"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """扁平化嵌套字典"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by(items: List[Any], key_func) -> Dict[str, List[Any]]:
    """按指定函数分组"""
    groups = {}
    for item in items:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """将列表分块"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates(lst: List[Any], key_func=None) -> List[Any]:
    """移除列表中的重复项"""
    if key_func is None:
        key_func = lambda x: x
    
    seen = set()
    result = []
    for item in lst:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    
    return result


def retry_on_exception(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(delay * (2 ** attempt))  # 指数退避
                    else:
                        raise last_exception
            return None
        return wrapper
    return decorator


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()


def is_image_file(filename: str) -> bool:
    """检查是否为图片文件"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    return get_file_extension(filename) in image_extensions


def is_text_file(filename: str) -> bool:
    """检查是否为文本文件"""
    text_extensions = {'.txt', '.md', '.json', '.csv', '.xml', '.html', '.css', '.js', '.py'}
    return get_file_extension(filename) in text_extensions


def create_backup_filename(original_path: str) -> str:
    """创建备份文件名"""
    path = Path(original_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}")


def validate_json(json_str: str) -> bool:
    """验证JSON字符串格式"""
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def get_relative_time(dt: datetime) -> str:
    """获取相对时间描述"""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}小时前"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}分钟前"
    else:
        return "刚刚"

