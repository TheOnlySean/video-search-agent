# Google AI Studio 中使用 YouTube Data API 的解决方案

## 问题说明

Google AI Studio 的 Build 功能主要用于 Gemini AI，**不能直接调用 YouTube Data API**。

---

## 🎯 解决方案

### 方案 A：在 Google AI Studio 外部运行（推荐）

**原理**：将代码移到正常的 Python 环境中运行

#### 步骤 1：创建独立的 Python 脚本

创建文件 `youtube_search.py`：

```python
#!/usr/bin/env python3
"""
YouTube 视频搜索工具
可以同时使用 Gemini AI 和 YouTube Data API
"""

import os
from googleapiclient.discovery import build
import google.generativeai as genai
from datetime import datetime, timedelta

# ==================== 配置 ====================

# API Keys
GEMINI_API_KEY = "your_gemini_api_key_here"
YOUTUBE_API_KEY = "your_youtube_api_key_here"

# ==================== YouTube 搜索 ====================

def search_youtube_videos(query, max_results=10):
    """
    搜索 YouTube 视频
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量
        
    Returns:
        视频列表
    """
    try:
        # 初始化 YouTube API 客户端
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # 计算时间范围（最近60天）
        published_after = (datetime.utcnow() - timedelta(days=60)).isoformat() + 'Z'
        
        # 搜索视频
        search_request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            publishedAfter=published_after,
            order='viewCount',
            maxResults=max_results,
            regionCode='US',
            relevanceLanguage='en'
        )
        
        search_response = search_request.execute()
        
        # 提取视频ID
        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
        
        if not video_ids:
            print("未找到视频")
            return []
        
        # 获取视频详细信息
        videos_request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        )
        
        videos_response = videos_request.execute()
        
        # 解析视频信息
        videos = []
        for item in videos_response.get('items', []):
            video = {
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'url': f"https://www.youtube.com/watch?v={item['id']}"
            }
            videos.append(video)
        
        return videos
        
    except Exception as e:
        print(f"YouTube API 错误: {e}")
        return []

# ==================== Gemini AI 分析 ====================

def analyze_videos_with_gemini(videos, topic):
    """
    使用 Gemini AI 分析视频相关性
    
    Args:
        videos: 视频列表
        topic: 搜索主题
        
    Returns:
        分析结果
    """
    try:
        # 初始化 Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 构建 prompt
        video_list = "\n".join([
            f"{i+1}. {v['title']} - {v['channel']} ({v['views']:,} views)"
            for i, v in enumerate(videos)
        ])
        
        prompt = f"""
请分析以下视频与主题 "{topic}" 的相关性，并给出推荐理由。

视频列表：
{video_list}

请为每个视频评分（1-10分）并说明理由。
"""
        
        # 调用 Gemini
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Gemini API 错误: {e}")
        return None

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("🎬 YouTube 视频搜索工具")
    print("=" * 60)
    
    # 输入搜索关键词
    query = input("\n请输入搜索关键词: ")
    
    # 1. 搜索 YouTube 视频
    print(f"\n🔍 正在搜索 YouTube: {query}")
    videos = search_youtube_videos(query, max_results=10)
    
    if not videos:
        print("❌ 未找到视频")
        return
    
    print(f"✅ 找到 {len(videos)} 个视频\n")
    
    # 显示视频列表
    print("📊 视频列表：")
    print("-" * 60)
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
        print(f"   频道: {video['channel']}")
        print(f"   播放量: {video['views']:,}")
        print(f"   链接: {video['url']}")
        print()
    
    # 2. 使用 Gemini AI 分析
    print("🤖 正在使用 Gemini AI 分析...")
    analysis = analyze_videos_with_gemini(videos, query)
    
    if analysis:
        print("\n" + "=" * 60)
        print("AI 分析结果：")
        print("=" * 60)
        print(analysis)
    
    print("\n✅ 完成！")

if __name__ == '__main__':
    main()
```

#### 步骤 2：安装依赖

```bash
pip install google-api-python-client google-generativeai
```

#### 步骤 3：配置 API Keys

修改脚本中的 API Keys：
```python
GEMINI_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
YOUTUBE_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
```

#### 步骤 4：运行

```bash
python3 youtube_search.py
```

