#!/usr/bin/env python3
"""
测试中文自动翻译功能
"""
from video_agent import VideoSearchAgent

def test_chinese_translation():
    """测试中文搜索自动翻译"""
    
    print("🧪 测试中文自动翻译功能\n")
    print("="*60)
    
    # 初始化 Agent
    agent = VideoSearchAgent(use_cache=False)
    
    # 测试案例
    test_cases = [
        "自媒体运营",
        "视频剪辑教程",
        "AI工具推荐",
        "健身训练",
        "social media marketing"  # 英文，不应该翻译
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n【测试 {i}】搜索词: {query}")
        print("-" * 60)
        
        # 检测是否包含中文
        import re
        is_chinese = bool(re.search(r'[\u4e00-\u9fff]', query))
        
        if is_chinese:
            print(f"✅ 检测到中文")
            # 测试翻译
            english = agent._translate_to_english(query)
            print(f"📝 翻译结果: {english}")
        else:
            print(f"ℹ️  英文输入，无需翻译")
        
        print()
    
    print("="*60)
    print("✅ 测试完成！")

if __name__ == "__main__":
    test_chinese_translation()

