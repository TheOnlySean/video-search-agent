#!/usr/bin/env python3
"""
检查 Streamlit 部署状态
"""
import requests
import json

def check_streamlit_deployment():
    print("=" * 80)
    print("🔍 检查 Streamlit 部署状态")
    print("=" * 80)
    print()
    
    app_url = "https://video-search-agent-smfrxp96bjth8s4bh7zyj7.streamlit.app/"
    
    print(f"📍 应用地址: {app_url}")
    print()
    
    try:
        print("⏳ 正在检查应用状态...")
        response = requests.get(app_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ 应用在线运行中")
            print(f"   状态码: {response.status_code}")
            print(f"   响应大小: {len(response.content)} bytes")
            
            # 检查是否是最新版本
            content = response.text
            
            if 'hookText' in content or '核心吸引点' in content:
                print()
                print("🎉 检测到新功能代码！")
                print("   前端代码已更新，包含新的分析维度")
            else:
                print()
                print("⚠️  未检测到新功能代码")
                print("   可能原因：")
                print("   1. Streamlit Cloud 还在部署中")
                print("   2. 浏览器缓存了旧版本")
                print("   3. GitHub 代码未同步到 Streamlit Cloud")
            
            if 'AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0' in content:
                print()
                print("⚠️  警告：API Key 出现在前端代码中！")
                print("   （这不应该发生，但不影响功能）")
                
        else:
            print(f"⚠️  应用响应异常: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ 连接超时 - 应用可能正在重启或部署中")
        print("   请等待 2-3 分钟后再试")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
    
    print()
    print("=" * 80)
    print("📋 下一步操作：")
    print("=" * 80)
    print()
    print("1️⃣  更新 API Key：")
    print("   https://share.streamlit.io/")
    print("   → 找到 video-search-agent")
    print("   → Settings → Secrets")
    print("   → 粘贴新的 API Key")
    print("   → Save")
    print()
    print("2️⃣  重启应用：")
    print("   → 点击右上角 ⋮")
    print("   → Reboot app")
    print()
    print("3️⃣  清除缓存并测试：")
    print("   → 强制刷新浏览器 (Cmd+Shift+R)")
    print("   → 搜索新关键词: 'youtube growth'")
    print()
    print("=" * 80)

if __name__ == '__main__':
    check_streamlit_deployment()

