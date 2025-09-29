"""
安装配置文件
Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 读取requirements文件
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="offline-dictionary",
    version="1.0.0",
    author="whatsbme",
    description="一个功能完整的移动端Python离线词典应用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Whatsbme/GHLan-Custom-Dictionary",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-kivy>=0.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "build": [
            "buildozer>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "offline-dictionary=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.kv", "*.png", "*.jpg", "*.ico", "*.ttf"],
    },
    keywords="dictionary, offline, mobile, kivy, sqlite, education",
    project_urls={
        "Bug Reports": "https://github.com/Whatsbme/GHLan-Custom-Dictionary/issues",
        "Source": "https://github.com/Whatsbme/GHLan-Custom-Dictionary",
        "Documentation": "https://github.com/Whatsbme/GHLan-Custom-Dictionary/wiki",
    },
)
