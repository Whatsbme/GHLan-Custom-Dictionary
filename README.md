# GHL自定义词典 (GALan custom Dictionary)

一个功能完整的移动端Python离线词典应用，支持本地词库管理、搜索、编辑、导出等功能。

## 功能特性

### 核心功能
- **本地词库存储**: 使用SQLite数据库存储词条信息
- **词条管理**: 支持增删改查、排序和搜索
- **自定义编辑**: 支持字序号、字型图片、拉丁写法、音标、词性、释义、例句、备注等
- **多格式导出**: 支持导出为PDF、Excel和字典格式
- **高级搜索**: 支持模糊搜索、正则表达式搜索、多字段搜索

### 工具功能
- **网址检阅和收藏**: 管理常用网址
- **备忘词条**: 快速记录临时词条
- **字符编辑**: 支持IDS描述符号编辑
- **数据备份**: 自动备份和恢复功能

### 用户设置
- **收藏夹管理**: 分类管理收藏词条
- **主题切换**: 支持明暗主题
- **字体设置**: 可调节字体大小
- **个性化配置**: 丰富的用户设置选项

## 技术架构

### 技术栈
- **GUI框架**: Kivy + KivyMD (Material Design)
- **数据库**: SQLite + SQLAlchemy ORM
- **文件处理**: Pillow (图片), ReportLab (PDF), openpyxl (Excel)
- **移动端构建**: Buildozer

### 架构模式
采用MVC + 服务层架构：
- **Model层**: 数据模型和数据库操作
- **View层**: 用户界面组件
- **Controller层**: 业务逻辑控制
- **Service层**: 核心业务服务

## 项目结构

```
offline_dictionary/
├── app/                    # 主应用目录
├── models/                 # 数据模型层
├── services/               # 业务逻辑层
├── views/                  # 视图层
├── utils/                  # 工具模块
├── data/                   # 数据目录
├── assets/                 # 静态资源
└── tests/                  # 测试目录
```

## 安装和运行

### 开发环境
```bash
# 克隆项目
git clone <repository-url>
cd offline_dictionary

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app/main.py
```

### Android构建
```bash
# 安装buildozer
pip install buildozer

# 构建APK
buildozer android debug
```

## 数据库设计

### 核心表结构
- `word_entries`: 词条主表
- `definitions`: 释义表
- `examples`: 例句表
- `word_images`: 字型图片表
- `bookmarks`: 网址收藏表
- `memo_words`: 备忘词条表
- `user_settings`: 用户设置表

## 开发指南

### 添加新功能
1. 在`models/`中定义数据模型
2. 在`services/`中实现业务逻辑
3. 在`views/`中创建用户界面
4. 更新配置文件

### 代码规范
- 使用Python类型提示
- 遵循PEP 8代码风格
- 添加适当的文档字符串
- 编写单元测试

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 开发者

**whatsbme** - GHLan自定义词典项目
