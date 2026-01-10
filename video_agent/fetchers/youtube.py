"""
YouTube 视频数据获取模块
"""
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class YouTubeFetcher:
    """YouTube 视频获取器"""
    
    def __init__(self, api_key: str):
        """
        初始化 YouTube API 客户端
        
        Args:
            api_key: YouTube Data API v3 密钥
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos(self, topic: str, max_results: int = 50, days_ago: int = 60) -> List[Dict]:
        """
        搜索 YouTube 视频
        
        Args:
            topic: 搜索主题
            max_results: 最大结果数
            days_ago: 搜索最近N天内的视频
            
        Returns:
            视频列表，每个视频包含标题、描述、播放量等信息
        """
        try:
            # 计算时间范围
            published_after = (datetime.utcnow() - timedelta(days=days_ago)).isoformat() + 'Z'
            
            logger.info(f"正在搜索 YouTube: 主题='{topic}', 最大结果={max_results}")
            
            # 第一步：搜索视频（包含长视频和Shorts）
            search_request = self.youtube.search().list(
                part='snippet',
                q=topic,
                type='video',
                publishedAfter=published_after,
                order='viewCount',  # 按播放量排序
                maxResults=max_results,
                regionCode='US',  # 美国区域
                relevanceLanguage='en',  # 英语相关性
                videoDuration='any'  # 包含所有长度（长视频和Shorts）
            )
            
            search_response = search_request.execute()
            
            # 提取视频ID
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                logger.warning("未找到任何视频")
                return []
            
            logger.info(f"找到 {len(video_ids)} 个视频，正在获取详细信息...")
            
            # 第二步：获取视频详细信息（包括播放量）
            videos_request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            
            videos_response = videos_request.execute()
            
            # 解析结果并过滤英语视频
            videos = []
            filtered_count = 0
            for item in videos_response.get('items', []):
                try:
                    video = self._parse_video(item)
                    
                    # 过滤：只保留英语视频
                    audio_lang = video.get('audio_language', '').lower()
                    lang = video.get('language', '').lower()
                    
                    # 检查是否是英语视频
                    is_english = (
                        audio_lang.startswith('en') or 
                        lang.startswith('en') or
                        # 如果没有语言信息，通过地区判断（美国区搜索默认英语内容）
                        (not audio_lang and not lang)
                    )
                    
                    if is_english:
                        videos.append(video)
                    else:
                        filtered_count += 1
                        logger.debug(f"过滤非英语视频: {video['title'][:50]} (语言: {audio_lang or lang or 'unknown'})")
                        
                except Exception as e:
                    logger.error(f"解析视频失败: {e}")
                    continue
            
            if filtered_count > 0:
                logger.info(f"过滤掉 {filtered_count} 个非英语视频")
            
            logger.info(f"成功获取 {len(videos)} 个英语 YouTube 视频（包含长视频和Shorts）")
            return videos
            
        except Exception as e:
            logger.error(f"YouTube 搜索失败: {e}")
            return []
    
    def _parse_video(self, item: Dict) -> Dict:
        """
        解析单个视频数据
        
        Args:
            item: YouTube API 返回的视频项
            
        Returns:
            标准化的视频字典
        """
        snippet = item['snippet']
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        # 解析播放量
        view_count = int(statistics.get('viewCount', 0))
        
        # 解析发布时间
        published_at = datetime.strptime(
            snippet['publishedAt'], 
            '%Y-%m-%dT%H:%M:%SZ'
        )
        days_ago = (datetime.utcnow() - published_at).days
        
        # 构建视频URL
        video_id = item['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # 获取频道信息
        channel_title = snippet.get('channelTitle', 'Unknown')
        channel_id = snippet.get('channelId', '')
        channel_url = f"https://www.youtube.com/channel/{channel_id}" if channel_id else ''
        
        # 获取视频时长（用于判断是否是 Shorts）
        duration = content_details.get('duration', '')
        
        # 获取语言信息（用于过滤）
        default_audio_language = snippet.get('defaultAudioLanguage', '')
        default_language = snippet.get('defaultLanguage', '')
        
        return {
            'platform': 'YouTube',
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'url': video_url,
            'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
            'views': view_count,
            'likes': int(statistics.get('likeCount', 0)),
            'comments': int(statistics.get('commentCount', 0)),
            'author': channel_title,
            'author_url': channel_url,
            'published_at': published_at.isoformat(),
            'days_ago': days_ago,
            'tags': snippet.get('tags', []),
            'duration': duration,
            'audio_language': default_audio_language,
            'language': default_language
        }


def test_youtube_fetcher():
    """测试 YouTube 获取器"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key or api_key == 'your_youtube_api_key_here':
        print("❌ 请先设置 YOUTUBE_API_KEY")
        return
    
    fetcher = YouTubeFetcher(api_key)
    videos = fetcher.search_videos("AI coding", max_results=10)
    
    print(f"\n✅ 找到 {len(videos)} 个视频：")
    for i, video in enumerate(videos[:5], 1):
        print(f"\n{i}. {video['title']}")
        print(f"   播放量: {video['views']:,}")
        print(f"   作者: {video['author']}")
        print(f"   链接: {video['url']}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_youtube_fetcher()

