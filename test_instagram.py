#!/usr/bin/env python3
"""
Instagram 登录测试工具
"""
import instaloader
import os
import sys
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

print("="*80)
print("🔐 Instagram 登录测试")
print("="*80)
print(f"\n用户名: {username}")

if not username or not password:
    print("❌ 未找到 Instagram 登录信息")
    print("\n请确认 .env 文件中已配置:")
    print("  INSTAGRAM_USERNAME=你的用户名")
    print("  INSTAGRAM_PASSWORD=你的密码")
    sys.exit(1)

print("\n正在尝试登录...\n")

try:
    L = instaloader.Instaloader(
        quiet=True,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False
    )
    
    L.login(username, password)
    
    print("✅ Instagram 登录成功！\n")
    
    # 测试获取账号信息
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"账号信息:")
        print(f"  - 用户名: {profile.username}")
        print(f"  - 粉丝数: {profile.followers}")
        print(f"  - 关注数: {profile.followees}")
        print(f"  - 帖子数: {profile.mediacount}")
    except Exception as e:
        print(f"⚠️  无法获取账号信息: {e}")
    
    print("\n" + "="*80)
    print("✅ Instagram 配置成功！")
    print("="*80)
    print("\n现在你可以:")
    print("  1. 搜索 Instagram 视频")
    print("  2. 运行完整搜索（YouTube + Instagram）")
    print("\n示例:")
    print("  python3 main.py \"fitness\"")
    print("  python3 main.py \"travel\"")
    print("  python3 main.py \"cooking\"")
    
    sys.exit(0)
    
except instaloader.exceptions.BadCredentialsException:
    print("❌ 登录失败：用户名或密码错误")
    print("\n请检查:")
    print("  1. 用户名是否正确")
    print("  2. 密码是否正确")
    sys.exit(1)
    
except instaloader.exceptions.ConnectionException as e:
    error_msg = str(e)
    
    if 'Checkpoint required' in error_msg:
        print("❌ 需要完成安全验证")
        print("\nInstagram 检测到新的登录尝试，需要验证身份。")
        print("\n请按照以下步骤操作:")
        print("  1. 打开浏览器访问: https://www.instagram.com/")
        print("  2. 登录你的账号")
        print("  3. 完成任何安全验证（邮箱/手机/人机验证）")
        print("  4. 等待 2-3 分钟")
        print("  5. 重新运行此脚本: python3 test_instagram.py")
        print("\n这是 Instagram 的正常安全机制。")
        
    elif 'Two-factor authentication' in error_msg:
        print("❌ 账号启用了双因素验证")
        print("\n请:")
        print("  1. 关闭双因素验证")
        print("  2. 或使用应用专用密码")
        
    else:
        print(f"❌ 连接失败: {e}")
        print("\n可能的原因:")
        print("  1. 网络问题")
        print("  2. Instagram 服务器限制")
        print("  3. IP 被临时限制")
        
    sys.exit(1)
    
except Exception as e:
    print(f"❌ 发生未知错误: {e}")
    print(f"\n错误类型: {type(e).__name__}")
    sys.exit(1)

