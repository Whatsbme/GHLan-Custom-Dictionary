"""
书签服务
Bookmark Service
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from models.bookmark import Bookmark
from services.database_service import db_service


class BookmarkService:
    """书签服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_bookmark(self, bookmark_data: Dict[str, Any]) -> Optional[Bookmark]:
        """添加书签"""
        try:
            bookmark = Bookmark(
                title=bookmark_data['title'],
                url=bookmark_data['url'],
                category=bookmark_data.get('category', '未分类'),
                description=bookmark_data.get('description', ''),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_service.add_object(bookmark)
            self.logger.info(f"添加书签成功: {bookmark.title}")
            return bookmark
            
        except Exception as e:
            self.logger.error(f"添加书签失败: {e}")
            return None
    
    def get_all_bookmarks(self) -> List[Bookmark]:
        """获取所有书签"""
        try:
            return db_service.get_all_objects(Bookmark)
        except Exception as e:
            self.logger.error(f"获取书签列表失败: {e}")
            return []
    
    def get_bookmark_by_id(self, bookmark_id: int) -> Optional[Bookmark]:
        """根据ID获取书签"""
        try:
            return db_service.get_object_by_id(Bookmark, bookmark_id)
        except Exception as e:
            self.logger.error(f"获取书签失败: {e}")
            return None
    
    def get_bookmarks_by_category(self, category: str) -> List[Bookmark]:
        """根据分类获取书签"""
        try:
            return db_service.get_objects_by_filter(Bookmark, {'category': category})
        except Exception as e:
            self.logger.error(f"根据分类获取书签失败: {e}")
            return []
    
    def search_bookmarks(self, query: str) -> List[Bookmark]:
        """搜索书签"""
        try:
            # 简单的文本搜索
            all_bookmarks = self.get_all_bookmarks()
            query_lower = query.lower()
            
            results = []
            for bookmark in all_bookmarks:
                if (query_lower in bookmark.title.lower() or 
                    query_lower in bookmark.url.lower() or 
                    query_lower in (bookmark.description or "").lower()):
                    results.append(bookmark)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索书签失败: {e}")
            return []
    
    def update_bookmark(self, bookmark: Bookmark) -> bool:
        """更新书签"""
        try:
            bookmark.updated_at = datetime.now()
            db_service.update_object(bookmark)
            self.logger.info(f"更新书签成功: {bookmark.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新书签失败: {e}")
            return False
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """删除书签"""
        try:
            bookmark = self.get_bookmark_by_id(bookmark_id)
            if bookmark:
                db_service.delete_object(bookmark)
                self.logger.info(f"删除书签成功: {bookmark.title}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"删除书签失败: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        try:
            bookmarks = self.get_all_bookmarks()
            categories = list(set([b.category for b in bookmarks if b.category]))
            return sorted(categories)
        except Exception as e:
            self.logger.error(f"获取分类失败: {e}")
            return []
    
    def get_bookmark_stats(self) -> Dict[str, Any]:
        """获取书签统计信息"""
        try:
            bookmarks = self.get_all_bookmarks()
            categories = self.get_categories()
            
            stats = {
                'total_count': len(bookmarks),
                'category_count': len(categories),
                'categories': categories,
                'recent_count': len([b for b in bookmarks if 
                                   (datetime.now() - b.created_at).days <= 7])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"获取书签统计失败: {e}")
            return {}


# 全局书签服务实例
bookmark_service = BookmarkService()

