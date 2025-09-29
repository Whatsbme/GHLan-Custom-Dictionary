@echo off
echo 🔧 GHLan Android环境自动安装脚本
echo ===========================================

:: 检查管理员权限
echo 📋 检查权限...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ 管理员权限确认
) else (
    echo ❌ 需要管理员权限！请右键选择"以管理员身份运行"
    pause
    exit
)

:: 创建Android SDK目录
echo 📁 创建Android SDK目录...
if not exist "C:\Android\Sdk" mkdir "C:\Android\Sdk"
set "ANDROID_HOME=C:\Android\Sdk"
echo ✅ Android SDK目录: %ANDROID_HOME%

:: 下载Android SDK命令行工具
echo 🌐 下载Android SDK命令行工具...
echo 请手动下载并解压 Android SDK命令行工具到 %ANDROID_HOME%\cmdline-tools\latest\
echo 下载地址: https://developer.android.com/studio#downloads
echo 选择: "Command line tools only"
echo.
echo 下载完成按任意键继续...
pause

:: 检查cmdline-tools是否存在
if not exist "%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" (
    echo ❌ cmdline-tools未正确安装！
    echo 请确保解压到: %ANDROID_HOME%\cmdline-tools\latest\
    pause
    exit
)

:: 设置环境变量
echo 🔧 设置环境变量...
setx ANDROID_HOME "%ANDROID_HOME%" >nul
setx PATH "%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools" >nul
echo ✅ 环境变量已设置

:: 添加Android SDK路径到当前会话
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools

:: 接受Android许可
echo 📋 接受Android SDK许可...
echo y | "%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" --licenses

:: 安装必要的SDK组件
echo 📦 安装Android SDK组件...
echo ⏳ 这可能需要10-30分钟，下载大约2GB...

echo 🔄 安装Platform Android API 30...
"%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" "platforms;android-30"

echo 🔄 安装Platform Tools...
"%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" "platform-tools"

echo 🔄 安装Build Tools...
"%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" "build-tools;30.0.3"

echo 🔄 安装Android NDK...
"%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager.bat" "ndk;21.3.6528147"

:: 检查安装结果
echo 🔍 验证安装...
if exist "%ANDROID_HOME%\platforms\android-30" (
    echo ✅ Android API 30 安装成功
) else (
    echo ❌ Android API 30 安装失败
)

if exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo ✅ Platform Tools 安装成功
) else (
    echo ❌ Platform Tools 安装失败
)

if exist "%ANDROID_HOME%\build-tools\30.0.3\aapt.exe" (
    echo ✅ Build Tools 安装成功
) else (
    echo ❌ Build Tools 安装失败
)

if exist "%ANDROID_HOME%\ndk\21.3.6528147\ndk-build.cmd" (
    echo ✅ Android NDK 安装成功
) else (
    echo ❌ Android NDK 安装失败
)

echo.
echo 🎉 Android SDK环境安装完成！
echo.
echo 📋 下一步操作：
echo 1. 重新打开命令行窗口（使环境变量生效）
echo 2. 在项目目录运行: python build_apk_simple.py
echo 3. 等待APK构建完成
echo.
echo ⚠️  注意：首次构建可能需要1-2小时，构建过程中请保持电脑联网
echo.
pause
