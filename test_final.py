#!/usr/bin/env python3
"""
快速测试新功能（使用新 API Key，更广泛的搜索）
"""
import os
os.environ['GEMINI_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'
os.environ['YOUTUBE_API_KEY'] = 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0'

import sys
sys.path.insert(0, '.')

from video_agent import VideoSearchAgent

def test():
    print("🧪 测试新的深度分析功能（搜索热门话题）")
    print("=" * 70)
    
    agent = VideoSearchAgent(use_cache=False)
    
    # 使用更广泛的搜索词
    query = "marketing"
    print(f"\n🔍 搜索: {query}")
    print("-" * 70)
    
    results = agent.search(query, top_n=3)
    
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
        hook = video.get('hookText', '')
        rep_score = video.get('replicabilityScore', 0)
        key_points = video.get('keyLearningPoints', '')
        success = video.get('reasonForSuccess', '')
        
        if hook:
            print(f"   ✅ 🎣 核心吸引点: {hook}")
        else:
            print(f"   ❌ 🎣 核心吸引点: 无")
        
        if rep_score:
            emoji = "🟢" if rep_score >= 7 else "🟡" if rep_score >= 4 else "🔴"
            print(f"   ✅ ♻️  可复制性: {emoji} {rep_score}/10")
        else:
            print(f"   ❌ ♻️  可复制性: 无")
        
        if key_points:
            print(f"   ✅ 💡 关键学习点: {key_points}")
        else:
            print(f"   ❌ 💡 关键学习点: 无")
        
        if success:
            print(f"   ✅ ⭐ 成功原因: {success}")
        else:
            print(f"   ❌ ⭐ 成功原因: 无")
    
    print("\n" + "=" * 70)
    
    # 检查是否有新数据
    has_hooks = sum(1 for v in results if v.get('hookText'))
    has_rep = sum(1 for v in results if v.get('replicabilityScore'))
    has_key = sum(1 for v in results if v.get('keyLearningPoints'))
    has_success = sum(1 for v in results if v.get('reasonForSuccess'))
    
    print(f"📊 新功能数据统计:")
    print(f"   核心吸引点: {has_hooks}/{len(results)}")
    print(f"   可复制性评分: {has_rep}/{len(results)}")
    print(f"   关键学习点: {has_key}/{len(results)}")
    print(f"   成功原因: {has_success}/{len(results)}")
    
    if all([has_hooks, has_rep, has_key, has_success]):
        print("\n🎉 所有新功能都工作正常！前端会显示这些数据！")
    else:
        print(f"\n⚠️  新功能数据未完全生成（{has_hooks + has_rep + has_key + has_success}/12 字段有数据）")

if __name__ == '__main__':
    test()

