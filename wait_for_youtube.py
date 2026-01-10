#!/usr/bin/env python3
"""
YouTube API 等待和重试工具
"""
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = 'AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY'

print("="*80)
print("🔄 YouTube API 连接测试工具")
print("="*80)
print("\n如果 API 刚刚启用，通常需要 2-5 分钟生效")
print("这个脚本会每 30 秒尝试一次，最多尝试 10 次\n")

max_attempts = 10
wait_seconds = 30

for attempt in range(1, max_attempts + 1):
    print(f"\n【尝试 {attempt}/{max_attempts}】")
    print(f"时间: {time.strftime('%H:%M:%S')}")
    
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        request = youtube.search().list(
            part='snippet',
            q='python',
            type='video',
            maxResults=1
        )
        
        print("正在调用 YouTube API...")
        response = request.execute()
        
        if response.get('items'):
            print("\n" + "="*80)
            print("🎉 成功！YouTube API 现在可以正常使用了！")
            print("="*80)
            print(f"\n测试视频: {response['items'][0]['snippet']['title']}")
            print(f"\n你现在可以运行:")
            print("  python3 test_api.py  # 完整测试")
            print("  python3 main.py \"AI编程\"  # 开始搜索")
            break
        else:
            print("⚠️  API 响应为空")
            
    except HttpError as e:
        if e.resp.status == 403:
            error_msg = e._get_reason()
            
            if 'blocked' in error_msg.lower():
                print(f"❌ 状态: API 请求被阻止")
                print(f"\n错误信息: {error_msg}")
                
                if attempt == 1:
                    print("\n可能的原因:")
                    print("  1. API 刚启用，还在生效中（继续等待）")
                    print("  2. API key 有限制设置")
                    print("\n请检查 Google Cloud Console:")
                    print("  → APIs & Services → Credentials")
                    print("  → 找到你的 API key")
                    print("  → 编辑 → API restrictions")
                    print("  → 确保 YouTube Data API v3 在允许列表中")
                    print("     或选择 'Don't restrict key'（不限制）")
                
                if attempt < max_attempts:
                    print(f"\n等待 {wait_seconds} 秒后重试...")
                    time.sleep(wait_seconds)
                else:
                    print("\n" + "="*80)
                    print("⚠️  已达到最大尝试次数")
                    print("="*80)
                    print("\n建议:")
                    print("  1. 检查 API key 的限制设置（见上面说明）")
                    print("  2. 确认 API 已在正确的项目中启用")
                    print("  3. 如果都正确，可能需要等待更长时间")
                    print("  4. 或者尝试创建一个新的 API key")
            else:
                print(f"❌ 403 错误: {error_msg}")
                break
                
        elif e.resp.status == 429:
            print("❌ 配额超限，请明天再试")
            break
        else:
            print(f"❌ HTTP {e.resp.status}: {e._get_reason()}")
            break
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        break

print("\n")

