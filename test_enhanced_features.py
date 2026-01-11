#!/usr/bin/env python3
"""
测试新的深度分析功能
"""
import sys
sys.path.insert(0, '.')

from video_agent import VideoSearchAgent

def test_enhanced_analysis():
    """测试增强的 AI 分析功能"""
    
    print("🧪 测试新的深度分析功能")
    print("=" * 60)
    
    # 初始化 Agent（不使用缓存，确保获取最新数据）
    print("\n📦 初始化搜索引擎...")
    agent = VideoSearchAgent(use_cache=False)
    
    # 搜索测试
    query = "social media marketing"
    print(f"\n🔍 搜索: {query}")
    print("-" * 60)
    
    results = agent.search(query, top_n=3)
    
    if not results:
        print("❌ 未找到结果")
        return
    
    print(f"\n✅ 找到 {len(results)} 个视频\n")
    print("=" * 60)
    
    # 检查新字段
    for i, video in enumerate(results, 1):
        print(f"\n📺 视频 {i}: {video['title'][:60]}...")
        print(f"   作者: {video['author']}")
        print(f"   播放量: {video['views']:,}")
        print(f"   相关性评分: {video.get('ai_score', 'N/A')}")
        
        # 新字段检查
        print("\n   🆕 新增分析维度:")
        
        if video.get('hook_text'):
            print(f"   🎣 核心吸引点: {video['hook_text']}")
        else:
            print(f"   🎣 核心吸引点: ❌ 未提供")
        
        if video.get('replicability_score'):
            score = video['replicability_score']
            emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
            print(f"   ♻️  可复制性: {emoji} {score}/10")
        else:
            print(f"   ♻️  可复制性: ❌ 未提供")
        
        if video.get('key_takeaway'):
            print(f"   💡 关键学习点: {video['key_takeaway']}")
        else:
            print(f"   💡 关键学习点: ❌ 未提供")
        
        if video.get('recommendation_reason'):
            print(f"   ⭐ 成功原因: {video['recommendation_reason']}")
        else:
            print(f"   ⭐ 成功原因: ❌ 未提供")
        
        print("-" * 60)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 功能检测总结:")
    print("=" * 60)
    
    has_hooks = sum(1 for v in results if v.get('hook_text'))
    has_replicability = sum(1 for v in results if v.get('replicability_score'))
    has_takeaways = sum(1 for v in results if v.get('key_takeaway'))
    has_reasons = sum(1 for v in results if v.get('recommendation_reason'))
    
    print(f"✅ 核心吸引点: {has_hooks}/{len(results)} 个视频有数据")
    print(f"✅ 可复制性评分: {has_replicability}/{len(results)} 个视频有数据")
    print(f"✅ 关键学习点: {has_takeaways}/{len(results)} 个视频有数据")
    print(f"✅ 成功原因: {has_reasons}/{len(results)} 个视频有数据")
    
    if all([has_hooks, has_replicability, has_takeaways, has_reasons]):
        print("\n🎉 所有新功能都工作正常！")
    else:
        print("\n⚠️  部分功能可能需要调试")
    
    print("=" * 60)

if __name__ == '__main__':
    test_enhanced_analysis()

