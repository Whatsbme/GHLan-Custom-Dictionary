"""
IDS符号服务
IDS Symbol Service
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import os
from pathlib import Path

from models.ids_symbol import IdsSymbol
from services.database_service import db_service
from app.config import config


class IdsService:
    """IDS符号服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.symbols_dir = Path(config.data_dir) / "ids_symbols"
        self.symbols_dir.mkdir(parents=True, exist_ok=True)
    
    def save_symbol(self, symbol_data: Dict[str, Any]) -> Optional[IdsSymbol]:
        """保存IDS符号"""
        try:
            symbol = IdsSymbol(
                name=symbol_data['name'],
                description=symbol_data.get('description', ''),
                symbols_data=json.dumps(symbol_data['symbols']),
                canvas_size=json.dumps(symbol_data['canvas_size']),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_service.add_object(symbol)
            self.logger.info(f"保存IDS符号成功: {symbol.name}")
            return symbol
            
        except Exception as e:
            self.logger.error(f"保存IDS符号失败: {e}")
            return None
    
    def get_all_symbols(self) -> List[IdsSymbol]:
        """获取所有IDS符号"""
        try:
            return db_service.get_all_objects(IdsSymbol)
        except Exception as e:
            self.logger.error(f"获取IDS符号列表失败: {e}")
            return []
    
    def get_symbol_by_id(self, symbol_id: int) -> Optional[IdsSymbol]:
        """根据ID获取IDS符号"""
        try:
            return db_service.get_object_by_id(IdsSymbol, symbol_id)
        except Exception as e:
            self.logger.error(f"获取IDS符号失败: {e}")
            return None
    
    def search_symbols(self, query: str) -> List[IdsSymbol]:
        """搜索IDS符号"""
        try:
            all_symbols = self.get_all_symbols()
            query_lower = query.lower()
            
            results = []
            for symbol in all_symbols:
                if (query_lower in symbol.name.lower() or 
                    query_lower in (symbol.description or "").lower()):
                    results.append(symbol)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索IDS符号失败: {e}")
            return []
    
    def update_symbol(self, symbol: IdsSymbol) -> bool:
        """更新IDS符号"""
        try:
            symbol.updated_at = datetime.now()
            db_service.update_object(symbol)
            self.logger.info(f"更新IDS符号成功: {symbol.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新IDS符号失败: {e}")
            return False
    
    def delete_symbol(self, symbol_id: int) -> bool:
        """删除IDS符号"""
        try:
            symbol = self.get_symbol_by_id(symbol_id)
            if symbol:
                db_service.delete_object(symbol)
                self.logger.info(f"删除IDS符号成功: {symbol.name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"删除IDS符号失败: {e}")
            return False
    
    def export_symbol_to_image(self, symbol: IdsSymbol, filepath: str) -> bool:
        """导出符号为图片"""
        try:
            from PIL import Image, ImageDraw
            
            # 解析画布大小
            canvas_size = json.loads(symbol.canvas_size)
            symbols_data = json.loads(symbol.symbols_data)
            
            # 创建PIL图像
            img = Image.new('RGB', canvas_size, 'white')
            draw = ImageDraw.Draw(img)
            
            # 绘制符号
            for symbol_data in symbols_data:
                if symbol_data['type'] == 'rectangle':
                    pos = symbol_data['pos']
                    size = symbol_data['size']
                    draw.rectangle([pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]], outline='black')
                elif symbol_data['type'] == 'circle':
                    pos = symbol_data['pos']
                    size = symbol_data['size']
                    draw.ellipse([pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]], outline='black')
                elif symbol_data['type'] == 'line':
                    points = symbol_data['points']
                    if len(points) >= 4:
                        for i in range(0, len(points) - 2, 2):
                            draw.line([points[i], points[i+1], points[i+2], points[i+3]], fill='black', width=2)
            
            # 保存图片
            img.save(filepath)
            self.logger.info(f"导出IDS符号图片成功: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出IDS符号图片失败: {e}")
            return False
    
    def get_symbol_templates(self) -> List[Dict[str, Any]]:
        """获取符号模板"""
        templates = [
            {
                'name': '基本结构',
                'description': '基本的矩形结构',
                'symbols': [
                    {'type': 'rectangle', 'pos': [50, 50], 'size': [100, 100]},
                    {'type': 'rectangle', 'pos': [200, 50], 'size': [100, 100]}
                ],
                'canvas_size': [400, 300]
            },
            {
                'name': '复合结构',
                'description': '复合的矩形结构',
                'symbols': [
                    {'type': 'rectangle', 'pos': [50, 50], 'size': [80, 80]},
                    {'type': 'rectangle', 'pos': [150, 50], 'size': [80, 80]},
                    {'type': 'rectangle', 'pos': [250, 50], 'size': [80, 80]},
                    {'type': 'rectangle', 'pos': [100, 150], 'size': [80, 80]}
                ],
                'canvas_size': [400, 300]
            },
            {
                'name': '圆形结构',
                'description': '圆形和矩形的组合',
                'symbols': [
                    {'type': 'circle', 'pos': [100, 100], 'size': [100, 100]},
                    {'type': 'rectangle', 'pos': [50, 200], 'size': [200, 50]}
                ],
                'canvas_size': [400, 300]
            }
        ]
        
        return templates
    
    def load_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """加载模板"""
        templates = self.get_symbol_templates()
        for template in templates:
            if template['name'] == template_name:
                return template
        return None
    
    def get_symbol_stats(self) -> Dict[str, Any]:
        """获取符号统计信息"""
        try:
            symbols = self.get_all_symbols()
            
            stats = {
                'total_count': len(symbols),
                'recent_count': len([s for s in symbols if 
                                   (datetime.now() - s.created_at).days <= 7])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"获取符号统计失败: {e}")
            return {}


# 全局IDS服务实例
ids_service = IdsService()

