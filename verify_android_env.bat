@echo off
echo 🔍 Android环境验证脚本
echo ==========================================

echo 📋 验证Java JDK...
java -version 2>nul
if %errorlevel% == 0 (
    echo ✅ Java环境 OK
) else (
    echo ❌ Java环境未安装
)

javac -version 2>nul
if %errorlevel% == 0 (
    echo ✅ Java JDK OK
) else (
    echo ❌ Java JDK未安装 - 请先安装JDK
    goto :end
)

echo.
echo 📱 验证Android SDK...
set "SDK_HOME=%LOCALAPPDATA%\Android\Sdk"
if exist "%SDK_HOME%" (
    echo ✅ Android SDK目录存在: %SDK_HOME%
) else (
    echo ❌ Android SDK目录不存在
    echo 💡 请安装Android Studio并完成SDK配置
    goto :end
)

echo.
echo 📦 检查关键组件...
if exist "%SDK_HOME%\platforms\android-30" (
    echo ✅ Android API 30 - OK
) else (
    echo ❌ Android API 30 未安装
)

if exist "%SDK_HOME%\build-tools\30.0.3" (
    echo ✅ Build Tools 30.0.3 - OK
) else (
    echo ❌ Build Tools 30.0.3 未安装
)

if exist "%SDK_HOME%\platform-tools\adb.exe" (
    echo ✅ Platform Tools - OK
) else (
    echo ❌ Platform Tools 未安装
)

echo.
echo 🔧 设置环境变量...
set ANDROID_HOME=%SDK_HOME%
set JAVA_HOME=%JAVA_HOME%
echo ANDROID_HOME = %ANDROID_HOME%
echo JAVA_HOME = %JAVA_HOME%

echo.
echo 🎯 验证完成！如果看到 ✅ 全部OK，可以继续构建APK
echo 📝 如有❌，请先完成相应的安装

:end
echo.
pause
