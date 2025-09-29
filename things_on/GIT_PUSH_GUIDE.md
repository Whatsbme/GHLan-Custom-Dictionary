# Git 安装和项目推送指南

## 🚀 GitHub Actions 的作用

GitHub Actions 在您的项目中充当**自动化构建服务器**：

### 主要功能
1. **自动构建 Android APK**：无需本地安装 Android SDK、NDK 等复杂环境
2. **云端编译**：使用 GitHub 提供的 Ubuntu 虚拟机进行构建
3. **持续集成**：每次代码推送时自动重新构建 APK
4. **版本管理**：每次构建都有对应的代码版本

### 工作流程
1. **触发**：推送到 GitHub 或手动触发
2. **环境准备**：安装 Python、Java、编译工具
3. **构建**：运行 `buildozer android debug` 命令
4. **输出**：生成 APK 文件并上传为构建产物

## 📦 项目推送步骤

### 第1步：安装 Git

#### 方法一：下载安装包（推荐）
1. 访问 [Git 官网](https://git-scm.com/download/win)
2. 下载 Windows 版本安装包
3. 运行安装程序，使用默认设置
4. 重启 PowerShell 或命令提示符

#### 方法二：使用包管理器
```powershell
# 如果有 Chocolatey
choco install git

# 如果有 Scoop
scoop install git

# 如果有 winget（需要网络连接）
winget install Git.Git
```

### 第2步：配置 Git
```bash
# 设置用户名和邮箱
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱@example.com"
```

### 第3步：推送项目到 GitHub
```bash
# 在项目目录中执行
git init
git add .
git commit -m "GHLan自定义字典完整版本 v1.0.0"

# 添加远程仓库
git remote add origin https://github.com/Whatsbme/GHLan-Custom-Dictionary.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 第4步：触发 GitHub Actions 构建
1. 登录 GitHub，进入 [GHLan-Custom-Dictionary](https://github.com/Whatsbme/GHLan-Custom-Dictionary) 仓库
2. 点击 **Actions** 标签页
3. 选择 **Build Android APK** 工作流
4. 点击 **Run workflow** 手动触发构建
5. 等待构建完成（约 10-15 分钟）

### 第5步：下载 APK
1. 构建完成后，点击构建记录
2. 在 **Artifacts** 部分下载 `ghlan-dictionary-apk`
3. 解压 zip 文件，获得 APK 文件

## 🔧 故障排除

### Git 安装问题
- 确保有管理员权限
- 检查网络连接
- 尝试使用不同的安装方法

### 推送问题
- 检查 GitHub 用户名和密码
- 确认仓库地址正确
- 检查网络连接

### 构建问题
- 查看 GitHub Actions 日志
- 检查 `buildozer.spec` 配置
- 确保所有文件都已推送

## 📱 使用 APK

### 安装到手机
1. 将 APK 文件传输到手机
2. 开启"未知来源"安装权限
3. 点击 APK 文件安装
4. 开始使用 GHLan自定义字典

### 系统要求
- Android 5.0 或更高版本
- 100MB 可用存储空间
- 2GB RAM（推荐）

## 🎯 总结

GitHub Actions 让您无需复杂的本地环境就能构建 Android APK，是最推荐的方案！

**完整流程**：
1. 安装 Git
2. 推送项目到 GitHub
3. 触发 GitHub Actions 构建
4. 下载 APK 并安装到手机
5. 开始使用应用

**优势**：
- 无需本地 Android 开发环境
- 自动化构建流程
- 云端构建，不占用本地资源
- 版本管理和追踪


