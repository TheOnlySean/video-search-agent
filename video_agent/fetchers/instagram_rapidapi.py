"""
Instagram RapidAPI 获取器 - 使用 RapidAPI 服务
"""
import requests
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class InstagramRapidAPIFetcher:
    """Instagram RapidAPI 获取器"""
    
    def __init__(self, api_key: str, api_host: str = None):
        """
        初始化 RapidAPI 客户端
        
        Args:
            api_key: RapidAPI Key
            api_host: API Host (默认使用 instagram-scraper-stable-api)
        """
        self.api_key = api_key
        self.api_host = api_host or "instagram-scraper-stable-api.p.rapidapi.com"
        self.base_url = f"https://{self.api_host}"
        
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-rapidapi-host": self.api_host,
            "x-rapidapi-key": self.api_key
        }
        
        logger.info(f"✅ Instagram RapidAPI 初始化成功")
    
    def search_users(self, query: str, limit: int = 50) -> List[Dict]:
        """
        搜索用户
        
        Args:
            query: 搜索关键词
            limit: 返回数量
            
        Returns:
            用户列表
        """
        # 这个端点名称需要根据实际 API 调整
        endpoint = "/search_users_v2.php"  # 待确认
        
        payload = {
            "query": query,
            "count": limit
        }
        
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                data=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('users', [])
            else:
                logger.error(f"搜索用户失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"搜索用户异常: {e}")
            return []
    
    def get_user_posts(self, username: str, limit: int = 50) -> List[Dict]:
        """
        获取用户的帖子
        
        Args:
            username: 用户名
            limit: 返回数量
            
        Returns:
            帖子列表
        """
        # 端点名称待确认
        endpoint = "/get_ig_user_posts_v2.php"  # 待确认
        
        payload = {
            "username_or_id_or_url": username,
            "count": limit
        }
        
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                data=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                logger.error(f"获取用户帖子失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取用户帖子异常: {e}")
            return []
    
    def get_hashtag_posts(self, hashtag: str, limit: int = 50) -> List[Dict]:
        """
        按话题获取帖子
        
        Args:
            hashtag: 话题标签（不含#）
            limit: 返回数量
            
        Returns:
            帖子列表
        """
        # 端点名称待确认
        endpoint = "/get_ig_hashtag_posts_v2.php"  # 待确认
        
        # 清理 hashtag
        hashtag = hashtag.replace('#', '').strip()
        
        payload = {
            "hashtag": hashtag,
            "count": limit
        }
        
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                data=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                logger.error(f"获取话题帖子失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取话题帖子异常: {e}")
            return []
    
    def search_videos(self, topic: str, max_results: int = 50, 
                     days_ago: int = 60, min_views: int = 200000) -> List[Dict]:
        """
        搜索视频（与系统集成的接口）
        
        Args:
            topic: 搜索主题
            max_results: 最大结果数
            days_ago: 最近N天
            min_views: 最小播放量
            
        Returns:
            标准化的视频列表
        """
        logger.info(f"正在搜索 Instagram (RapidAPI): 主题='{topic}'")
        
        # 方法1: 尝试按话题搜索
        posts = self.get_hashtag_posts(topic, max_results)
        
        # 方法2: 如果方法1失败，搜索用户然后获取他们的帖子
        if not posts:
            logger.info("尝试通过用户搜索...")
            users = self.search_users(topic, limit=10)
            posts = []
            for user in users[:5]:  # 只取前5个用户
                user_posts = self.get_user_posts(user['username'], limit=10)
                posts.extend(user_posts)
        
        # 转换为标准格式
        videos = []
        for post in posts:
            try:
                video = self._parse_post(post)
                
                # 应用筛选条件
                if video['views'] >= min_views:
                    if video['days_ago'] <= days_ago:
                        videos.append(video)
                        
            except Exception as e:
                logger.debug(f"解析帖子失败: {e}")
                continue
        
        logger.info(f"✅ 找到 {len(videos)} 个符合条件的 Instagram 视频")
        return videos[:max_results]
    
    def _parse_post(self, post: Dict) -> Dict:
        """
        解析 Instagram 帖子为标准格式
        
        Args:
            post: RapidAPI 返回的帖子数据
            
        Returns:
            标准化的视频字典
        """
        # 这个函数需要根据实际 API 响应格式调整
        
        # 提取基本信息
        video_id = post.get('id', post.get('pk', ''))
        caption = post.get('caption', {})
        if isinstance(caption, dict):
            caption_text = caption.get('text', '')
        else:
            caption_text = str(caption)
        
        # 标题
        title = caption_text[:100] if caption_text else f"Instagram Post {video_id}"
        
        # 播放量（视频）
        views = post.get('view_count', post.get('play_count', 0))
        
        # 点赞和评论
        likes = post.get('like_count', 0)
        comments = post.get('comment_count', 0)
        
        # 发布时间
        taken_at = post.get('taken_at', 0)
        if taken_at:
            published_at = datetime.fromtimestamp(taken_at)
            days_ago = (datetime.now() - published_at).days
        else:
            published_at = datetime.now()
            days_ago = 0
        
        # 作者
        user = post.get('user', {})
        author = user.get('username', 'unknown')
        
        # URL
        code = post.get('code', video_id)
        url = f"https://www.instagram.com/p/{code}/" if code else ''
        author_url = f"https://www.instagram.com/{author}/"
        
        return {
            'platform': 'Instagram',
            'video_id': str(video_id),
            'title': title,
            'description': caption_text,
            'url': url,
            'thumbnail': post.get('thumbnail_url', ''),
            'views': views,
            'likes': likes,
            'comments': comments,
            'author': author,
            'author_url': author_url,
            'published_at': published_at.isoformat(),
            'days_ago': days_ago,
            'tags': []
        }


def test_rapidapi_fetcher():
    """测试 RapidAPI 获取器"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('RAPIDAPI_KEY')
    api_host = os.getenv('RAPIDAPI_HOST')
    
    if not api_key:
        print("❌ 请先在 .env 中设置 RAPIDAPI_KEY")
        return
    
    print("=== 测试 Instagram RapidAPI 获取器 ===\n")
    
    fetcher = InstagramRapidAPIFetcher(api_key, api_host)
    
    # 测试搜索用户
    print("1. 测试搜索用户...")
    users = fetcher.search_users("fitness", limit=3)
    print(f"   找到 {len(users)} 个用户")
    
    # 测试搜索视频
    print("\n2. 测试搜索视频...")
    videos = fetcher.search_videos("fitness", max_results=5, min_views=50000)
    print(f"   找到 {len(videos)} 个视频")
    
    if videos:
        print("\n前3个视频:")
        for v in videos[:3]:
            print(f"  - {v['title'][:50]}...")
            print(f"    {v['views']:,} 播放")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_rapidapi_fetcher()

