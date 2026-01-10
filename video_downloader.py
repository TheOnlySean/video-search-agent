#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频下载工具
支持 YouTube, Instagram, TikTok 等平台
"""

import os
import sys
from pathlib import Path
import yt_dlp


class VideoDownloader:
    def __init__(self, output_dir="downloads"):
        """
        初始化下载器
        :param output_dir: 下载文件保存目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download(self, url, quality="best"):
        """
        下载视频
        :param url: 视频链接
        :param quality: 视频质量 (best/worst/720p/1080p等)
        """
        try:
            # 配置下载选项
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'progress_hooks': [self._progress_hook],
                'quiet': False,
                'no_warnings': False,
                # TikTok 特定配置
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }
            
            # 根据平台调整配置
            if 'instagram.com' in url:
                # Instagram 特定配置
                ydl_opts['format'] = 'best'
            elif 'tiktok.com' in url:
                # TikTok 特定配置
                ydl_opts['format'] = 'best'
            
            print(f"\n开始下载: {url}")
            print(f"保存目录: {self.output_dir.absolute()}\n")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 获取视频信息
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                
                print(f"视频标题: {video_title}")
                if duration:
                    duration = int(duration)  # 确保 duration 是整数
                    print(f"视频时长: {duration // 60}:{duration % 60:02d}")
                print("")
                
                # 下载视频
                ydl.download([url])
                
            print(f"\n✅ 下载完成!")
            print(f"📁 文件保存在: {self.output_dir.absolute()}")
            return True
            
        except Exception as e:
            print(f"\n❌ 下载失败: {str(e)}")
            return False
    
    def _progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                print(f"\r下载中: {percent} | 速度: {speed} | 剩余时间: {eta}", end='', flush=True)
            except:
                pass
        elif d['status'] == 'finished':
            print(f"\n正在处理视频文件...")


def main():
    """主函数"""
    print("=" * 60)
    print("   视频下载工具")
    print("   支持: YouTube, Instagram, TikTok")
    print("=" * 60)
    print()
    
    # 创建下载器实例
    downloader = VideoDownloader(output_dir="downloads")
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        url = sys.argv[1]
        downloader.download(url)
    else:
        # 交互模式
        while True:
            print("\n请输入视频链接 (输入 'q' 退出):")
            url = input(">>> ").strip()
            
            if url.lower() in ['q', 'quit', 'exit', '退出']:
                print("\n再见! 👋")
                break
            
            if not url:
                print("❌ 请输入有效的链接!")
                continue
            
            if not any(platform in url.lower() for platform in ['youtube.com', 'youtu.be', 'instagram.com', 'tiktok.com']):
                print("⚠️  警告: 链接可能不是支持的平台,但我会尝试下载...")
            
            downloader.download(url)
            print("\n" + "-" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消操作 👋")
        sys.exit(0)


