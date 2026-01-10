#!/usr/bin/env python3
"""
欢迎使用视频搜索 Agent！
这个脚本会帮你检查环境和配置
"""
import sys
import os

def print_banner():
    """打印欢迎横幅"""
    print("\n" + "="*80)
    print("🎬 欢迎使用视频搜索 Agent！")
    print("="*80)
    print("\n这个工具可以帮你在 YouTube 和 Instagram 上找到最热门的视频！\n")

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要 Python 3.7 或更高版本")
        return False

def check_dependencies():
    """检查依赖是否安装"""
    required = [
        'googleapiclient',
        'google.generativeai',
        'instaloader',
        'dotenv',
        'requests'
    ]
    
    print("\n检查依赖包...")
    all_installed = True
    
    for package in required:
        try:
            __import__(package.replace('.', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - 未安装")
            all_installed = False
    
    if not all_installed:
        print("\n请运行以下命令安装依赖：")
        print("  pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """检查配置文件"""
    print("\n检查配置文件...")
    
    if not os.path.exists('.env'):
        print("  ❌ .env 文件不存在")
        print("\n请执行以下步骤：")
        print("  1. cp env_template.txt .env")
        print("  2. 编辑 .env 文件，填入你的 API Keys")
        print("\n获取 API Keys:")
        print("  - Gemini: https://ai.google.dev/")
        print("  - YouTube: https://console.cloud.google.com/")
        return False
    
    print("  ✅ .env 文件存在")
    
    # 尝试加载配置
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        youtube_key = os.getenv('YOUTUBE_API_KEY')
        
        if not gemini_key or gemini_key == 'your_gemini_api_key_here':
            print("  ⚠️  GEMINI_API_KEY 未设置")
            return False
        else:
            print("  ✅ GEMINI_API_KEY 已设置")
        
        if not youtube_key or youtube_key == 'your_youtube_api_key_here':
            print("  ⚠️  YOUTUBE_API_KEY 未设置")
            return False
        else:
            print("  ✅ YOUTUBE_API_KEY 已设置")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        return False

def show_usage():
    """显示使用方法"""
    print("\n" + "="*80)
    print("🚀 使用方法")
    print("="*80)
    print("\n命令行使用：")
    print("  python main.py \"你的搜索主题\"")
    print("\n示例：")
    print("  python main.py \"AI编程工具\"")
    print("  python main.py \"健身教程\"")
    print("  python main.py \"美食制作\"")
    print("\n查看更多示例：")
    print("  python examples.py")
    print("\n查看文档：")
    print("  - 完整文档: README.md")
    print("  - 快速开始: QUICKSTART.md 或 开始使用.md")
    print("  - 检查清单: CHECKLIST.md")

def main():
    """主函数"""
    print_banner()
    
    # 检查 Python 版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 检查配置
    config_ok = check_config()
    
    # 显示结果
    print("\n" + "="*80)
    if deps_ok and config_ok:
        print("✅ 所有检查通过！你可以开始使用了！")
        show_usage()
    else:
        print("⚠️  还有一些配置需要完成")
        print("\n请按照上面的提示完成配置，然后重新运行此脚本")
        print("或查看 QUICKSTART.md 获取详细指南")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()

