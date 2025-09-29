# GHLan自定义字典 - 开发者指南

## 🛠️ 开发环境设置

### 系统要求
- Python 3.13+
- Kivy 2.3.1+
- KivyMD 1.2.0+
- SQLAlchemy 2.0.0+
- 其他依赖见 `requirements.txt`

### 开发环境安装
```bash
# 克隆项目
git clone <repository-url>
cd GHLan

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/

# 启动应用
python run.py
```

## 🏗️ 项目架构

### 目录结构
```
GHLan/
├── app/                    # 应用核心
│   ├── main.py            # 主应用类
│   └── config.py          # 配置管理
├── models/                # 数据模型
│   ├── base.py           # 基础模型
│   ├── word_entry.py     # 词条模型
│   ├── definition.py     # 释义模型
│   ├── example.py        # 例句模型
│   ├── bookmark.py       # 书签模型
│   ├── memo_word.py      # 备忘模型
│   ├── ids_symbol.py     # IDS符号模型
│   └── settings.py       # 设置模型
├── services/              # 业务逻辑层
│   ├── database_service.py    # 数据库服务
│   ├── dictionary_service.py  # 词条服务
│   ├── search_service.py      # 搜索服务
│   ├── import_service.py      # 导入服务
│   ├── export_service.py      # 导出服务
│   ├── bookmark_service.py    # 书签服务
│   ├── memo_service.py        # 备忘服务
│   └── ids_service.py         # IDS服务
├── views/                 # 视图层
│   ├── base_screen.py    # 基础屏幕
│   ├── main_screen.py    # 主界面
│   ├── word_list_screen.py    # 词条列表
│   ├── word_detail_screen.py  # 词条详情
│   ├── word_edit_screen.py    # 词条编辑
│   ├── advanced_search_screen.py # 高级搜索
│   ├── settings_screen.py     # 设置界面
│   ├── tools_screen.py        # 工具界面
│   └── components/            # UI组件
│       ├── ink_card.py        # 水墨卡片
│       ├── ink_button.py      # 水墨按钮
│       ├── ink_input.py       # 水墨输入
│       └── ink_navigation.py  # 水墨导航
├── utils/                 # 工具类
│   ├── logger.py         # 日志工具
│   ├── theme_manager.py  # 主题管理
│   └── ink_theme.py      # 水墨主题
├── tests/                 # 测试代码
│   ├── test_base.py      # 测试基础
│   ├── test_views.py     # 视图测试
│   ├── test_integration.py # 集成测试
│   ├── test_ui.py        # UI测试
│   └── test_performance.py # 性能测试
├── assets/                # 静态资源
│   ├── icons/            # 图标文件
│   ├── themes/           # 主题文件
│   └── fonts/            # 字体文件
├── docs/                  # 文档
│   ├── API.md            # API文档
│   ├── USER_MANUAL.md    # 用户手册
│   └── DEVELOPER_GUIDE.md # 开发者指南
└── requirements.txt       # 依赖列表
```

### 架构模式
项目采用 **MVC + Service Layer** 架构：

- **Model**: 数据模型层，定义数据结构
- **View**: 视图层，用户界面组件
- **Controller**: 控制器层，处理用户交互
- **Service**: 服务层，业务逻辑处理

## 🔧 核心组件开发

### 1. 数据模型开发

#### 创建新模型
```python
from sqlalchemy import Column, Integer, String, DateTime, func
from models.base import Base

class NewModel(Base):
    """新模型类"""
    __tablename__ = 'new_table'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='名称')
    description = Column(String(1000), nullable=True, comment='描述')
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<NewModel(name='{self.name}')>"
```

#### 模型最佳实践
- 继承自 `Base` 类
- 包含 `id` 主键
- 添加 `created_at` 和 `updated_at` 时间戳
- 实现 `to_dict()` 方法
- 实现 `__repr__()` 方法
- 添加适当的注释

### 2. 服务层开发