---

### 方案 B：使用 Function Calling（在 AI Studio 中间接调用）

如果必须在 Google AI Studio 中使用，可以通过 **Function Calling** 来调用外部 API。

#### 概念

```
Google AI Studio (Gemini)
    ↓ Function Calling
    ↓
外部 API 服务（你自己搭建）
    ↓ 调用 YouTube API
    ↓
返回结果给 Gemini
```

#### 实现步骤

1. **创建一个外部 API 服务**（使用 Flask 或 FastAPI）
2. **在 AI Studio 中定义 Function**
3. **Gemini 调用你的 Function**
4. **Function 内部调用 YouTube API**

**示例代码**（外部 API 服务）：

```python
from flask import Flask, request, jsonify
from googleapiclient.discovery import build

app = Flask(__name__)
YOUTUBE_API_KEY = "your_youtube_api_key"

@app.route('/search_youtube', methods=['POST'])
def search_youtube():
    """YouTube 搜索 API 端点"""
    data = request.json
    query = data.get('query')
    
    # 调用 YouTube API
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=10
    ).execute()
    
    # 返回结果
    videos = [
        {
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'videoId': item['id']['videoId']
        }
        for item in search_response.get('items', [])
    ]
    
    return jsonify(videos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**在 AI Studio 中定义 Function**：

```python
# 在 Google AI Studio 中
import requests

def search_youtube_videos(query: str):
    """搜索 YouTube 视频"""
    response = requests.post(
        'http://your-server.com:5000/search_youtube',
        json={'query': query}
    )
    return response.json()
```

---

### 方案 C：使用 Google Cloud Functions（云函数）

部署一个云函数来调用 YouTube API，然后在 AI Studio 中调用这个云函数。

**优点**：
- 完全托管
- 自动扩展
- 与 Google Cloud 集成好

**缺点**：
- 需要 Google Cloud 账号
- 可能有额外成本

---

## 🎯 推荐方案

### 对于你的同事：

**最简单的方案**：**方案 A - 在 Python 环境中运行**

**原因**：
1. ✅ 最简单直接
2. ✅ 无需额外服务
3. ✅ 完全控制代码
4. ✅ 可以同时使用 Gemini 和 YouTube API
5. ✅ 便于调试

---

## 📋 给你同事的快速指南

### 快速开始（5分钟）

**1. 创建文件 `search.py`**（复制上面的完整代码）

**2. 安装依赖**：
```bash
pip install google-api-python-client google-generativeai
```

**3. 填入 API Keys**（这两个 key 是同一个）：
```python
GEMINI_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
YOUTUBE_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
```

**4. 运行**：
```bash
python3 search.py
```

**5. 输入搜索关键词**，比如：`social media marketing`

**6. 查看结果**！

---

## 🔑 关于 API Key

你提供的这个 key 可以同时用于：
- ✅ Gemini AI API
- ✅ YouTube Data API v3

因为它们都是 Google Cloud 的 API。

---

## ❓ 常见问题

### Q1: 为什么 Google AI Studio 不能直接用 YouTube API？

**A**: Google AI Studio 是一个专门为 Gemini AI 设计的沙盒环境，不支持其他 Google APIs。

### Q2: 我必须在 AI Studio 中使用怎么办？

**A**: 使用方案 B 或 C，通过外部服务间接调用。

### Q3: 这个脚本能在哪里运行？

**A**: 任何有 Python 的环境：
- 本地电脑（Mac/Windows/Linux）
- Google Colab
- 云服务器
- Replit
- 任何支持 Python 的平台

### Q4: 有没有在线运行的方案？

**A**: 可以用 **Google Colab**（免费）：
1. 访问 https://colab.research.google.com/
2. 创建新笔记本
3. 粘贴代码
4. 运行

---

## 💡 总结

**核心问题**：Google AI Studio 的 Build 功能只支持 Gemini API，不支持其他 Google APIs。

**最佳解决方案**：将代码移到正常的 Python 环境（本地/Colab/服务器）。

**给你同事的建议**：使用上面的完整脚本，在本地 Python 或 Google Colab 中运行。

---

把这个指南发给你的同事，他应该就能解决问题了！如果还有问题，随时告诉我！🚀

