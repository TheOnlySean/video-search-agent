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
            
            # 解析结果并过滤欧美英语视频
            videos = []
            filtered_stats = {'non_western': 0, 'other_lang': 0, 'passed': 0}
            
            # 接受的欧美英语区域代码
            western_english_regions = {
                'en-us', 'en-gb', 'en-ca', 'en-au',  # 美国、英国、加拿大、澳大利亚
                'en', 'en-nz', 'en-ie',               # 通用英语、新西兰、爱尔兰
            }
            
            # 需要排除的非欧美区域
            excluded_regions = {
                'en-in',  # 印度
                'en-ph',  # 菲律宾
                'en-pk',  # 巴基斯坦
                'en-sg',  # 新加坡
                'en-za',  # 南非
            }
            
            for item in videos_response.get('items', []):
                try:
                    video = self._parse_video(item)
                    
                    # 获取语言信息
                    audio_lang = video.get('audio_language', '').lower()
                    lang = video.get('language', '').lower()
                    
                    # 检查主要语言标识
                    primary_lang = audio_lang or lang or ''
                    
                    # 判断是否是欧美英语视频
                    is_western_english = False
                    
                    if primary_lang:
                        # 如果明确是排除的区域，直接过滤
                        if primary_lang in excluded_regions:
                            filtered_stats['non_western'] += 1
                            logger.debug(f"❌ 过滤非欧美区域: {video['title'][:50]} ({primary_lang})")
                            continue
                        
                        # 检查是否是接受的欧美英语
                        if primary_lang in western_english_regions or primary_lang.startswith('en-us') or primary_lang.startswith('en-gb'):
                            is_western_english = True
                        elif primary_lang.startswith('en'):
                            # 如果是其他 en- 开头但不在白名单中，也过滤
                            filtered_stats['non_western'] += 1
                            logger.debug(f"❌ 过滤非欧美英语: {video['title'][:50]} ({primary_lang})")
                            continue
                        else:
                            # 非英语
                            filtered_stats['other_lang'] += 1
                            logger.debug(f"❌ 过滤非英语: {video['title'][:50]} ({primary_lang})")
                            continue
                    else:
                        # 没有语言标记，通过美国区域搜索，默认接受
                        is_western_english = True
                    
                    if is_western_english:
                        filtered_stats['passed'] += 1
                        videos.append(video)
                        
                except Exception as e:
                    logger.error(f"解析视频失败: {e}")
                    continue
            
            # 日志统计
            total_filtered = filtered_stats['non_western'] + filtered_stats['other_lang']
            if total_filtered > 0:
                logger.info(f"📊 过滤统计: 非欧美区域={filtered_stats['non_western']}, 其他语言={filtered_stats['other_lang']}")
            
            logger.info(f"✅ 成功获取 {len(videos)} 个欧美英语视频（包含长视频和Shorts）")
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

