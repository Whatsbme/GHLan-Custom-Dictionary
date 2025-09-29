# GHLan APK构建详细指南

## 🎯 APK方案完整流程

APK是Android应用程序包，可以将你的Python应用打包成原生Android应用。这是最简单、性能最好的在手机上使用GHLan的方案。

---

## 📋 方案优势

### ✅ 优点：
- **原生性能** - 直接在Android系统上运行，性能最佳
- **用户友好** - 安装简单，像普通App一样使用
- **功能完整** - 支持所有Kivy/KivyMD功能
- **易于分发** - 可以分享给其他人安装
- **无需ROOT** - 不修改系统，安全可靠

### ⚠️ 要求：
- **Windows/macOS/Linux电脑**
- **稳定的网络连接**（下载Android SDK）
- **足够的磁盘空间**（至少8GB）
- **2-4小时时间**（首次构建）

---

## 🛠️ 第一步：构建环境准备

### Windows系统（推荐）

#### 方案A：自动安装（简单）
```bash
# 1. 安装Python依赖
pip install buildozer cython

# 2. 克隆你的项目
git clone https://github.com/Whatsbme/GHLan-Custom-Dictionary.git
cd GHLan-Custom-Dictionary

# 3. 运行我的自动构建脚本
python build_apk_simple.py
```

#### 方案B：手动安装（更可控）
```bash
# 1. 安装Java JDK（必需）
# 下载：https://adoptium.net/

# 2. 安装Android Studio（用于SDK）
# 下载：https://developer.android.com/studio

# 3. 设置环境变量
set ANDROID_HOME=C:\Users\你的用户名\AppData\Local\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools
set PATH=%PATH%;C:\Program Files\Java\jdk-11\bin

# 4. 安装Python工具
pip install buildozer cython numpy pillow kivy kivymd sqlalchemy reportlab
```

### Linux/macOS系统
```bash
# 安装系统依赖
# Ubuntu/Debian:
sudo apt update
sudo apt install openjdk-11-jdk python3-pip python3-venv

# macOS:
brew install openjdk@11

# 安装Python工具
pip3 install buildozer cython numpy pillow kivy kivymd sqlalchemy reportlab
```

---

## 🔧 第二步：Buildozer配置详解

Buildozer是Kivy官方推荐的Android构建工具。我为你创建了优化的配置文件：

### buildozer.spec 配置解析
```ini
[app]
# 应用基本信息
title = GHLan自定义词典              # 应用显示名称
package.name = ghlan_dict           # 包名（唯一标识）
package.domain = org.whatsbme.ghlan # 域名（按Android规范）

# 版本管理
version = 1.0.0                    # 应用版本号

# 源码配置
source.dir = .                     # 源码根目录
source.include_exts = py,png,jpg,jpeg,ogg,wav,mp3,json,kv,ini,txt
source.exclude_dirs = tests,bin,venv,__pycache__,.git
source.exclude_patterns = license,images/*.png

[android]
# Android API级别
api = 30                          # 目标Android版本
minapi = 21                       # 最低支持Android版本
ndk = 21.3.6528147               # Android NDK版本

# 权限配置
permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Python依赖
requirements = python3,kivy==2.3.1,kivymd==1.2.0,sqlalchemy,pillow,python-dateutil,certifi,charset-normalizer,greenlet,reportlab,xlwt,openpyxl,fuzzywuzzy,python-levenshtein

# 构建模式
build = debug                     # debug模式（比release快）
```

### 自定义配置建议
根据你的需求，可以调整：

```ini
# 应用信息
title = 你的自定义名称
package.name = 你的包名

# 版本信息
version = 1.0.0

# 特定功能需求
permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE

# 添加特定库（如果项目需要）
requirements = python3,kivy==2.3.1,kivymd==1.2.0,sqlalchemy,pillow,python-dateutil,certifi,charset-normalizer,greenlet,reportlab,xlwt,openpyxl,fuzzywuzzy,python-levenshtein,qrcode,requests
```

---

## 🚀 第三步：构建流程详解

### 首次构建（需要2-4小时）
```bash
# 1. 进入项目目录
cd GHLan-Custom-Dictionary

# 2. 初始化buildozer（如果没有配置）
buildozer init

# 3. 开始构建（耐心等待）
buildozer android debug

# 4. 构建成功后会显示：
# Build completed successfully!
# Binaries available in: /path/to/bin/
```

### 构建过程监控
构建过程中会显示：
```
[INFO]    Building package...
[INFO]    -> directory context /kivy/GHLan-Custom-Dictionary/.buildozer
[INFO]    -> Building python3 (found in cache)
[INFO]    -> Building kivy (found in cache)
[INFO]    -> Building sqlalchemy (found in cache)
[INFO]    -> Building apk...
[INFO]    -> APK successfully built: bin/your_app_name-debug.apk
```

### 增量构建（快速）
修改代码后，后续构建会快很多：
```bash
# 只重新编译Python代码
buildozer android debug --target python3,kivy

# 完全重新构建
buildozer android clean
buildozer android debug
```

---

## 📱 第四步：APK安装测试

### 传输APK到手机
1. **通过USB传输**：
   - Android 11+：USB线连接，选择"文件传输"模式
   - 直接拖拽APK文件到手机存储

2. **通过云盘传输**：
   - 上传APK到百度网盘/微信
   - 在手机上登录下载

