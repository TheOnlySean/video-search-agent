#!/usr/bin/env python3
"""
API 测试脚本 - 检查你的 API keys 是否正常工作
"""
import sys
import os

# 设置 API key（从命令行参数或环境变量获取）
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    API_KEY = 'AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY'

print("="*80)
print("🔑 API 测试工具")
print("="*80)
print(f"\n使用的 API Key: {API_KEY[:20]}...\n")

# ==================== 测试 1: Gemini API ====================
print("="*80)
print("测试 1: Google Gemini API")
print("="*80)

try:
    import google.generativeai as genai
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("\n正在测试 Gemini API...")
    response = model.generate_content("请用中文回复'你好'，只需一个词")
    
    if response.text:
        print("✅ Gemini API 工作正常！")
        print(f"   响应: {response.text.strip()}")
        gemini_ok = True
    else:
        print("⚠️  Gemini API 响应为空")
        gemini_ok = False
        
except Exception as e:
    print(f"❌ Gemini API 测试失败")
    print(f"   错误: {e}")
    gemini_ok = False

# ==================== 测试 2: YouTube Data API ====================
print("\n" + "="*80)
print("测试 2: YouTube Data API v3")
print("="*80)

try:
    from googleapiclient.discovery import build
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    print("\n正在测试 YouTube Data API...")
    
    # 尝试搜索
    request = youtube.search().list(
        part='snippet',
        q='python',
        type='video',
        maxResults=2
    )
    response = request.execute()
    
    if response.get('items'):
        print("✅ YouTube Data API 工作正常！")
        print(f"   找到 {len(response['items'])} 个测试视频")
        for i, item in enumerate(response['items'], 1):
            print(f"   {i}. {item['snippet']['title'][:50]}...")
        youtube_ok = True
    else:
        print("⚠️  YouTube API 响应为空")
        youtube_ok = False
        
except Exception as e:
    error_msg = str(e)
    print(f"❌ YouTube Data API 测试失败")
    
    if 'blocked' in error_msg.lower() or '403' in error_msg:
        print("\n   原因: YouTube Data API v3 未启用")
        print("\n   解决方法:")
        print("   1. 访问 https://console.cloud.google.com/")
        print("   2. 选择你的项目")
        print("   3. 进入 'APIs & Services' > 'Library'")
        print("   4. 搜索 'YouTube Data API v3'")
        print("   5. 点击 'ENABLE'（启用）")
        print("   6. 等待几分钟生效后重试")
    else:
        print(f"   错误: {error_msg[:200]}")
    
    youtube_ok = False

# ==================== 总结 ====================
print("\n" + "="*80)
print("📊 测试结果总结")
print("="*80)

print(f"\n✅ Gemini API: {'正常' if gemini_ok else '失败'}")
print(f"{'✅' if youtube_ok else '❌'} YouTube API: {'正常' if youtube_ok else '需要启用'}")

if gemini_ok and youtube_ok:
    print("\n🎉 太好了！所有 API 都工作正常！")
    print("\n你现在可以使用视频搜索 Agent 了：")
    print("  python main.py \"AI编程\"")
    print("\n或者查看示例：")
    print("  python examples.py")
    sys.exit(0)
    
elif gemini_ok and not youtube_ok:
    print("\n⚠️  Gemini API 正常，但 YouTube API 需要启用")
    print("\n当前可以做的：")
    print("  - 使用 AI 分析功能")
    print("  - 只搜索 Instagram（如果配置了）")
    print("\n需要做的：")
    print("  1. 在 Google Cloud Console 启用 YouTube Data API v3")
    print("  2. 等待几分钟后重新运行此脚本测试")
    sys.exit(1)
    
elif youtube_ok and not gemini_ok:
    print("\n⚠️  YouTube API 正常，但 Gemini API 有问题")
    print("\n请检查:")
    print("  - API key 是否来自 https://ai.google.dev/")
    print("  - 账号是否有 Gemini API 访问权限")
    sys.exit(1)
    
else:
    print("\n❌ 两个 API 都有问题")
    print("\n建议:")
    print("  1. 检查 API key 是否正确")
    print("  2. 确认 Google Cloud 项目配置正确")
    print("  3. 查看 QUICKSTART.md 了解详细设置步骤")
    sys.exit(1)

