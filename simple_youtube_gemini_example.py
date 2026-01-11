#!/usr/bin/env python3
"""
简单的 YouTube 视频搜索示例
可以同时使用 Gemini AI 和 YouTube Data API
适合在本地 Python 环境或 Google Colab 中运行
"""

from googleapiclient.discovery import build
import google.generativeai as genai
from datetime import datetime, timedelta

# ==================== 配置 API Keys ====================
# 这两个 key 实际上是同一个（Google Cloud 统一管理）
GEMINI_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
YOUTUBE_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"

# ==================== YouTube 搜索功能 ====================

def search_youtube(query, max_results=10):
    """搜索 YouTube 视频"""
    print(f"🔍 搜索 YouTube: {query}")
    
    # 初始化 YouTube API
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    # 搜索视频
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        order='viewCount',
        regionCode='US',
        relevanceLanguage='en'
    ).execute()
    
    # 获取视频ID
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    
    # 获取视频详情
    videos_response = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()
    
    # 解析视频信息
    videos = []
    for item in videos_response.get('items', []):
        videos.append({
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'views': int(item['statistics'].get('viewCount', 0)),
            'url': f"https://www.youtube.com/watch?v={item['id']}"
        })
    
    print(f"✅ 找到 {len(videos)} 个视频\n")
    return videos

# ==================== Gemini AI 分析 ====================

def analyze_with_gemini(videos, topic):
    """使用 Gemini AI 分析视频"""
    print("🤖 使用 Gemini AI 分析视频相关性...\n")
    
    # 初始化 Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 构建视频列表
    video_list = "\n".join([
        f"{i+1}. 【{v['views']:,} views】{v['title']} - {v['channel']}"
        for i, v in enumerate(videos)
    ])
    
    # AI 分析
    prompt = f"""
请分析以下视频与主题 "{topic}" 的相关性。

视频列表：
{video_list}

请为每个视频：
1. 评分（0-100分）
2. 说明相关性
3. 推荐理由（如果相关）

输出格式：
1. 标题 - 评分：XX分 - 理由：...
"""
    
    response = model.generate_content(prompt)
    return response.text

# ==================== 主程序 ====================

def main():
    print("=" * 70)
    print("🎬 YouTube 视频搜索 + Gemini AI 分析工具")
    print("=" * 70)
    print()
    
    # 用户输入
    query = input("请输入搜索关键词（中文会自动翻译）: ").strip()
    
    if not query:
        print("❌ 请输入搜索关键词")
        return
    
    print()
    
    try:
        # 1. 搜索 YouTube
        videos = search_youtube(query, max_results=10)
        
        if not videos:
            print("❌ 未找到视频")
            return
        
        # 2. 显示视频列表
        print("📊 搜索结果：")
        print("-" * 70)
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title']}")
            print(f"   📺 频道: {video['channel']}")
            print(f"   👁️  播放量: {video['views']:,}")
            print(f"   🔗 链接: {video['url']}")
            print()
        
        # 3. Gemini AI 分析
        print("=" * 70)
        analysis = analyze_with_gemini(videos, query)
        print("🤖 AI 分析结果：")
        print("=" * 70)
        print(analysis)
        print()
        
        print("=" * 70)
        print("✅ 搜索完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n请检查：")
        print("1. API Keys 是否正确")
        print("2. YouTube Data API 是否已启用")
        print("3. 网络连接是否正常")

# ==================== 运行 ====================

if __name__ == '__main__':
    main()