3. **通过邮件传输**：
   - 发送APK作为邮件附件
   - 在手机邮箱中下载

### Android安装步骤
1. **启用未知来源安装**：
   ```
   设置 → 安全 → 未知来源应用安装 → 允许安装
   ```

2. **定位APK文件**：
   ```
   文件管理器 → Downloads → your_app_name-debug.apk
   ```

3. **安装应用**：
   ```
   点击APK文件 → 安装 → 等待完成
   ```

4. **启动应用**：
   ```
   桌面找到"GHLan自定义词典"图标 → 点击启动
   ```

---

## 🔍 第五步：测试和调试

### 功能测试清单
```
□ 应用启动正常
□ 搜索功能可用
□ 词条管理正常
□ 设置界面可打开
□ 导入导出功能可用
□ 工具界面响应
□ 主题切换正常
□ 字体设置生效
```

### 性能优化检查
```
□ 启动时间 < 5秒
□ 内存占用 < 200MB
□ 界面响应流畅
□ 无崩溃现象
□ 网络功能正常
```

### 调试信息收集
如果出现问题，收集以下信息：
```bash
# Android日志（需要ADB）
adb logcat | grep "ghlan"

# 或在应用中启用日志
# 查看Python错误
```

---

## 🛠️ 故障排除详细指南

### 问题1：构建环境失败
```
错误：No such file or directory: 'javac'
解决：
1. 安装Java JDK：https://adoptium.net/
2. 设置JAVA_HOME环境变量
3. 验证：javac -version
```

### 问题2：Android SDK下载失败
```
错误：SDK component not found
解决：
1. 手动下载Android SDK Tools
2. 设置ANDROID_HOME环境变量
3. 下载特定API级别：
   sdkmanager "platforms;android-30"
```

### 问题3：NDK版本不匹配
```
错误：NDK version not supported
解决：
1. 修改buildozer.spec中的ndk版本
2. 使用推荐的NDK版本：21.3.6528147
3. 或者完全删除ndk = 使用最新自动匹配
```

### 问题4：依赖包构建失败
```
错误：Failed to build pillow/numpy
解决：
1. 预处理步骤：
   pip install setuptools wheel

2. 单个安装：
   pip install pillow
   pip install numpy

3. 检查依赖：
   pip check
```

### 问题5：APK安装失败
```
错误：App not installed
解决：
1. 检查Android版本兼容性
2. 卸载同名应用
3. 增加存储空间
4. 重新签名APK：
   buildozer android release
```

### 问题6：应用启动崩溃
```
错误：App crashes on startup
解决：
1. 检查Python语法错误
2. 验证资源文件是否存在
3. 添加错误处理：
   try:
       # 应用初始化代码
   except Exception as e:
       # 错误日志记录
```

---

## 📊 构建性能优化

### 加速构建技巧
```bash
# 1. 使用SSD硬盘
# 2. 增加RAM（8GB+）
# 3. 使用增量构建：
buildozer android debug --target python3

# 4. 缓存管理：
buildozer android clean
# 或部分清理：
rm -rf .buildozer/android/platform/build-*/libs
```

### 网络优化
```bash
# 1. 使用国内镜像：
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 预下载Android组件：
sdkmanager --list
sdkmanager "platforms;android-30"
```

---

## 🎯 最佳实践建议

### 构建前检查
```bash
# 1. 确保项目可以正常运行：
python run.py

# 2. 运行测试：
python -m pytest tests/

# 3. 检查依赖：
pip check
```

### 版本管理策略
```bash
# 1. 使用Git标签管理版本：
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 2. 构建发布版：
buildozer android release
```

### 分发策略
```bash
# 1. APK签名：
buildozer android release

# 2. 多平台测试：
#    在不同Android版本测试
#    在不同设备尺寸测试
#    在不同厂商系统测试
```

---

## 📈 进阶技巧

### 自定义应用图标
```bash
# 1. 准备图标文件：
# android/app_icon.png (应该是正方形，建议512x512)

# 2. 在buildozer.spec中引用：
icon = android/app_icon.png

# 3. 为不同密度创建图标：
# android/app_icon-hdpi.png (72x72)
# android/app_icon-mdpi.png (48x48)
# android/app_icon-xhdpi.png (96x96)
# android/app_icon-xxhdpi.png (144x144)
```

### 添加应用权限配置
```ini
[android]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,VIBRATE,ACCESS_NETWORK_STATE
allow_backup = True
```

### 发布到应用市场
```bash
# 1. 构建release版本：
buildozer android release

# 2. 签名APK：
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

# 3. 对齐APK：
zipalign -v 4 bin/your_app_name-release-unsigned.apk bin/your_app_name-release-aligned.apk
```

---

## 📋 完整构建checklist

### 构建前
- [ ] Python 3.8+已安装
- [ ] Java JDK已安装并配置环境变量
- [ ] Android SDK已下载并配置
- [ ] 网络连接稳定
- [ ] 磁盘空间充足（8GB+）

### 构建中
- [ ] 监控构建进度
- [ ] 解决依赖冲突
- [ ] 优化构建速度

### 构建后
- [ ] APK文件成功生成
- [ ] 传输到测试设备
- [ ] 安装测试通过
- [ ] 功能测试完成
- [ ] 性能表现满意

---

这就是APK构建方案的完整详细信息！这个方案虽然首次构建需要时间，但最终会给你一个专业级的Android应用。
