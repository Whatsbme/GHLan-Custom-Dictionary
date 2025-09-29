# GHLan自定义字典 - API文档

## 📋 概述

GHLan自定义字典提供了完整的API接口，支持词条管理、搜索、导入导出等功能。本文档详细描述了所有可用的API接口。

## 🏗️ 架构

### 服务层 (Services)
- `DictionaryService` - 词条管理服务
- `SearchService` - 搜索服务
- `ImportService` - 导入服务
- `ExportService` - 导出服务
- `BookmarkService` - 书签服务
- `MemoService` - 备忘服务
- `IdsService` - IDS符号服务

### 数据模型 (Models)
- `WordEntry` - 词条模型
- `Definition` - 释义模型
- `Example` - 例句模型
- `Bookmark` - 书签模型
- `MemoWord` - 备忘模型
- `IdsSymbol` - IDS符号模型

## 📚 词条管理API

### DictionaryService

#### 添加词条
```python
def add_word_entry(word_data: Dict[str, Any]) -> Optional[WordEntry]
```

**参数:**
- `word_data`: 词条数据字典
  - `word_id` (str): 词条ID
  - `latin_form` (str): 拉丁形式
  - `phonetic` (str, optional): 音标
  - `word_type` (str, optional): 词性
  - `definitions` (List[str]): 释义列表
  - `examples` (List[Dict]): 例句列表
  - `notes` (str, optional): 备注

**返回:**
- `WordEntry`: 成功创建的词条对象
- `None`: 创建失败

**示例:**
```python
word_data = {
    'word_id': 'test001',
    'latin_form': 'testus',
    'phonetic': '/ˈtestəs/',
    'word_type': 'noun',
    'definitions': ['测试', '试验'],
    'examples': [
        {'text': 'This is a test.', 'translation': '这是一个测试。'}
    ],
    'notes': '测试词条'
}
word_entry = dictionary_service.add_word_entry(word_data)
```

#### 获取词条
```python
def get_word_entry_by_id(word_id: int) -> Optional[WordEntry]
def get_word_entry_by_word_id(word_id: str) -> Optional[WordEntry]
def get_all_word_entries() -> List[WordEntry]
```

#### 更新词条
```python
def update_word_entry(word_entry: WordEntry) -> bool
```

#### 删除词条
```python
def delete_word_entry(word_id: int) -> bool
```

#### 添加图片
```python
def add_image_to_word_entry(word_entry_id: int, image_data: bytes, image_type: str) -> bool
```

## 🔍 搜索API

### SearchService

#### 精确搜索
```python
def search_by_latin_form(latin_form: str) -> List[WordEntry]
def search_by_phonetic(phonetic: str) -> List[WordEntry]
def search_by_definition(definition: str) -> List[WordEntry]
```

#### 模糊搜索
```python
def fuzzy_search(query: str, search_fields: List[str] = None) -> List[WordEntry]
```

**参数:**
- `query`: 搜索查询
- `search_fields`: 搜索字段列表，默认为所有字段

#### 正则搜索
```python
def search_by_pattern(pattern: str, search_fields: List[str] = None) -> List[WordEntry]
```

#### 多字段搜索
```python
def multi_field_search(query: str, search_fields: List[str], 
                      case_sensitive: bool = False, fuzzy: bool = False) -> List[WordEntry]
```

#### 高级搜索
```python
def advanced_search(search_params: Dict[str, Any]) -> List[WordEntry]
```

**参数:**
- `search_params`: 搜索参数字典
  - `query`: 搜索查询
  - `search_type`: 搜索类型 ('exact', 'fuzzy', 'regex')
  - `search_fields`: 搜索字段
  - `case_sensitive`: 是否区分大小写
  - `search_translation`: 是否搜索翻译

## 📥 导入API

### ImportService

#### Excel导入
```python
def import_from_excel(filepath: str, progress_callback=None) -> Dict[str, Any]
```

