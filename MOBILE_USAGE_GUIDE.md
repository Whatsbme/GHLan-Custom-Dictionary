# GHLan自定义词典 - 手机使用指南

## 📱 在手机上使用GHLan的三种方案

### 方案一：Android APK（推荐）

这是最简单直接的方式，将应用打包成Android APK文件。

#### 构建要求：
- Windows/Linux/macOS 电脑
- Python 3.8+
- Buildozer

#### 构建步骤：

1. **安装Android SDK和NDK**
```bash
# 安装buildozer
pip install buildozer

# 初始化构建配置
buildozer init

# 构建APK
buildozer android debug
```

2. **手动配置构建环境**
如果自动环境配置失败，可以：
- 下载Android SDK和NDK
- 设置环境变量
- 使用简化的构建脚本

#### 使用APK：
- 下载生成的APK文件到手机
- 启用"未知来源"安装
- 安装并运行

---

### 方案二：Termux（推荐给技术用户）

Termux是一个强大的Android终端模拟器，可以在手机上运行Linux环境。

#### 安装Termux：
1. 从F-Droid或Google Play下载Termux
2. 更新包管理器：`pkg update && pkg upgrade`

#### 在Termux中安装GHLan：
```bash
# 安装Python
pkg install python

# 安装Git
pkg install git

# 克隆项目
git clone https://github.com/Whatsbme/GHLan-Custom-Dictionary.git
cd GHLan-Custom-Dictionary

# 安装依赖
pip install -r requirements.txt

# 更新Kivy配置用于触摸屏
export DISPLAY=:0.0

# 运行应用
python run.py
```

#### Termux限制：
- 需要手动安装Kivy触摸支持
- GUI性能可能不如原生应用
- 需要Termux:X11插件支持GUI

---

### 方案三：Linux Deploy（高级用户）

在手机上运行完整的Linux发行版。

#### 前置条件：
- 已ROOT的Android设备
- Linux Deploy应用

#### 配置步骤：
1. 在Linux Deploy中安装Ubuntu/Debian
2. 配置桌面环境（如LXQT）
3. 安装Python和依赖
4. 通过VNC或直接使用运行应用

#### Linux Deploy优势：
- 完整的Linux环境
- 更接近桌面体验
- 支持完整的GUI应用

#### Linux Deploy限制：
- 需要ROOT权限
- 配置复杂
- 占用存储空间大

---

## 🚀 快速开始（推荐步骤）

### 最简单的方式：
1. **找一台电脑**安装Buildozer
2. **克隆你的GitHub仓库**
3. **运行构建命令**生成APK
4. **将APK传输到手机**安装使用

### 如果你有Python经验：
1. **在手机上安装Termux**
2. **按照Termux方案**一步步配置
3. **在线程环境运行**Python应用

### 如果你是高级用户：
1. **ROOT你的Android设备**
2. **使用Linux Deploy**创建完整Linux环境
3. **享受完整的桌面体验**

---

## ⚡ 各方案对比

| 特性 | Android APK | Termux | Linux Deploy |
|------|-------------|---------|--------------|
| 安装难度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 原生体验 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 存储占用 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 依赖管理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 功能完整性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 常见问题解决

### APK构建失败：
- 检查Android SDK版本
- 确认Python依赖安装完整
- 查看buildozer日志错误

### Termux GUI不显示：
- 安装Termux:X11插件
- 设置DISPLAY环境变量
- 检查Kivy触摸配置

### Linux Deploy启动慢：
- 增加chroot内存分配
- 优化桌面环境配置
- 使用SSD存储

---

## 📞 技术支持

- GitHub Issues: https://github.com/Whatqbme/GHLan-Custom-Dictionary/issues
- 开发者: whatsbme
- 项目主页: https://github.com/Whatqbme/GHLan-Custom-Dictionary

---

选择最适合你的方案，开始在你的手机上使用GHLan自定义词典！