#### 创建新服务
```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.new_model import NewModel
from services.database_service import db_service
from utils.logger import get_logger

class NewService:
    """新服务类"""
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
    
    def add_item(self, name: str, description: str = None) -> Optional[NewModel]:
        """添加新项目"""
        with db_service.get_session() as session:
            try:
                item = NewModel(name=name, description=description)
                session.add(item)
                session.commit()
                session.refresh(item)
                self.logger.info(f"添加项目成功: {item.name}")
                return item
            except Exception as e:
                session.rollback()
                self.logger.error(f"添加项目失败: {e}")
                return None
    
    def get_item_by_id(self, item_id: int) -> Optional[NewModel]:
        """根据ID获取项目"""
        with db_service.get_session() as session:
            return session.query(NewModel).filter_by(id=item_id).first()
    
    def get_all_items(self) -> List[NewModel]:
        """获取所有项目"""
        with db_service.get_session() as session:
            return session.query(NewModel).order_by(NewModel.created_at.desc()).all()
    
    def update_item(self, item_id: int, name: str = None, description: str = None) -> bool:
        """更新项目"""
        with db_service.get_session() as session:
            try:
                item = session.query(NewModel).filter_by(id=item_id).first()
                if item:
                    if name:
                        item.name = name
                    if description:
                        item.description = description
                    session.commit()
                    self.logger.info(f"更新项目成功: {item.name}")
                    return True
                return False
            except Exception as e:
                session.rollback()
                self.logger.error(f"更新项目失败: {e}")
                return False
    
    def delete_item(self, item_id: int) -> bool:
        """删除项目"""
        with db_service.get_session() as session:
            try:
                item = session.query(NewModel).filter_by(id=item_id).first()
                if item:
                    session.delete(item)
                    session.commit()
                    self.logger.info(f"删除项目成功: ID {item_id}")
                    return True
                return False
            except Exception as e:
                session.rollback()
                self.logger.error(f"删除项目失败: {e}")
                return False

# 全局服务实例
new_service = NewService()
```

#### 服务层最佳实践
- 使用数据库会话管理
- 实现完整的CRUD操作
- 添加适当的错误处理
- 记录操作日志
- 使用类型提示
- 提供全局服务实例

### 3. 视图层开发

#### 创建新屏幕
```python
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from views.base_screen import BaseScreen
from utils.logger import get_logger

class NewScreen(BaseScreen):
    """新屏幕类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
    
    def on_enter(self):
        """进入屏幕时调用"""
        self.logger.info("进入新屏幕")
        self._load_data()
    
    def on_leave(self):
        """离开屏幕时调用"""
        self.logger.info("离开新屏幕")
    
    def get_screen_title(self) -> str:
        """获取屏幕标题"""
        return "新屏幕"
    
    def _load_data(self):
        """加载数据"""
        try:
            # 加载数据逻辑
            self.logger.info("数据加载完成")
        except Exception as e:
            self.logger.error(f"数据加载失败: {e}")
            self.show_snackbar("数据加载失败")
    
    def _setup_ui(self):
        """设置UI"""
        # UI设置逻辑
        pass
```

#### 视图层最佳实践
- 继承自 `BaseScreen`
- 实现 `on_enter()` 和 `on_leave()` 方法
- 实现 `get_screen_title()` 方法
- 添加适当的错误处理
- 使用日志记录
- 分离UI逻辑和业务逻辑

### 4. UI组件开发

#### 创建水墨风格组件
```python
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from utils.ink_theme import ink_theme
from utils.logger import get_logger

class InkNewComponent(MDCard):
    """水墨风格新组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self._setup_ink_style()
    
    def _setup_ink_style(self):
        """设置水墨风格"""
        # 水墨风格设置
        self.elevation = 2
        self.radius = [dp(12), dp(12), dp(12), dp(12)]
        self.md_bg_color = ink_theme.get_color('paper_white')
        
        # 设置水墨边框
        with self.canvas.before:
            Color(*ink_theme.get_color('border_light'))
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius
            )
        
        self.bind(pos=self._update_border, size=self._update_border)
    
    def _update_border(self, *args):
        """更新边框"""
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = self.pos
            self.border_rect.size = self.size
```

#### UI组件最佳实践
- 使用水墨主题颜色
- 实现响应式设计
- 添加动画效果
- 支持主题切换
- 提供良好的用户体验

## 🧪 测试开发

### 单元测试
```python
import unittest
from tests.test_base import BaseTestCase
from services.new_service import new_service

class TestNewService(BaseTestCase):
    """新服务测试"""
    
    def test_add_item(self):
        """测试添加项目"""
        item = new_service.add_item("测试项目", "测试描述")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "测试项目")
        self.assertEqual(item.description, "测试描述")
    
    def test_get_item_by_id(self):
        """测试根据ID获取项目"""
        item = new_service.add_item("测试项目")
        retrieved_item = new_service.get_item_by_id(item.id)
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.name, "测试项目")
    
    def test_update_item(self):
        """测试更新项目"""
        item = new_service.add_item("测试项目")
        success = new_service.update_item(item.id, "更新的项目")
        self.assertTrue(success)
        
        updated_item = new_service.get_item_by_id(item.id)
        self.assertEqual(updated_item.name, "更新的项目")
    
    def test_delete_item(self):
        """测试删除项目"""
        item = new_service.add_item("测试项目")
        success = new_service.delete_item(item.id)
        self.assertTrue(success)
        
        deleted_item = new_service.get_item_by_id(item.id)
        self.assertIsNone(deleted_item)
```