**返回:**
```python
{
    'success': int,      # 成功导入数量
    'failed': int,       # 失败数量
    'errors': List[str], # 错误信息列表
    'total': int         # 总数量
}
```

#### CSV导入
```python
def import_from_csv(filepath: str, progress_callback=None) -> Dict[str, Any]
```

#### JSON导入
```python
def import_from_json(filepath: str) -> Dict[str, Any]
```

## 📤 导出API

### ExportService

#### PDF导出
```python
def export_to_pdf(word_entries: List[WordEntry] = None, filename: str = None, 
                 progress_callback=None) -> str
```

#### Excel导出
```python
def export_to_excel(word_entries: List[WordEntry] = None, filename: str = None,
                   progress_callback=None) -> str
```

#### CSV导出
```python
def export_to_csv(word_entries: List[WordEntry] = None, filename: str = None,
                 progress_callback=None) -> str
```

## 🔖 书签API

### BookmarkService

#### 添加书签
```python
def add_bookmark(title: str, url: str, category: str = '未分类', 
                description: Optional[str] = None) -> Optional[Bookmark]
```

#### 获取书签
```python
def get_bookmark_by_id(bookmark_id: int) -> Optional[Bookmark]
def get_all_bookmarks() -> List[Bookmark]
```

#### 更新书签
```python
def update_bookmark(bookmark_id: int, title: Optional[str] = None,
                   url: Optional[str] = None, category: Optional[str] = None,
                   description: Optional[str] = None) -> bool
```

#### 删除书签
```python
def delete_bookmark(bookmark_id: int) -> bool
```

#### 搜索书签
```python
def search_bookmarks(query: str) -> List[Bookmark]
```

## 📝 备忘API

### MemoService

#### 添加备忘
```python
def add_memo_word(content: str, priority: int = 3) -> Optional[MemoWord]
```

#### 获取备忘
```python
def get_memo_word_by_id(memo_id: int) -> Optional[MemoWord]
def get_all_memo_words(include_completed: bool = True) -> List[MemoWord]
```

#### 更新备忘
```python
def update_memo_word(memo_id: int, content: Optional[str] = None,
                    priority: Optional[int] = None, 
                    is_completed: Optional[bool] = None) -> bool
```

#### 完成备忘
```python
def complete_memo_word(memo_id: int) -> bool
```

#### 删除备忘
```python
def delete_memo_word(memo_id: int) -> bool
```

#### 搜索备忘
```python
def search_memo_words(query: str, include_completed: bool = True) -> List[MemoWord]
```

## 🔤 IDS符号API

### IdsService

#### 添加IDS符号
```python
def add_ids_symbol(name: str, ids_string: Optional[str] = None,
                  image_data: Optional[bytes] = None, 
                  description: Optional[str] = None) -> Optional[IdsSymbol]
```

#### 获取IDS符号
```python
def get_ids_symbol_by_id(symbol_id: int) -> Optional[IdsSymbol]
def get_ids_symbol_by_name(name: str) -> Optional[IdsSymbol]
def get_all_ids_symbols() -> List[IdsSymbol]
```

#### 更新IDS符号
```python
def update_ids_symbol(symbol_id: int, name: Optional[str] = None,
                     ids_string: Optional[str] = None,
                     image_data: Optional[bytes] = None,
                     description: Optional[str] = None) -> bool
```

#### 删除IDS符号
```python
def delete_ids_symbol(symbol_id: int) -> bool
```

#### 渲染IDS为图片
```python
def render_ids_to_image(ids_string: str, size: tuple = (200, 200),
                       bg_color: str = "white", text_color: str = "black") -> bytes
```

## 🎨 主题API

### ThemeManager

#### 应用主题
```python
def apply_theme() -> None
def apply_ink_theme() -> None
```

#### 切换主题
```python
def toggle_ink_theme() -> None
```

#### 设置主题样式
```python
def set_theme_style(style: str) -> None
def set_primary_palette(palette: str) -> None
def set_accent_palette(palette: str) -> None
```

