"""
Instagram 视频数据获取模块
"""
import instaloader
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import time

logger = logging.getLogger(__name__)


class InstagramFetcher:
    """Instagram Reels 获取器"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化 Instagram 客户端
        
        Args:
            username: Instagram 用户名（可选，登录可减少限制）
            password: Instagram 密码（可选）
        """
        self.loader = instaloader.Instaloader(
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True
        )
        
        self.logged_in = False
        
        # 尝试登录（如果提供了凭据）
        if username and password:
            try:
                logger.info(f"正在登录 Instagram: {username}")
                self.loader.login(username, password)
                self.logged_in = True
                logger.info("✅ Instagram 登录成功")
            except Exception as e:
                logger.warning(f"Instagram 登录失败: {e}，将使用未登录模式")
    
    def search_videos(self, topic: str, max_results: int = 50, days_ago: int = 60, 
                     min_views: int = 200000) -> List[Dict]:
        """
        搜索 Instagram Reels
        
        Args:
            topic: 搜索主题（作为hashtag）
            max_results: 最大结果数
            days_ago: 搜索最近N天内的视频
            min_views: 最小播放量
            
        Returns:
            视频列表
        """
        try:
            # 清理话题标签
            hashtag = topic.replace('#', '').replace(' ', '').lower()
            
            logger.info(f"正在搜索 Instagram: 话题=#{hashtag}, 最大结果={max_results}")
            
            if not self.logged_in:
                logger.warning("⚠️  未登录 Instagram，可能会遇到限制。建议提供登录凭据。")
            
            # 获取hashtag
            try:
                hashtag_obj = instaloader.Hashtag.from_name(self.loader.context, hashtag)
            except Exception as e:
                logger.error(f"无法找到话题 #{hashtag}: {e}")
                return []
            
            videos = []
            cutoff_date = datetime.now() - timedelta(days=days_ago)
            
            # 遍历帖子
            post_count = 0
            for post in hashtag_obj.get_posts():
                try:
                    # 限制请求数量
                    post_count += 1
                    if post_count > max_results * 3:  # 多查一些，因为有筛选
                        break
                    
                    # 只处理视频
                    if not post.is_video:
                        continue
                    
                    # 检查日期
                    if post.date < cutoff_date:
                        continue
                    
                    # 检查播放量
                    if post.video_view_count and post.video_view_count < min_views:
                        continue
                    
                    # 解析视频
                    video = self._parse_post(post)
                    videos.append(video)
                    
                    logger.debug(f"找到视频: {video['title'][:50]}... (播放量: {video['views']:,})")
                    
                    # 达到目标数量就停止
                    if len(videos) >= max_results:
                        break
                    
                    # 添加延迟，避免被限制
                    time.sleep(2)
                    
                except Exception as e:
                    logger.debug(f"跳过帖子: {e}")
                    continue
            
            logger.info(f"成功获取 {len(videos)} 个 Instagram 视频")
            return videos
            
        except Exception as e:
            logger.error(f"Instagram 搜索失败: {e}")
            return []
    
    def _parse_post(self, post) -> Dict:
        """
        解析单个 Instagram 帖子
        
        Args:
            post: Instaloader Post 对象
            
        Returns:
            标准化的视频字典
        """
        # 获取标题（caption）
        caption = post.caption if post.caption else ''
        title = caption[:100] if caption else f"Video by {post.owner_username}"
        
        # 计算发布时间
        days_ago = (datetime.now() - post.date).days
        
        # 构建URL
        video_url = f"https://www.instagram.com/p/{post.shortcode}/"
        author_url = f"https://www.instagram.com/{post.owner_username}/"
        
        return {
            'platform': 'Instagram',
            'video_id': post.shortcode,
            'title': title,
            'description': caption,
            'url': video_url,
            'thumbnail': post.url,  # 帖子的图片URL
            'views': post.video_view_count if post.video_view_count else 0,
            'likes': post.likes,
            'comments': post.comments,
            'author': post.owner_username,
            'author_url': author_url,
            'published_at': post.date.isoformat(),
            'days_ago': days_ago,
            'tags': list(post.caption_hashtags) if post.caption_hashtags else []
        }


def test_instagram_fetcher():
    """测试 Instagram 获取器"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    # 不登录也可以尝试
    fetcher = InstagramFetcher(username, password)
    
    # 测试搜索（使用一个常见的话题）
    videos = fetcher.search_videos("coding", max_results=5, min_views=100000)
    
    print(f"\n✅ 找到 {len(videos)} 个视频：")
    for i, video in enumerate(videos, 1):
        print(f"\n{i}. {video['title'][:60]}...")
        print(f"   播放量: {video['views']:,}")
        print(f"   作者: @{video['author']}")
        print(f"   链接: {video['url']}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_instagram_fetcher()

