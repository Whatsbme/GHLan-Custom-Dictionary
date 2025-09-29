# 开发指南

## 项目概述

离线词典是一个基于Python和Kivy框架开发的移动端离线词典应用。本项目采用MVC架构模式，支持本地词库管理、搜索、编辑、导出等功能。

## 开发环境设置

### 1. 系统要求
- Python 3.8+
- Windows 10/11, macOS 10.14+, 或 Linux
- 至少2GB RAM
- 1GB可用磁盘空间

### 2. 安装依赖
```bash
# 克隆项目
git clone <repository-url>
cd offline_dictionary

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行应用
```bash
# 开发模式运行
python run.py

# 或者直接运行主模块
python app/main.py
```

## 项目结构说明

```
offline_dictionary/
├── app/                    # 主应用目录
│   ├── __init__.py        # 应用包初始化
│   ├── main.py            # 应用入口点
│   └── config.py          # 配置管理
├── models/                 # 数据模型层
│   ├── __init__.py
│   ├── base.py            # 基础模型类
│   ├── word_entry.py      # 词条模型
│   ├── definition.py      # 释义模型
│   ├── example.py         # 例句模型
│   ├── image.py           # 图片模型
│   ├── bookmark.py        # 书签模型
│   ├── memo_word.py       # 备忘词条模型
│   └── settings.py        # 用户设置模型
├── services/               # 业务逻辑层
│   ├── __init__.py
│   ├── database_service.py    # 数据库服务
│   ├── dictionary_service.py  # 词典服务
│   ├── search_service.py      # 搜索服务
│   ├── export_service.py      # 导出服务
│   ├── import_service.py      # 导入服务
│   └── utility_service.py     # 工具服务
├── views/                  # 视图层
│   ├── __init__.py
│   ├── base_screen.py     # 基础屏幕类
│   ├── main_screen.py     # 主界面
│   └── components/        # UI组件
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── logger.py          # 日志工具
│   ├── validators.py      # 数据验证
│   └── helpers.py         # 辅助函数
├── data/                   # 数据目录
│   ├── database/          # 数据库文件
│   ├── images/            # 图片资源
│   ├── exports/           # 导出文件
│   └── imports/           # 导入文件
├── assets/                 # 静态资源
│   ├── icons/             # 图标
│   ├── themes/            # 主题文件
│   └── fonts/             # 字体文件
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── test_models.py     # 模型测试
│   └── test_services.py   # 服务测试
├── requirements.txt        # 依赖包列表
├── setup.py               # 安装配置
├── buildozer.spec         # Android构建配置
├── run.py                 # 启动脚本
└── README.md              # 项目说明
```

## 开发规范

### 1. 代码风格
- 遵循PEP 8代码风格指南
- 使用4个空格缩进
- 行长度限制为100字符
- 使用有意义的变量和函数名

### 2. 文档字符串
所有公共函数、类和方法都应该包含文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """
    示例函数的文档字符串
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
    
    Returns:
        返回值的描述
    
    Raises:
        ValueError: 当参数无效时抛出
    """
    pass
```

### 3. 类型提示
使用Python类型提示提高代码可读性：

```python
from typing import List, Dict, Optional

def process_words(words: List[str]) -> Dict[str, int]:
    """处理词条列表"""
    pass
```

### 4. 错误处理
- 使用适当的异常类型
- 记录详细的错误信息
- 提供用户友好的错误消息

### 5. 测试
- 为新功能编写单元测试
- 测试覆盖率应达到80%以上
- 使用pytest作为测试框架

## 数据库设计

### 核心表结构
- `word_entries`: 词条主表
- `definitions`: 释义表
- `examples`: 例句表
- `word_images`: 字型图片表
- `bookmarks`: 网址收藏表
- `memo_words`: 备忘词条表
- `user_settings`: 用户设置表

### 数据库操作
使用SQLAlchemy ORM进行数据库操作，所有数据库操作都应该通过服务层进行。

## 移动端构建

### Android构建
```bash
# 安装buildozer
pip install buildozer

# 初始化buildozer配置
buildozer init

# 构建APK
buildozer android debug
```

### 构建配置
编辑`buildozer.spec`文件来配置构建选项：
- 应用名称和版本
- 依赖包列表
- 权限设置
- 图标和资源

## 调试和日志

### 日志配置
应用使用Python标准库的logging模块：
- 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
- 日志文件位置：`~/.offline_dictionary/logs/`
- 日志格式：时间戳 - 模块名 - 级别 - 消息

### 调试技巧
1. 使用IDE的调试器
2. 添加断点进行调试
3. 查看日志文件
4. 使用Kivy的调试工具

## 性能优化

### 数据库优化
- 为常用查询字段添加索引
- 使用连接查询减少数据库访问
- 实现分页加载大量数据

### 内存优化
- 及时释放不需要的对象
- 使用生成器处理大量数据
- 优化图片加载和缓存

### UI优化
- 使用虚拟化列表处理大量数据
- 实现懒加载
- 优化动画性能

## 贡献指南

### 1. 提交代码
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

### 2. 代码审查
- 确保代码符合项目规范
- 添加适当的测试
- 更新相关文档

### 3. 问题报告
使用GitHub Issues报告bug或提出功能请求，包含：
- 详细的问题描述
- 重现步骤
- 预期行为
- 实际行为
- 环境信息

## 常见问题

### Q: 如何添加新的词条字段？
A: 1. 在models/word_entry.py中添加新字段
2. 更新数据库迁移脚本
3. 修改相关的服务和视图代码

### Q: 如何自定义主题？
A: 1. 在assets/themes/目录下创建主题文件
2. 修改app/config.py中的主题配置
3. 更新UI组件使用新主题

### Q: 如何添加新的导出格式？
A: 1. 在services/export_service.py中添加新的导出方法
2. 在views中添加相应的UI选项
3. 更新配置和文档

## 联系信息

开发者信息：
- 开发者：whatsbme
- GitHub：https://github.com/Whatsbme/GHLan-Custom-Dictionary
- 项目主页：https://github.com/Whatsbme/GHLan-Custom-Dictionary

