#!/usr/bin/env python3
"""
GHLan APK构建脚本
简化版APK构建工具
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """检查构建依赖"""
    print("🔍 检查构建环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8+")
        return False
    
    # 检查必要的包
    required_packages = ['buildozer', 'kivy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少依赖包:", missing_packages)
        print("运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_buildozer_spec():
    """创建buildozer.spec配置"""
    print("📝 创建构建配置...")
    
    spec_content = """[app]

# 应用信息
title = GHLan自定义词典
package.name = ghlan_dict
package.domain = org.whatqbme.ghlan

# 版本信息
version = 1.0.0

# 源码配置
source.dir = .
source.include_exts = py,png,jpg,jpeg,ogg,wav,mp3,json,kv,ini,txt
source.exclude_dirs = tests,bin,venv,__pycache__,.git
source.exclude_patterns = license,images/*.png

# 路径配置
[buildozer]
# 如果自动安装失败，手动注释这些行
# android.sdk_path = /path/to/android/sdk
# android.ndk_path = /path/to/android/ndk

# Gradle配置
[android]
# Android基本信息
api = 30
minapi = 21
ndk = 21.3.6528147

# 权限
permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 依赖包
requirements = python3,kivy==2.3.1,kivymd==1.2.0,sqlalchemy,pillow,python-dateutil,certifi,charset-normalizer,greenlet,reportlab,xlwt,openpyxl,fuzzywuzzy,python-levenshtein

# Kotlin支持
gradle_dependencies = implementation 'org.jetbrains.kotlin:kotlin-stdlib:1.5.32'

# 构建配置
build = debug
"""
    
    with open('buildozer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ buildozer.spec 已创建")

def build_apk():
    """执行APK构建"""
    print("🔨 开始构建APK...")
    print("⚠️  首次构建可能需要1-2小时，请耐心等待...")
    
    try:
        # 运行buildozer
        result = subprocess.run([
            'buildozer', 'android', 'debug'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("🎉 APK构建成功!")
            
            # 查找生成的APK文件
            bin_dir = Path('bin')
            if bin_dir.exists():
                apk_files = list(bin_dir.glob('*.apk'))
                if apk_files:
                    print(f"📱 APK文件位置: {apk_files[0].absolute()}")
                    print("📤 将此文件传输到手机安装")
                    return True
            
        else:
            print("❌ APK构建失败")
            print("错误输出:")
            print(result.stderr)
            
            # 提供解决建议
            print("\n💡 可能的解决方案:")
            print("1. 检查Android SDK和NDK是否正确安装")
            print("2. 尝试手动设置android.sdk_path和android.ndk_path")
            print("3. 检查Python依赖是否完整安装")
            
            return False
            
    except Exception as e:
        print(f"❌ 构建过程出错: {e}")
        return False

def install_android_tools():
    """安装Android构建工具"""
    print("📱 安装Android构建工具...")
    
    commands = [
        "pip install buildozer",
        "pip install cython",
        "buildozer android debug"
    ]
    
    print("推荐的安装命令:")
    for cmd in commands:
        print(f"  {cmd}")

def main():
    """主函数"""
    print("🎯 GHLan APK构建工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败")
        install_android_tools()
        return
    
    # 创建构建配置
    create_buildozer_spec()
    
    # 构建APK
    if build_apk():
        print("\n🎉 恭喜！APK构建成功！")
        print("📱 请将生成的APK文件传输到手机安装")
    else:
        print("\n❌ APK构建失败")
        print("💡 建议手动配置Android SDK环境")

if __name__ == "__main__":
    main()