### 集成测试
```python
import unittest
from tests.test_base import BaseTestCase
from services.new_service import new_service
from services.dictionary_service import dictionary_service

class TestIntegration(BaseTestCase):
    """集成测试"""
    
    def test_service_integration(self):
        """测试服务集成"""
        # 创建测试数据
        item = new_service.add_item("测试项目")
        word_entry = self.create_test_word_entry()
        
        # 验证数据创建
        self.assertIsNotNone(item.id)
        self.assertIsNotNone(word_entry.id)
        
        # 测试数据关联
        # 这里可以测试不同服务之间的数据交互
```

### UI测试
```python
import unittest
from tests.test_base import UITestCase
from views.new_screen import NewScreen

class TestNewScreen(UITestCase):
    """新屏幕UI测试"""
    
    def test_screen_initialization(self):
        """测试屏幕初始化"""
        def test_screen():
            screen = NewScreen()
            self.assertIsNotNone(screen)
            self.assertEqual(screen.get_screen_title(), "新屏幕")
        
        self.run_ui_test(test_screen)
```

### 性能测试
```python
import unittest
from tests.test_base import PerformanceTestCase
from services.new_service import new_service

class TestNewServicePerformance(PerformanceTestCase):
    """新服务性能测试"""
    
    def test_bulk_operations(self):
        """测试批量操作性能"""
        # 创建大量数据
        for i in range(1000):
            new_service.add_item(f"测试项目 {i}")
        
        # 性能断言
        self.assert_performance(5.0)  # 应该在5秒内完成
```

## 📦 打包部署

### 桌面应用打包
```bash
# 使用PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed run.py

# 使用cx_Freeze
pip install cx_Freeze
python setup.py build
```

### 移动应用打包
```bash
# 安装Buildozer
pip install buildozer

# 初始化构建配置
buildozer init

# 构建Android APK
buildozer android debug

# 构建iOS应用
buildozer ios debug
```

### Docker部署
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

## 🔧 配置管理

### 环境配置
```python
# config.py
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.debug = os.getenv('DEBUG', 'True').lower() == 'true'
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        
        if self.environment == 'production':
            self.log_level = 'WARNING'
        else:
            self.log_level = 'DEBUG'
```

### 日志配置
```python
# logger.py
import logging
import os

def setup_logger(level='INFO'):
    """设置日志"""
    log_level = getattr(logging, level.upper())
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
```

## 🚀 性能优化

### 数据库优化
```python
# 使用索引
class WordEntry(Base):
    __tablename__ = 'word_entries'
    
    id = Column(Integer, primary_key=True)
    word_id = Column(String(50), unique=True, index=True)  # 添加索引
    latin_form = Column(String(255), index=True)  # 添加索引
```

### 查询优化
```python
# 使用预加载
def get_word_entries_with_relations():
    with db_service.get_session() as session:
        return session.query(WordEntry)\
            .options(joinedload(WordEntry.definitions))\
            .options(joinedload(WordEntry.examples))\
            .all()
```

### 缓存优化
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_theme_colors(theme_name):
    """缓存主题颜色"""
    return load_theme_colors(theme_name)
```

## 🔒 安全考虑

### 输入验证
```python
def validate_word_data(word_data):
    """验证词条数据"""
    required_fields = ['word_id', 'latin_form']
    
    for field in required_fields:
        if not word_data.get(field):
            raise ValueError(f"缺少必需字段: {field}")
    
    # 验证数据格式
    if len(word_data['word_id']) > 50:
        raise ValueError("字序号长度不能超过50个字符")
```

### SQL注入防护
```python
# 使用参数化查询
def search_by_latin_form(latin_form):
    with db_service.get_session() as session:
        return session.query(WordEntry)\
            .filter(WordEntry.latin_form == latin_form)\
            .all()
```

### 文件上传安全
```python
import os
from pathlib import Path

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

def is_allowed_file(filename):
    """检查文件类型"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """生成安全文件名"""
    return os.path.basename(filename)
```

## 📊 监控和调试

### 性能监控
```python
import time
from functools import wraps

def monitor_performance(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper
```

### 错误追踪
```python
import traceback
import logging

def log_exception(func):
    """异常日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"函数 {func.__name__} 发生异常: {e}")
            logging.error(traceback.format_exc())
            raise
    return wrapper
```

## 🤝 贡献指南

### 代码规范
- 使用PEP 8代码风格
- 添加类型提示
- 编写文档字符串
- 添加单元测试

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建过程或辅助工具的变动
```

### 拉取请求
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建拉取请求
5. 等待代码审查

## 📞 技术支持

### 开发社区
- GitHub Issues: 问题报告和功能请求
- 讨论区: 技术讨论和经验分享
- 文档: 详细的开发文档

### 联系方式
- 邮箱: dev@ghlan.com
- 微信群: GHLan开发者群
- QQ群: 123456789

---

**版本**: 1.5.0  
**更新日期**: 2025年9月  
**维护者**: GHLan开发团队







