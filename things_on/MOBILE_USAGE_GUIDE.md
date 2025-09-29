# 📱 手机使用 GHLan自定义字典 完整指南

## 🎯 快速开始（3步完成）

### 第1步：获取 APK 文件
**推荐方式 - GitHub Actions 自动构建**：
1. 将项目推送到 GitHub
2. 在 Actions 页面触发构建
3. 下载生成的 APK 文件

### 第2步：安装到手机
1. 将 APK 文件传输到手机
2. 开启"未知来源"安装权限
3. 点击 APK 文件安装

### 第3步：开始使用
1. 打开应用
2. 添加词条
3. 享受离线字典体验

---

## 🚀 详细操作步骤

### 方案一：GitHub Actions 构建（最简单）

#### 1. 准备 GitHub 仓库
```bash
# 在项目目录执行
git init
git add .
git commit -m "GHLan自定义字典 v1.0.0"

# 在 GitHub 创建新仓库后
git remote add origin https://github.com/Whatsbme/GHLan-Custom-Dictionary.git
git push -u origin main
```

#### 2. 触发自动构建
1. 登录 GitHub，进入仓库
2. 点击 **Actions** 标签
3. 选择 **Build Android APK**
4. 点击 **Run workflow** → **Run workflow**
5. 等待构建完成（约 10-15 分钟）

#### 3. 下载 APK
1. 构建完成后，点击构建记录
2. 在 **Artifacts** 部分下载 `ghlan-dictionary-apk`
3. 解压 zip 文件，获得 APK

#### 4. 安装到手机
1. 将 APK 传输到手机（USB/邮件/云盘）
2. 手机设置 → 安全 → 允许未知来源
3. 点击 APK 文件安装
4. 安装完成，开始使用

### 方案二：WSL2 本地构建

#### 1. 安装 WSL2
```bash
# PowerShell 管理员模式
wsl --install
# 重启电脑完成安装
```

#### 2. 构建 APK
```bash
# 进入 WSL2
wsl

# 安装依赖
sudo apt update
sudo apt install python3 python3-pip git
pip3 install buildozer

# 构建 APK
cd /mnt/d/Program\ Files/GHLan
buildozer android debug
```

#### 3. 获取 APK
- APK 文件位置：`bin/ghlandictionary-1.0.0-debug.apk`
- 复制到手机安装

---

## 📱 手机安装详细说明

### Android 权限设置

#### 允许未知来源安装
**方法一**：
1. 设置 → 安全 → 未知来源
2. 开启允许安装

**方法二**：
1. 设置 → 应用管理 → 特殊权限
2. 安装未知应用 → 选择文件管理器
3. 允许安装

#### 应用权限
安装后首次运行会请求：
- **存储权限**：保存词条数据
- **网络权限**：URL 书签功能（可选）

### 系统要求
- **Android 版本**：5.0 (API 21) 或更高
- **存储空间**：100MB 可用空间
- **内存**：2GB RAM 推荐
- **屏幕**：支持触摸操作

---

## 🎮 应用使用指南

### 主要功能
1. **词条管理**
   - 添加新词条
   - 编辑现有词条
   - 删除词条
   - 查看词条详情

2. **高级搜索**
   - 多字段搜索
   - 模糊匹配
   - 正则表达式搜索

3. **导入导出**
   - Excel 格式导入
   - PDF/Excel 导出
   - 批量操作

4. **工具模块**
   - URL 书签管理
   - 备忘录功能
   - IDS 符号编辑器

5. **个性化设置**
   - 主题切换
   - 字体调整
   - 界面定制

### 操作技巧
- **快速搜索**：主界面搜索框
- **添加词条**：点击"添加词条"按钮
- **查看详情**：点击词条列表中的项目
- **编辑词条**：在详情页面点击编辑按钮

---

## 🔧 常见问题解决

### 构建问题
**Q: GitHub Actions 构建失败**
A: 
- 检查 `buildozer.spec` 配置
- 查看构建日志错误信息
- 确保依赖版本正确

**Q: WSL2 构建失败**
A:
- 确保 WSL2 正确安装
- 检查网络连接
- 尝试更新系统包

### 安装问题
**Q: 无法安装 APK**
A:
- 检查 Android 版本兼容性
- 确认未知来源权限已开启
- 尝试重新下载 APK

**Q: 安装后无法运行**
A:
- 检查设备性能是否满足要求
- 确认存储权限已授予
- 重启应用或设备

### 使用问题
**Q: 应用运行缓慢**
A:
- 关闭其他应用释放内存
- 检查设备存储空间
- 重启应用

**Q: 数据丢失**
A:
- 检查存储权限
- 确认设备存储空间充足
- 定期备份数据

---

## 📞 技术支持

### 获取帮助
- 查看 `docs/USER_MANUAL.md` 用户手册
- 阅读 `docs/DEVELOPER_GUIDE.md` 开发者指南
- 检查项目文档和说明

### 反馈问题
- 记录错误信息
- 描述操作步骤
- 提供设备信息

---

## 🎉 开始使用

现在您已经了解了完整的安装和使用流程：

1. **选择构建方案**（推荐 GitHub Actions）
2. **获取 APK 文件**
3. **安装到手机**
4. **开始使用 GHLan自定义字典**

享受您的离线字典应用体验！📚✨
