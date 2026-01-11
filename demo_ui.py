#!/usr/bin/env python3
"""
演示新 UI 应该显示的内容
"""
import os
os.environ['GEMINI_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'
os.environ['YOUTUBE_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'

import sys
sys.path.insert(0, '.')

from video_agent import VideoSearchAgent

print("=" * 80)
print("🎬 新 UI 演示 - 这就是你应该在 Streamlit 上看到的内容")
print("=" * 80)
print()

agent = VideoSearchAgent(use_cache=False)
results = agent.search("marketing", top_n=2)

print(f"✅ 找到 {len(results)} 个视频\n")

for i, video in enumerate(results, 1):
    print("┌" + "─" * 78 + "┐")
    print(f"│ 📺 视频 {i}: {video['title'][:65]}")
    print(f"│ 👤 作者: {video['author']}")
    print(f"│ 👁️  播放量: {video['views']:,} | 📅 {video['days_ago']} 天前")
    print("├" + "─" * 78 + "┤")
    
    # 新功能区域
    if video.get('hookText'):
        print(f"│ 🎣 核心吸引点: {video['hookText']}")
    else:
        print(f"│ ⚠️  [缺失] 核心吸引点")
    
    if video.get('replicabilityScore'):
        score = video['replicabilityScore']
        emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
        print(f"│ ♻️  可复制性: {emoji} {score}/10 分")
    else:
        print(f"│ ⚠️  [缺失] 可复制性评分")
    
    if video.get('keyLearningPoints'):
        print(f"│ 💡 关键学习点: {video['keyLearningPoints']}")
    else:
        print(f"│ ⚠️  [缺失] 关键学习点")
    
    if video.get('reasonForSuccess'):
        print(f"│ ⭐ 成功原因: {video['reasonForSuccess']}")
    else:
        print(f"│ ⚠️  [缺失] 成功原因")
    
    print("└" + "─" * 78 + "┘")
    print()

print("=" * 80)
print("📌 如果 Streamlit 上看不到这些，请检查：")
print("   1. 是否更新了 Streamlit Cloud 的 API Key")
print("   2. 是否搜索了新的关键词（不是缓存结果）")
print("   3. 是否等待了 2-3 分钟让部署完成")
print("   4. 是否强制刷新了浏览器 (Ctrl/Cmd + Shift + R)")
print("=" * 80)

