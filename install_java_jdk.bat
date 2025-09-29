@echo off
echo ☕ 自动安装Java JDK脚本
echo ========================================

:: 检查是否已经有Java
echo 📋 检查当前Java状态...
java -version 2>nul
if %errorlevel% == 0 (
    echo ✅ Java运行环境已安装
    java -version
) else (
    echo ❌ Java运行环境未安装
)

where javac 2>nul
if %errorlevel% == 0 (
    echo ✅ Java开发工具包已安装
    javac -version
) else (
    echo ❌ Java开发工具包未安装
)

echo.
echo 🔧 需要安装Java JDK...
echo.
echo 请按以下步骤手动安装：
echo.
echo 1. 访问: https://adoptium.net/temurin/releases/
echo 2. 选择: JDK 11 或 JDK 17 (推荐)
echo 3. 选择: Windows x64
echo 4. 下载文件: OpenJDK11U-jdk_x64_windows_hotspot_*.zip
echo 5. 解压到: C:\Program Files\Java\
echo.

echo 📁 建议解压路径：
echo C:\Program Files\Java\jdk-11.0.20.101-hotspot\
echo.

echo 🔧 安装完成后，需要设置环境变量：
echo.
echo 1. 按 Windows + R
echo 2. 输入 sysdm.cpl
echo 3. 点击 "环境变量"
echo 4. 在 "系统变量" 中添加：
echo    JAVA_HOME = C:\Program Files\Java\jdk-11.0.20.101-hotspot
echo.
echo 5. 修改 PATH 变量，添加：
echo    %JAVA_HOME%\bin
echo.

echo ⚠️  注意：
echo - JDK版本可以是11、17或21
echo - 路径要根据实际解压位置调整
echo - 设置完成后需要重启命令行

echo.
echo 🎯 安装完成检查命令：
echo java -version
echo javac -version
echo echo %%JAVA_HOME%%

pause
