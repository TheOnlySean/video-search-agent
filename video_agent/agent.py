"""
视频搜索 Agent 主程序
"""
from typing import List, Dict, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .fetchers import YouTubeFetcher, InstagramFetcher
from .analyzers import RuleFilter, AIRanker
from .cache import CacheManager
from . import config

logger = logging.getLogger(__name__)


class VideoSearchAgent:
    """视频搜索 Agent"""
    
    def __init__(self, use_cache: bool = True):
        """
        初始化 Agent
        
        Args:
            use_cache: 是否使用缓存
        """
        # 验证配置
        config.validate_config()
        
        # 初始化组件
        self.youtube_fetcher = YouTubeFetcher(config.YOUTUBE_API_KEY)
        self.instagram_fetcher = InstagramFetcher(
            config.INSTAGRAM_USERNAME,
            config.INSTAGRAM_PASSWORD
        )
        self.rule_filter = RuleFilter(
            min_views=config.MIN_VIEWS,
            max_days_ago=config.MAX_DAYS_AGO
        )
        self.ai_ranker = AIRanker(config.GEMINI_API_KEY)
        
        # 缓存管理
        self.use_cache = use_cache and config.CACHE_ENABLED
        if self.use_cache:
            self.cache = CacheManager(
                config.CACHE_FILE,
                config.CACHE_EXPIRY_HOURS
            )
        
        logger.info("✅ 视频搜索 Agent 初始化完成")
    
    def search(self, topic: str, top_n: int = 10) -> List[Dict]:
        """
        搜索热门视频
        
        Args:
            topic: 搜索主题
            top_n: 返回的视频数量
            
        Returns:
            排序后的视频列表
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 开始搜索: {topic}")
        logger.info(f"{'='*60}\n")
        
        # 检查缓存
        if self.use_cache:
            cached_results = self.cache.get(topic)
            if cached_results:
                logger.info("✅ 使用缓存结果")
                return cached_results[:top_n]
        
        # 第1步：并行获取数据
        logger.info("【步骤 1/4】从各平台获取数据...")
        all_videos = self._fetch_from_all_platforms(topic)
        logger.info(f"✅ 共获取 {len(all_videos)} 个候选视频\n")
        
        if not all_videos:
            logger.warning("未找到任何视频")
            return []
        
        # 第2步：规则筛选
        logger.info("【步骤 2/4】应用规则筛选...")
        filtered_videos = self.rule_filter.filter(
            all_videos,
            topic,
            target_count=config.RULE_FILTER_COUNT
        )
        logger.info(f"✅ 规则筛选保留 {len(filtered_videos)} 个视频\n")
        
        if not filtered_videos:
            logger.warning("规则筛选后无结果")
            return []
        
        # 第3步：AI相关性评分
        logger.info("【步骤 3/4】AI 相关性分析...")
        scored_videos = self.ai_ranker.score_relevance(
            filtered_videos,
            topic,
            target_count=config.AI_FILTER_COUNT
        )
        logger.info(f"✅ AI 筛选保留 {len(scored_videos)} 个高相关视频\n")
        
        if not scored_videos:
            logger.warning("AI筛选后无结果")
            return filtered_videos[:top_n]
        
        # 第4步：AI精细排序
        logger.info(f"【步骤 4/4】AI 精细排序，选出 Top {top_n}...")
        final_results = self.ai_ranker.rank_top_n(
            scored_videos,
            topic,
            top_n=top_n
        )
        logger.info(f"✅ 最终选出 {len(final_results)} 个视频\n")
        
        # 保存到缓存
        if self.use_cache and final_results:
            self.cache.set(topic, final_results)
        
        logger.info(f"{'='*60}")
        logger.info(f"✅ 搜索完成！")
        logger.info(f"{'='*60}\n")
        
        return final_results
    
    def _fetch_from_all_platforms(self, topic: str) -> List[Dict]:
        """
        并行从所有平台获取视频
        
        Args:
            topic: 搜索主题
            
        Returns:
            合并的视频列表
        """
        all_videos = []
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(
                    self.youtube_fetcher.search_videos,
                    topic,
                    config.MAX_RESULTS_PER_PLATFORM,
                    config.MAX_DAYS_AGO
                ): 'YouTube',
                executor.submit(
                    self.instagram_fetcher.search_videos,
                    topic,
                    config.MAX_RESULTS_PER_PLATFORM,
                    config.MAX_DAYS_AGO,
                    config.MIN_VIEWS
                ): 'Instagram'
            }
            
            for future in as_completed(futures):
                platform = futures[future]
                try:
                    videos = future.result()
                    logger.info(f"  ✓ {platform}: {len(videos)} 个视频")
                    all_videos.extend(videos)
                except Exception as e:
                    logger.error(f"  ✗ {platform} 获取失败: {e}")
        
        return all_videos
    
    def clear_cache(self, topic: Optional[str] = None):
        """
        清理缓存
        
        Args:
            topic: 要清理的主题，如果为 None 则清理所有
        """
        if not self.use_cache:
            logger.warning("缓存未启用")
            return
        
        if topic:
            self.cache.delete(topic)
        else:
            self.cache.clear_all()


def format_results(videos: List[Dict]) -> str:
    """
    格式化输出结果
    
    Args:
        videos: 视频列表
        
    Returns:
        格式化的字符串
    """
    if not videos:
        return "未找到任何视频。"
    
    output = []
    output.append("\n" + "="*80)
    output.append(f"🎬 找到 {len(videos)} 个热门视频")
    output.append("="*80 + "\n")
    
    for i, video in enumerate(videos, 1):
        output.append(f"{i}. [{video['platform']}] {video['title']}")
        output.append(f"   👤 作者: @{video['author']}")
        output.append(f"      主页: {video['author_url']}")
        output.append(f"   📊 播放量: {video['views']:,}")
        output.append(f"   📅 发布时间: {video['days_ago']} 天前")
        output.append(f"   🔗 链接: {video['url']}")
        
        # AI 评分信息（如果有）
        if 'ai_score' in video:
            output.append(f"   🤖 相关性: {video['ai_score']}/100 ({video.get('ai_reason', '')})")
        
        # 推荐理由（如果有）
        if 'recommendation_reason' in video:
            output.append(f"   💡 推荐理由: {video['recommendation_reason']}")
        
        output.append("")
    
    return "\n".join(output)


def main():
    """主函数 - 命令行交互"""
    import sys
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    try:
        # 初始化 Agent
        agent = VideoSearchAgent(use_cache=True)
        
        # 获取搜索主题
        if len(sys.argv) > 1:
            topic = ' '.join(sys.argv[1:])
        else:
            print("\n🎬 视频搜索 Agent")
            print("=" * 80)
            topic = input("\n请输入搜索主题（如：AI编程工具、健身教程等）: ").strip()
        
        if not topic:
            print("❌ 主题不能为空")
            return
        
        # 执行搜索
        results = agent.search(topic, top_n=10)
        
        # 输出结果
        print(format_results(results))
        
        # 导出选项
        export = input("\n是否导出为JSON文件？(y/n): ").strip().lower()
        if export == 'y':
            import json
            filename = f"results_{topic.replace(' ', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 已导出到: {filename}")
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消操作")
    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n请检查 .env 文件中的 API keys 配置")
    except Exception as e:
        logger.exception(f"发生错误: {e}")


if __name__ == '__main__':
    main()

