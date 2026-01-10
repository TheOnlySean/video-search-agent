"""
缓存管理模块 - 减少重复查询和API调用
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import os

logger = logging.getLogger(__name__)


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_file: str = 'cache.db', expiry_hours: int = 2):
        """
        初始化缓存管理器
        
        Args:
            cache_file: 缓存数据库文件路径
            expiry_hours: 缓存过期时间（小时）
        """
        self.cache_file = cache_file
        self.expiry_hours = expiry_hours
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.cache_file) if os.path.dirname(self.cache_file) else '.', exist_ok=True)
        
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        # 创建缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_cache (
                query_key TEXT PRIMARY KEY,
                topic TEXT,
                results TEXT,
                created_at TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"✅ 缓存数据库初始化完成: {self.cache_file}")
    
    def get(self, topic: str) -> Optional[List[Dict]]:
        """
        从缓存获取结果
        
        Args:
            topic: 搜索主题
            
        Returns:
            缓存的视频列表，如果不存在或已过期则返回 None
        """
        query_key = self._make_key(topic)
        
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT results, expires_at FROM video_cache WHERE query_key = ?',
            (query_key,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            logger.info(f"缓存未命中: {topic}")
            return None
        
        results_json, expires_at = row
        expires_at = datetime.fromisoformat(expires_at)
        
        # 检查是否过期
        if datetime.now() > expires_at:
            logger.info(f"缓存已过期: {topic}")
            self.delete(topic)
            return None
        
        logger.info(f"✅ 缓存命中: {topic} (有效期至 {expires_at.strftime('%Y-%m-%d %H:%M')})")
        return json.loads(results_json)
    
    def set(self, topic: str, results: List[Dict]):
        """
        保存结果到缓存
        
        Args:
            topic: 搜索主题
            results: 视频列表
        """
        query_key = self._make_key(topic)
        created_at = datetime.now()
        expires_at = created_at + timedelta(hours=self.expiry_hours)
        
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO video_cache 
            (query_key, topic, results, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            query_key,
            topic,
            json.dumps(results, ensure_ascii=False),
            created_at.isoformat(),
            expires_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ 结果已缓存: {topic} (有效期至 {expires_at.strftime('%Y-%m-%d %H:%M')})")
    
    def delete(self, topic: str):
        """
        删除缓存
        
        Args:
            topic: 搜索主题
        """
        query_key = self._make_key(topic)
        
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM video_cache WHERE query_key = ?', (query_key,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"缓存已删除: {topic}")
    
    def clear_expired(self):
        """清理所有过期的缓存"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'DELETE FROM video_cache WHERE expires_at < ?',
            (datetime.now().isoformat(),)
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            logger.info(f"✅ 清理了 {deleted_count} 条过期缓存")
    
    def clear_all(self):
        """清空所有缓存"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM video_cache')
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"✅ 清空了所有缓存 ({deleted_count} 条)")
    
    def _make_key(self, topic: str) -> str:
        """
        生成缓存键
        
        Args:
            topic: 主题
            
        Returns:
            缓存键
        """
        # 标准化主题（去除空格、转小写）
        return topic.strip().lower().replace(' ', '_')


def test_cache_manager():
    """测试缓存管理器"""
    import tempfile
    
    # 使用临时文件
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        cache_file = f.name
    
    try:
        cache = CacheManager(cache_file, expiry_hours=1)
        
        # 测试数据
        test_results = [
            {'title': 'Video 1', 'views': 100000},
            {'title': 'Video 2', 'views': 200000}
        ]
        
        print("\n=== 测试缓存 ===")
        
        # 设置缓存
        print("1. 保存缓存...")
        cache.set("AI coding", test_results)
        
        # 读取缓存
        print("2. 读取缓存...")
        cached = cache.get("AI coding")
        print(f"   结果: {cached is not None}")
        
        # 读取不存在的缓存
        print("3. 读取不存在的主题...")
        cached = cache.get("Non-existent topic")
        print(f"   结果: {cached is None}")
        
        # 清理过期缓存
        print("4. 清理过期缓存...")
        cache.clear_expired()
        
        print("\n✅ 缓存测试完成")
        
    finally:
        # 清理测试文件
        if os.path.exists(cache_file):
            os.remove(cache_file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_cache_manager()

