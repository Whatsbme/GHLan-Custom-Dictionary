#!/bin/bash
# GHLan Termux安装脚本
# 用于在安卓手机上的Termux环境中安装和运行GHLan

set -e

echo "🎯 GHLan Termux 安装脚本"
echo "=========================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Termux是否安装
check_termux() {
    print_status "检查Termux环境..."
    
    if ! command -v pkg &> /dev/null; then
        print_error "Termux未找到，请先安装Termux应用"
        echo "下载地址: https://f-droid.org/en/packages/com.termux/"
        exit 1
    fi
    
    print_success "Termux环境检查通过"
}

# 更新包管理器
update_packages() {
    print_status "更新包管理器..."
    pkg update -y
    pkg upgrade -y
    print_success "包管理器更新完成"
}

# 安装Python和相关依赖
install_python_deps() {
    print_status "安装Python和相关依赖..."
    
    # 安装基础Python包
    pkg install -y python python-pip
    
    # 安装编译工具
    pkg install -y libffi libjpeg-turbo
    pkg install -y python-dev
    
    # 安装Git
    pkg install -y git
    
    print_success "Python环境安装完成"
}

# 安装GUI支持
install_gui_support() {
    print_status "配置GUI支持..."
    
    # 提示用户安装Termux:X11
    print_warning "为了运行GUI应用，你需要安装Termux:X11"
    echo "下载地址: https://x11vnc.sourceforge.net/termux/"
    echo ""
    echo "或者使用以下命令通过F-Droid安装:"
    echo "1. 下载F-Droid"
    echo "2. 在F-Droid中搜索 'Termux:X11'"
    echo "3. 安装Termux:X11插件"
    echo ""
    
    read -p "是否已安装Termux:X11? (y/n): " gui_installed
    
    if [ "$gui_installed" != "y" ]; then
        print_warning "请先安装Termux:X11后再继续"
        exit 1
    fi
}

# 克隆项目
clone_project() {
    print_status "克隆GHLan项目..."
    
    # 检查是否已存在
    if [ -d "GHLan-Custom-Dictionary" ]; then
        print_warning "项目目录已存在，是否更新? (y/n): "
        read -r update_project
        if [ "$update_project" = "y" ]; then
            rm -rf GHLan-Custom-Dictionary
        else
            cd GHLan-Custom-Dictionary
            print_success "使用现有项目目录"
            return
        fi
    fi
    
    # 克隆项目
    git clone https://github.com/Whatsbme/GHLan-Custom-Dictionary.git
    
    cd GHLan-Custom-Dictionary
    print_success "项目克隆完成"
}

# 安装Python依赖
install_python_requirements() {
    print_status "安装Python项目依赖..."
    
    # 升级pip
    python -m pip install --upgrade pip
    
    # 安装requirements.txt中的依赖
    if [ -f "requirements.txt" ]; then
        python -m pip install -r requirements.txt
    else
        print_warning "requirements.txt不存在，手动安装核心依赖..."
        python -m pip install kivy==2.3.1 kivymd==1.2.0 sqlalchemy pillow reportlab xlwt openpyxl fuzzywuzzy python-levenshtein
    fi
    
    print_success "Python依赖安装完成"
}

# 配置Kivy用于触摸屏
configure_kivy() {
    print_status "配置Kivy触摸屏支持..."
    
    # 创建Kivy配置目录
    mkdir -p ~/.kivy/config.d
    
    # 创建触摸屏配置
    cat > ~/.kivy/config.d/touch_config.ini << EOF
[graphics]
show_cursor = 0
borderless = 0
window_state = normal

[input]
mouse = mouse
touch = mtdev
mtdev_%(name)s = probesysfs,provider=mtdev

[widgets]
single_tap_distance = 40
double_tap_distance = 40
double_tap_time = 250

[application]
window_state = normal
EOF

    print_success "Kivy触摸屏配置完成"
}

# 创建启动脚本
create_launch_script() {
    print_status "创建启动脚本..."
    
    cat > ~/run_ghlan.sh << 'EOF'
#!/bin/bash
# GHLan启动脚本

echo "🚀 启动GHLan自定义词典..."

# 设置环境变量
export DISPLAY=:0.0
export ANDROID_ROOT=/system
export ANDROID_DATA=/data

# 进入项目目录
cd ~/GHLan-Custom-Dictionary

# 启动应用
echo "📱 启动GUI应用..."
python run.py
EOF

    chmod +x ~/run_ghlan.sh
    print_success "启动脚本创建完成"
}

# 显示使用说明
show_usage() {
    print_success "🎉 GHLan安装完成!"
    echo ""
    echo "📱 使用说明:"
    echo "1. 启动Termux"
    echo "2. 运行: ./run_ghlan.sh"
    echo "  或者: cd ~/GHLan-Custom-Dictionary && python run.py"
    echo ""
    echo "📋 注意事项:"
    echo "- 首次启动可能需要几秒钟编译"
    echo "- 如果GUI不显示，确保Termux:X11正在运行"
    echo "- 可以通过Termux:X11查看图形界面"
    echo ""
    echo "🔧 故障排除:"
    echo "- 如果启动失败，检查: pip list | grep kivy"
    echo "- 重新安装Kivy: pip uninstall kivy && pip install kivy==2.3.1"
    echo "- 查看错误信息: python run.py 2>&1"
}

# 主安装流程
main() {
    check_termux
    update_packages
    install_python_deps
    install_gui_support
    clone_project
    install_python_requirements
    configure_kivy
    create_launch_script
    show_usage
}

# 捕获中断信号
trap 'print_error "安装被中断"; exit 1' INT TERM

# 运行主函数
main
