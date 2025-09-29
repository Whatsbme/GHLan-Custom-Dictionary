"""
GHLan水墨风格Logo生成器
GHLan Ink Style Logo Generator
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path


class GHLanLogoGenerator:
    """GHLan Logo生成器"""
    
    def __init__(self):
        self.size = (200, 200)
        self.ink_colors = {
            'ink_black': '#2C2C2C',
            'water_blue': '#4A90A4',
            'cinnabar': '#D2691E',
            'paper_white': '#FEFEFE'
        }
    
    def generate_logo(self, output_path="assets/icons/ghlan_logo.png"):
        """生成GHLan Logo"""
        # 创建画布
        img = Image.new('RGBA', self.size, self.ink_colors['paper_white'])
        draw = ImageDraw.Draw(img)
        
        # 绘制"言"字形态的"GHL"标志
        self._draw_ghl_character(draw)
        
        # 保存图片
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, 'PNG')
        
        return output_path
    
    def _draw_ghl_character(self, draw):
        """绘制"言"字形态的"GHL"标志"""
        center_x, center_y = self.size[0] // 2, self.size[1] // 2
        
        # 绘制"言"字的基本结构
        # 上部横线
        draw.rectangle(
            [center_x - 60, center_y - 80, center_x + 60, center_y - 75],
            fill=self.ink_colors['ink_black']
        )
        
        # 中间横线
        draw.rectangle(
            [center_x - 50, center_y - 20, center_x + 50, center_y - 15],
            fill=self.ink_colors['ink_black']
        )
        
        # 下部横线
        draw.rectangle(
            [center_x - 50, center_y + 20, center_x + 50, center_y + 25],
            fill=self.ink_colors['ink_black']
        )
        
        # 左侧竖线
        draw.rectangle(
            [center_x - 60, center_y - 80, center_x - 55, center_y + 30],
            fill=self.ink_colors['ink_black']
        )
        
        # 右侧竖线
        draw.rectangle(
            [center_x + 55, center_y - 80, center_x + 60, center_y + 30],
            fill=self.ink_colors['ink_black']
        )
        
        # 添加"GHL"字母的水墨效果
        self._draw_ghl_letters(draw, center_x, center_y)
        
        # 添加装饰性水墨点
        self._draw_ink_dots(draw, center_x, center_y)
    
    def _draw_ghl_letters(self, draw, center_x, center_y):
        """绘制GHL字母"""
        # 使用简化的字母形状，融入"言"字结构
        
        # G字母 - 在左上角
        draw.ellipse(
            [center_x - 45, center_y - 70, center_x - 25, center_y - 50],
            outline=self.ink_colors['water_blue'],
            width=3
        )
        draw.rectangle(
            [center_x - 35, center_y - 60, center_x - 25, center_y - 50],
            fill=self.ink_colors['water_blue']
        )
        
        # H字母 - 在中间
        draw.rectangle(
            [center_x - 20, center_y - 40, center_x - 15, center_y + 10],
            fill=self.ink_colors['cinnabar']
        )
        draw.rectangle(
            [center_x + 5, center_y - 40, center_x + 10, center_y + 10],
            fill=self.ink_colors['cinnabar']
        )
        draw.rectangle(
            [center_x - 20, center_y - 15, center_x + 10, center_y - 10],
            fill=self.ink_colors['cinnabar']
        )
        
        # L字母 - 在右下角
        draw.rectangle(
            [center_x + 15, center_y - 40, center_x + 20, center_y + 10],
            fill=self.ink_colors['water_blue']
        )
        draw.rectangle(
            [center_x + 15, center_y + 5, center_x + 35, center_y + 10],
            fill=self.ink_colors['water_blue']
        )
    
    def _draw_ink_dots(self, draw, center_x, center_y):
        """绘制装饰性水墨点"""
        # 在"言"字周围添加水墨点，营造水墨画效果
        dots = [
            (center_x - 80, center_y - 60, 8),
            (center_x + 80, center_y - 40, 6),
            (center_x - 70, center_y + 40, 5),
            (center_x + 70, center_y + 20, 7),
            (center_x - 30, center_y - 100, 4),
            (center_x + 30, center_y + 50, 6),
        ]
        
        for x, y, size in dots:
            draw.ellipse(
                [x - size, y - size, x + size, y + size],
                fill=self.ink_colors['ink_black']
            )
    
    def generate_icon_variants(self):
        """生成不同尺寸的图标变体"""
        variants = [
            (16, 16, "ghlan_icon_16.png"),
            (32, 32, "ghlan_icon_32.png"),
            (48, 48, "ghlan_icon_48.png"),
            (64, 64, "ghlan_icon_64.png"),
            (128, 128, "ghlan_icon_128.png"),
            (256, 256, "ghlan_icon_256.png"),
        ]
        
        generated_files = []
        
        for width, height, filename in variants:
            # 创建指定尺寸的画布
            img = Image.new('RGBA', (width, height), self.ink_colors['paper_white'])
            draw = ImageDraw.Draw(img)
            
            # 缩放绘制
            scale = min(width, height) / 200
            self._draw_scaled_ghl_character(draw, width, height, scale)
            
            # 保存文件
            output_path = f"assets/icons/{filename}"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'PNG')
            generated_files.append(output_path)
        
        return generated_files
    
    def _draw_scaled_ghl_character(self, draw, width, height, scale):
        """绘制缩放后的GHL字符"""
        center_x, center_y = width // 2, height // 2
        
        # 缩放所有尺寸
        def scale_coord(coord):
            return int(coord * scale)
        
        # 绘制"言"字的基本结构
        # 上部横线
        draw.rectangle(
            [center_x - scale_coord(60), center_y - scale_coord(80),
             center_x + scale_coord(60), center_y - scale_coord(75)],
            fill=self.ink_colors['ink_black']
        )
        
        # 中间横线
        draw.rectangle(
            [center_x - scale_coord(50), center_y - scale_coord(20),
             center_x + scale_coord(50), center_y - scale_coord(15)],
            fill=self.ink_colors['ink_black']
        )
        
        # 下部横线
        draw.rectangle(
            [center_x - scale_coord(50), center_y + scale_coord(20),
             center_x + scale_coord(50), center_y + scale_coord(25)],
            fill=self.ink_colors['ink_black']
        )
        
        # 左侧竖线
        draw.rectangle(
            [center_x - scale_coord(60), center_y - scale_coord(80),
             center_x - scale_coord(55), center_y + scale_coord(30)],
            fill=self.ink_colors['ink_black']
        )
        
        # 右侧竖线
        draw.rectangle(
            [center_x + scale_coord(55), center_y - scale_coord(80),
             center_x + scale_coord(60), center_y + scale_coord(30)],
            fill=self.ink_colors['ink_black']
        )
        
        # 添加GHL字母（简化版）
        if scale > 0.5:  # 只在较大的图标中绘制字母
            # G字母
            draw.ellipse(
                [center_x - scale_coord(45), center_y - scale_coord(70),
                 center_x - scale_coord(25), center_y - scale_coord(50)],
                outline=self.ink_colors['water_blue'],
                width=max(1, int(3 * scale))
            )
            
            # H字母
            draw.rectangle(
                [center_x - scale_coord(20), center_y - scale_coord(15),
                 center_x + scale_coord(10), center_y - scale_coord(10)],
                fill=self.ink_colors['cinnabar']
            )
            
            # L字母
            draw.rectangle(
                [center_x + scale_coord(15), center_y + scale_coord(5),
                 center_x + scale_coord(35), center_y + scale_coord(10)],
                fill=self.ink_colors['water_blue']
            )


def generate_all_logos():
    """生成所有Logo文件"""
    generator = GHLanLogoGenerator()
    
    # 生成主Logo
    main_logo = generator.generate_logo()
    print(f"Generated main logo: {main_logo}")
    
    # 生成图标变体
    icon_variants = generator.generate_icon_variants()
    print(f"Generated {len(icon_variants)} icon variants")
    
    return main_logo, icon_variants


if __name__ == "__main__":
    generate_all_logos()







