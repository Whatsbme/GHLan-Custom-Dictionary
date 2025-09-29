"""
备忘服务
Memo Service
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from models.memo_word import MemoWord
from services.database_service import db_service


class MemoService:
    """备忘服务类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_memo_word(self, memo_data: Dict[str, Any]) -> Optional[MemoWord]:
        """添加备忘词条"""
        try:
            memo_word = MemoWord(
                content=memo_data['content'],
                priority=memo_data.get('priority', 3),
                is_completed=False,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_service.add_object(memo_word)
            self.logger.info(f"添加备忘成功: {memo_word.content[:20]}...")
            return memo_word
            
        except Exception as e:
            self.logger.error(f"添加备忘失败: {e}")
            return None
    
    def get_all_memo_words(self) -> List[MemoWord]:
        """获取所有备忘词条"""
        try:
            return db_service.get_all_objects(MemoWord)
        except Exception as e:
            self.logger.error(f"获取备忘列表失败: {e}")
            return []
    
    def get_memo_word_by_id(self, memo_id: int) -> Optional[MemoWord]:
        """根据ID获取备忘词条"""
        try:
            return db_service.get_object_by_id(MemoWord, memo_id)
        except Exception as e:
            self.logger.error(f"获取备忘失败: {e}")
            return None
    
    def get_pending_memo_words(self) -> List[MemoWord]:
        """获取待处理的备忘词条"""
        try:
            return db_service.get_objects_by_filter(MemoWord, {'is_completed': False})
        except Exception as e:
            self.logger.error(f"获取待处理备忘失败: {e}")
            return []
    
    def get_completed_memo_words(self) -> List[MemoWord]:
        """获取已完成的备忘词条"""
        try:
            return db_service.get_objects_by_filter(MemoWord, {'is_completed': True})
        except Exception as e:
            self.logger.error(f"获取已完成备忘失败: {e}")
            return []
    
    def search_memo_words(self, query: str) -> List[MemoWord]:
        """搜索备忘词条"""
        try:
            all_memos = self.get_all_memo_words()
            query_lower = query.lower()
            
            results = []
            for memo in all_memos:
                if query_lower in memo.content.lower():
                    results.append(memo)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索备忘失败: {e}")
            return []
    
    def update_memo_word(self, memo_word: MemoWord) -> bool:
        """更新备忘词条"""
        try:
            memo_word.updated_at = datetime.now()
            db_service.update_object(memo_word)
            self.logger.info(f"更新备忘成功: {memo_word.content[:20]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"更新备忘失败: {e}")
            return False
    
    def complete_memo_word(self, memo_id: int) -> bool:
        """完成备忘词条"""
        try:
            memo_word = self.get_memo_word_by_id(memo_id)
            if memo_word:
                memo_word.is_completed = True
                memo_word.completed_at = datetime.now()
                memo_word.updated_at = datetime.now()
                db_service.update_object(memo_word)
                self.logger.info(f"完成备忘成功: {memo_word.content[:20]}...")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"完成备忘失败: {e}")
            return False
    
    def delete_memo_word(self, memo_id: int) -> bool:
        """删除备忘词条"""
        try:
            memo_word = self.get_memo_word_by_id(memo_id)
            if memo_word:
                db_service.delete_object(memo_word)
                self.logger.info(f"删除备忘成功: {memo_word.content[:20]}...")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"删除备忘失败: {e}")
            return False
    
    def get_memo_stats(self) -> Dict[str, Any]:
        """获取备忘统计信息"""
        try:
            all_memos = self.get_all_memo_words()
            pending_memos = self.get_pending_memo_words()
            completed_memos = self.get_completed_memo_words()
            
            # 按优先级统计
            priority_stats = {}
            for priority in range(1, 6):
                count = len([m for m in all_memos if m.priority == priority])
                priority_stats[f'priority_{priority}'] = count
            
            # 最近添加的备忘
            recent_memos = [m for m in all_memos if 
                          (datetime.now() - m.created_at).days <= 7]
            
            stats = {
                'total_count': len(all_memos),
                'pending_count': len(pending_memos),
                'completed_count': len(completed_memos),
                'recent_count': len(recent_memos),
                'priority_stats': priority_stats
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"获取备忘统计失败: {e}")
            return {}
    
    def cleanup_old_memos(self, days: int = 30) -> int:
        """清理旧的已完成备忘"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            old_memos = db_service.get_objects_by_filter(
                MemoWord, 
                {'is_completed': True, 'completed_at__lt': cutoff_date}
            )
            
            count = 0
            for memo in old_memos:
                if self.delete_memo_word(memo.id):
                    count += 1
            
            self.logger.info(f"清理了 {count} 个旧备忘")
            return count
            
        except Exception as e:
            self.logger.error(f"清理旧备忘失败: {e}")
            return 0


# 全局备忘服务实例
memo_service = MemoService()