#### 设置字体
```python
def set_font_size(size: int) -> None
def set_font_family(family: str) -> None
```

## 🔧 配置API

### Config

#### 获取配置
```python
def get(section: str, key: str, fallback: str = None) -> str
def get_int(section: str, key: str, fallback: int = None) -> int
def get_bool(section: str, key: str, fallback: bool = None) -> bool
```

#### 设置配置
```python
def set(section: str, key: str, value: str) -> None
```

#### 保存配置
```python
def save() -> None
```

## 📊 数据模型

### WordEntry
```python
class WordEntry:
    id: int
    word_id: str
    latin_form: str
    phonetic: Optional[str]
    word_type: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # 关联对象
    definitions: List[Definition]
    examples: List[Example]
    images: List[WordImage]
```

### Definition
```python
class Definition:
    id: int
    word_entry_id: int
    definition_text: str
    definition_order: int
    created_at: datetime
    updated_at: datetime
```

### Example
```python
class Example:
    id: int
    word_entry_id: int
    example_text: str
    translation: str
    example_order: int
    created_at: datetime
    updated_at: datetime
```

### Bookmark
```python
class Bookmark:
    id: int
    title: str
    url: str
    category: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### MemoWord
```python
class MemoWord:
    id: int
    content: str
    priority: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime
```

### IdsSymbol
```python
class IdsSymbol:
    id: int
    name: str
    ids_string: Optional[str]
    image_data: Optional[bytes]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
```

## 🚨 错误处理

### 异常类型
- `DatabaseError`: 数据库操作错误
- `ValidationError`: 数据验证错误
- `FileNotFoundError`: 文件未找到错误
- `ImportError`: 导入错误
- `ExportError`: 导出错误

### 错误响应格式
```python
{
    'success': False,
    'error': 'Error message',
    'error_code': 'ERROR_CODE',
    'details': {}
}
```

## 📝 使用示例

### 完整的词条管理流程
```python
from services.dictionary_service import dictionary_service
from services.search_service import search_service

# 1. 添加词条
word_data = {
    'word_id': 'example001',
    'latin_form': 'exemplum',
    'phonetic': '/ɪɡˈzempləm/',
    'word_type': 'noun',
    'definitions': ['例子', '范例'],
    'examples': [
        {'text': 'This is an example.', 'translation': '这是一个例子。'}
    ],
    'notes': '示例词条'
}
word_entry = dictionary_service.add_word_entry(word_data)

# 2. 搜索词条
results = search_service.search_by_latin_form('exemplum')
print(f"找到 {len(results)} 个结果")

# 3. 更新词条
word_entry.notes = '更新的备注'
dictionary_service.update_word_entry(word_entry)

# 4. 删除词条
dictionary_service.delete_word_entry(word_entry.id)
```

### 批量导入导出
```python
from services.import_service import import_service
from services.export_service import export_service

# 导入Excel文件
def progress_callback(current, total, item):
    print(f"进度: {current}/{total} - {item}")

result = import_service.import_from_excel('words.xlsx', progress_callback)
print(f"导入完成: 成功 {result['success']} 条，失败 {result['failed']} 条")

# 导出为PDF
filepath = export_service.export_to_pdf(progress_callback=progress_callback)
print(f"导出完成: {filepath}")
```

## 🔄 版本历史

- **v1.0.0** - 初始版本，基础功能
- **v1.1.0** - 添加搜索功能
- **v1.2.0** - 添加导入导出功能
- **v1.3.0** - 添加书签和备忘功能
- **v1.4.0** - 添加IDS符号功能
- **v1.5.0** - 添加水墨主题

## 📞 支持

如有API使用问题，请参考：
- 用户手册: `docs/USER_MANUAL.md`
- 开发者指南: `docs/DEVELOPER_GUIDE.md`
- 问题反馈: GitHub Issues







