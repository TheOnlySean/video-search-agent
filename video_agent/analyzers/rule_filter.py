"""
规则筛选器 - 基于硬性规则快速过滤视频
"""
from typing import List, Dict
import logging
import re

logger = logging.getLogger(__name__)


class RuleFilter:
    """规则筛选器"""
    
    def __init__(self, min_views: int = 200000, max_days_ago: int = 60):
        """
        初始化筛选器
        
        Args:
            min_views: 最小播放量
            max_days_ago: 最近N天内的视频
        """
        self.min_views = min_views
        self.max_days_ago = max_days_ago
    
    def filter(self, videos: List[Dict], topic: str, target_count: int = 30) -> List[Dict]:
        """
        应用规则筛选
        
        Args:
            videos: 候选视频列表
            topic: 搜索主题（仅用于日志，不再用于关键词匹配）
            target_count: 目标保留数量
            
        Returns:
            筛选后的视频列表
        """
        logger.info(f"开始规则筛选: 输入{len(videos)}个视频, 目标{target_count}个")
        logger.info(f"筛选条件: 播放量≥{self.min_views:,}, 发布时间≤{self.max_days_ago}天")
        
        filtered = []
        stats = {
            'views': 0,
            'time': 0,
            'passed': 0
        }
        
        for video in videos:
            # 规则1：播放量检查
            if video['views'] < self.min_views:
                stats['views'] += 1
                logger.debug(f"❌ 播放量不足: {video['title'][:50]} ({video['views']:,} < {self.min_views:,})")
                continue
            
            # 规则2：时间检查
            if video['days_ago'] > self.max_days_ago:
                stats['time'] += 1
                logger.debug(f"❌ 发布时间过久: {video['title'][:50]} ({video['days_ago']}天 > {self.max_days_ago}天)")
                continue
            
            # 注意：我们移除了关键词匹配检查
            # 原因：YouTube API 已经根据搜索词返回了相关结果
            # 后续还有 AI 来评估相关性，没必要在这里二次过滤
            
            stats['passed'] += 1
            filtered.append(video)
        
        # 如果结果太多，按播放量排序并截取
        if len(filtered) > target_count:
            filtered = sorted(filtered, key=lambda x: x['views'], reverse=True)[:target_count]
            logger.info(f"📊 结果过多，按播放量排序后截取前 {target_count} 个")
        
        logger.info(f"✅ 规则筛选完成: 保留{len(filtered)}个视频")
        logger.info(f"📊 过滤统计: 播放量不足={stats['views']}, 时间过久={stats['time']}, 通过={stats['passed']}")
        return filtered
    
    def _is_relevant(self, video: Dict, topic: str) -> bool:
        """
        检查视频是否与主题相关（基础关键词匹配）
        
        Args:
            video: 视频信息
            topic: 主题
            
        Returns:
            是否相关
        """
        # 提取关键词
        keywords = self._extract_keywords(topic)
        
        # 构建搜索文本
        search_text = f"{video['title']} {video['description']}".lower()
        
        # 检查是否包含任意关键词
        for keyword in keywords:
            if keyword.lower() in search_text:
                return True
        
        # 检查标签
        tags = video.get('tags', [])
        for tag in tags:
            for keyword in keywords:
                if keyword.lower() in tag.lower():
                    return True
        
        return False
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """
        从主题中提取关键词
        
        Args:
            topic: 主题字符串
            
        Returns:
            关键词列表
        """
        # 清理和分词
        words = re.findall(r'\w+', topic.lower())
        
        # 过滤停用词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been'}
        
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # 如果关键词太少，返回原始主题
        if not keywords:
            return [topic]
        
        return keywords


def test_rule_filter():
    """测试规则筛选器"""
    # 模拟视频数据
    test_videos = [
        {
            'title': 'Learn AI Coding in 10 Minutes',
            'description': 'A tutorial on AI-assisted coding',
            'views': 500000,
            'days_ago': 15,
            'tags': ['ai', 'coding', 'tutorial']
        },
        {
            'title': 'Cooking Recipes',
            'description': 'How to cook pasta',
            'views': 300000,
            'days_ago': 20,
            'tags': ['cooking', 'food']
        },
        {
            'title': 'AI Programming Tutorial',
            'description': 'Complete guide',
            'views': 150000,  # 播放量不足
            'days_ago': 10,
            'tags': ['ai', 'programming']
        },
        {
            'title': 'ChatGPT for Developers',
            'description': 'Using AI in development',
            'views': 800000,
            'days_ago': 80,  # 时间过久
            'tags': ['chatgpt', 'ai']
        }
    ]
    
    filter = RuleFilter(min_views=200000, max_days_ago=60)
    filtered = filter.filter(test_videos, "AI coding", target_count=10)
    
    print(f"\n✅ 筛选结果: {len(filtered)}/4 个视频通过")
    for video in filtered:
        print(f"  - {video['title']}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_rule_filter()

