# GHLan自定义字典 - 快速推送指南

## 🎯 目标
将 GHLan自定义字典 项目推送到 GitHub，并使用 GitHub Actions 自动构建 Android APK

## 📋 前置要求
- Windows 10/11 系统
- 网络连接
- GitHub 账户

## 🚀 快速开始

### 第1步：安装 Git
1. 访问 [Git 官网](https://git-scm.com/download/win)
2. 下载 **Git for Windows**
3. 运行安装程序，使用默认设置
4. 重启命令提示符或 PowerShell

### 第2步：运行推送脚本
1. 双击运行 `push_to_github.bat`
2. 按照提示操作
3. 等待推送完成

### 第3步：触发 GitHub Actions 构建
1. 访问 [GHLan-Custom-Dictionary](https://github.com/Whatsbme/GHLan-Custom-Dictionary)
2. 点击 **Actions** 标签
3. 选择 **Build Android APK**
4. 点击 **Run workflow** → **Run workflow**
5. 等待构建完成（约 10-15 分钟）

### 第4步：下载 APK
1. 构建完成后，点击构建记录
2. 在 **Artifacts** 部分下载 `ghlan-dictionary-apk`
3. 解压 zip 文件，获得 APK

### 第5步：安装到手机
1. 将 APK 传输到手机
2. 开启"未知来源"安装权限
3. 点击 APK 文件安装
4. 开始使用应用

## 🔧 手动操作（如果脚本失败）

### 1. 初始化 Git 仓库
```bash
git init
git add .
git commit -m "GHLan自定义字典完整版本 v1.0.0"
```

### 2. 添加远程仓库
```bash
git remote add origin https://github.com/Whatsbme/GHLan-Custom-Dictionary.git
```

### 3. 推送到 GitHub
```bash
git branch -M main
git push -u origin main
```

## 📱 应用功能

### 主要特性
- **离线使用**：无需网络连接
- **词条管理**：添加、编辑、删除、查看词条
- **高级搜索**：多字段、模糊、正则搜索
- **导入导出**：Excel、PDF 格式支持
- **工具模块**：URL 书签、备忘录、IDS 编辑器
- **个性化设置**：主题切换、字体调整

### 系统要求
- **Android 版本**：5.0 (API 21) 或更高
- **存储空间**：100MB 可用空间
- **内存**：2GB RAM 推荐

## 🎉 完成

推送完成后，您将拥有：
- ✅ 完整的源代码仓库
- ✅ 自动构建的 Android APK
- ✅ 详细的文档和指南
- ✅ 可安装的手机应用

**享受您的 GHLan自定义字典 应用！** 📚✨


