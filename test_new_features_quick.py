#!/usr/bin/env python3
"""
快速测试新功能（使用新 API Key）
"""
import os
os.environ['GEMINI_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'
os.environ['YOUTUBE_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'

import sys
sys.path.insert(0, '.')

from video_agent import VideoSearchAgent

def test():
    print("🧪 测试新的深度分析功能（使用新 API Key）")
    print("=" * 70)
    
    agent = VideoSearchAgent(use_cache=False)
    
    query = "social media growth tips"
    print(f"\n🔍 搜索: {query}")
    print("-" * 70)
    
    results = agent.search(query, top_n=2)
    
    if not results:
        print("❌ 未找到结果")
        return
    
    print(f"\n✅ 找到 {len(results)} 个视频\n")
    
    for i, video in enumerate(results, 1):
        print("=" * 70)
        print(f"📺 视频 {i}: {video['title']}")
        print(f"   👤 作者: {video['author']}")
        print(f"   👁️  播放: {video['views']:,}")
        print(f"   📊 评分: {video.get('ai_score', 'N/A')}")
        
        print("\n   🆕 深度分析:")
        print(f"   🎣 核心吸引点: {video.get('hookText', '❌ 无')}")
        print(f"   ♻️  可复制性: {video.get('replicabilityScore', '❌ 无')}/10")
        print(f"   💡 关键学习点: {video.get('keyLearningPoints', '❌ 无')}")
        print(f"   ⭐ 成功原因: {video.get('reasonForSuccess', '❌ 无')}")
    
    print("\n" + "=" * 70)
    
    # 检查是否有新数据
    has_new_data = any(v.get('hookText') for v in results)
    
    if has_new_data:
        print("🎉 新功能工作正常！前端会显示这些数据！")
    else:
        print("⚠️  新功能数据未生成，需要检查 AI 分析逻辑")

if __name__ == '__main__':
    test()

