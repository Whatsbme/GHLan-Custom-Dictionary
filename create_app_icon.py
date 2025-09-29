#!/usr/bin/env python3
"""
创建GHLan应用图标
生成Android应用所需的icon.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """创建GHLan应用图标"""
    # 创建512x512的画布
    size = 512
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 设置背景渐变
    for i in range(size):
        # 创建墨色渐变背景
        alpha = 255 - int(i * 0.3)
        color = (44, 44, 44, alpha)  # 墨黑色
        draw.line([(i, 0), (i, size)], fill=color)
    
    # 绘制"言"字样的GHL标志
    # 外圆
    circle_radius = 180
    center = (size // 2, size // 2)
    draw.ellipse(
        [center[0] - circle_radius, center[1] - circle_radius,
         center[0] + circle_radius, center[1] + circle_radius],
        fill=None,
        outline=(212, 105, 58),  # 朱砂色边框
        width=8
    )
    
    # 绘制"GHL"文字样式的"言"形
    # G - 左半部分，像"言"字的横
    draw.line([(center[0] - 80, center[1] - 20), (center[0] - 20, center[1] - 20)], 
              fill=(212, 105, 58), width=12)
    
    # H - 中间部分，像"言"字的竖
    draw.line([(center[0] - 15, center[1] - 50), (center[0] - 15, center[1] + 20)], 
              fill=(212, 105, 58), width=8)
    
    # L - 右半部分，像"言"字的点
    draw.circle([center[0] + 40, center[1] + 30], radius=15, fill=(212, 105, 58))
    
    # 添加一些水墨画风格的飞白效果
    for i in range(20):
        x = center[0] + (i - 10) * 15
        y = center[1] + (i % 3) * 30 - 40
        radius = 5 + (i % 3) * 3
        alpha = 80 - i * 2
        color = (106, 106, 106, alpha)  # 淡墨色
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    
    # 确保android目录存在
    os.makedirs('android', exist_ok=True)
    
    # 保存图标
    img.save('android/app_icon.png', 'PNG')
    print("✅ 应用图标已创建：android/app_icon.png")
    
    # 创建不同尺寸的图标（用于不同密度的屏幕）
    sizes = {
        'android/app_icon-hdpi.png': 72,
        'android/app_icon-mdpi.png': 48, 
        'android/app_icon-xhdpi.png': 96,
        'android/app_icon-xxhdpi.png': 144,
        'android/app_icon-xxxhdpi.png': 192
    }
    
    for filename, scale in sizes.items():
        resized = img.resize((scale, scale), Image.Resampling.LANCZOS)
        resized.save(filename, 'PNG')
    
    print("✅ 多尺寸图标已创建")
    
    return True

if __name__ == "__main__":
    try:
        create_app_icon()
        print("🎨 GHLan应用图标生成完成！")
    except Exception as e:
        print(f"❌ 图标生成失败: {e}")
        # 创建一个简单的纯色图标作为备选
        img = Image.new('RGB', (512, 512), (74, 144, 164))  # 水蓝色背景
        img.save('android/app_icon.png', 'PNG')
        print("📱 已创建简单备选图标")
