"""
使用示例 - 展示如何在代码中使用 Video Search Agent
"""
from video_agent import VideoSearchAgent, format_results
import logging

# 配置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def example_1_basic_search():
    """示例1：基础搜索"""
    print("\n" + "="*80)
    print("示例 1: 基础搜索")
    print("="*80)
    
    # 初始化 Agent（启用缓存）
    agent = VideoSearchAgent(use_cache=True)
    
    # 搜索视频
    results = agent.search("AI编程工具", top_n=10)
    
    # 显示结果
    print(format_results(results))


def example_2_custom_config():
    """示例2：自定义配置"""
    print("\n" + "="*80)
    print("示例 2: 自定义配置")
    print("="*80)
    
    from video_agent import config
    
    # 临时修改配置
    original_min_views = config.MIN_VIEWS
    config.MIN_VIEWS = 100000  # 降低播放量要求
    
    try:
        agent = VideoSearchAgent(use_cache=False)
        results = agent.search("健身教程", top_n=5)
        
        print(f"\n找到 {len(results)} 个视频（播放量 > 10万）")
        for video in results[:3]:
            print(f"  - {video['title']} ({video['views']:,} 播放)")
    
    finally:
        # 恢复原配置
        config.MIN_VIEWS = original_min_views


def example_3_process_results():
    """示例3：处理搜索结果"""
    print("\n" + "="*80)
    print("示例 3: 处理和分析结果")
    print("="*80)
    
    agent = VideoSearchAgent()
    results = agent.search("Python教程", top_n=10)
    
    # 统计各平台视频数量
    platform_stats = {}
    for video in results:
        platform = video['platform']
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    
    print("\n平台分布：")
    for platform, count in platform_stats.items():
        print(f"  {platform}: {count} 个视频")
    
    # 找出播放量最高的视频
    if results:
        top_video = max(results, key=lambda x: x['views'])
        print(f"\n播放量最高：")
        print(f"  {top_video['title']}")
        print(f"  {top_video['views']:,} 播放量")
    
    # 计算平均播放量
    if results:
        avg_views = sum(v['views'] for v in results) / len(results)
        print(f"\n平均播放量：{avg_views:,.0f}")


def example_4_export_results():
    """示例4：导出结果"""
    print("\n" + "="*80)
    print("示例 4: 导出结果到文件")
    print("="*80)
    
    import json
    from datetime import datetime
    
    agent = VideoSearchAgent()
    results = agent.search("旅游vlog", top_n=10)
    
    # 导出为 JSON
    filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已导出到: {filename}")
    
    # 导出为 CSV
    import csv
    csv_filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=[
                'platform', 'title', 'author', 'views', 
                'days_ago', 'url', 'author_url'
            ])
            writer.writeheader()
            for video in results:
                writer.writerow({
                    'platform': video['platform'],
                    'title': video['title'],
                    'author': video['author'],
                    'views': video['views'],
                    'days_ago': video['days_ago'],
                    'url': video['url'],
                    'author_url': video['author_url']
                })
    
    print(f"✅ 已导出到: {csv_filename}")


def example_5_batch_search():
    """示例5：批量搜索多个主题"""
    print("\n" + "="*80)
    print("示例 5: 批量搜索")
    print("="*80)
    
    topics = ["AI编程", "健身教程", "美食制作"]
    
    agent = VideoSearchAgent()
    
    all_results = {}
    for topic in topics:
        print(f"\n搜索主题: {topic}")
        results = agent.search(topic, top_n=5)
        all_results[topic] = results
        print(f"  找到 {len(results)} 个视频")
    
    # 汇总统计
    print("\n\n=== 汇总统计 ===")
    for topic, results in all_results.items():
        total_views = sum(v['views'] for v in results)
        print(f"{topic}: {len(results)} 个视频, 总播放量 {total_views:,}")


def example_6_cache_management():
    """示例6：缓存管理"""
    print("\n" + "="*80)
    print("示例 6: 缓存管理")
    print("="*80)
    
    agent = VideoSearchAgent(use_cache=True)
    
    # 第一次搜索（会查询API）
    print("\n第一次搜索...")
    results1 = agent.search("AI工具", top_n=5)
    print(f"耗时：正常（查询API）")
    
    # 第二次搜索（使用缓存）
    print("\n第二次搜索同样的主题...")
    results2 = agent.search("AI工具", top_n=5)
    print(f"耗时：很快（使用缓存）")
    
    # 清理特定主题缓存
    print("\n清理缓存...")
    agent.clear_cache("AI工具")
    print("✅ 缓存已清理")


def example_7_error_handling():
    """示例7：错误处理"""
    print("\n" + "="*80)
    print("示例 7: 错误处理")
    print("="*80)
    
    try:
        agent = VideoSearchAgent()
        results = agent.search("测试主题", top_n=10)
        
        if not results:
            print("⚠️  未找到符合条件的视频")
            print("建议：")
            print("  1. 尝试更通用的关键词")
            print("  2. 降低播放量要求")
            print("  3. 扩大时间范围")
        else:
            print(f"✅ 找到 {len(results)} 个视频")
    
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("请检查 .env 文件中的 API keys")
    
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        print("请查看日志了解详细信息")


def example_8_youtube_only():
    """示例8：只搜索 YouTube"""
    print("\n" + "="*80)
    print("示例 8: 只搜索 YouTube")
    print("="*80)
    
    from video_agent.fetchers import YouTubeFetcher
    from video_agent.analyzers import RuleFilter, AIRanker
    from video_agent import config
    
    # 只使用 YouTube
    youtube = YouTubeFetcher(config.YOUTUBE_API_KEY)
    videos = youtube.search_videos("编程教程", max_results=20)
    
    # 筛选和排序
    rule_filter = RuleFilter()
    filtered = rule_filter.filter(videos, "编程教程", target_count=10)
    
    ai_ranker = AIRanker(config.GEMINI_API_KEY)
    final_results = ai_ranker.rank_top_n(filtered, "编程教程", top_n=5)
    
    print(f"\n找到 {len(final_results)} 个 YouTube 视频")
    for video in final_results:
        print(f"  - {video['title']}")


def main():
    """运行所有示例"""
    examples = [
        ("基础搜索", example_1_basic_search),
        ("自定义配置", example_2_custom_config),
        ("处理结果", example_3_process_results),
        ("导出结果", example_4_export_results),
        ("批量搜索", example_5_batch_search),
        ("缓存管理", example_6_cache_management),
        ("错误处理", example_7_error_handling),
        ("只搜索YouTube", example_8_youtube_only),
    ]
    
    print("\n" + "="*80)
    print("Video Search Agent - 使用示例")
    print("="*80)
    print("\n可用示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. 运行所有示例")
    
    choice = input("\n请选择要运行的示例 (0-8): ").strip()
    
    if choice == '0':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n❌ {name} 运行失败: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        try:
            func()
        except Exception as e:
            print(f"\n❌ {name} 运行失败: {e}")
    else:
        print("❌ 无效选择")


if __name__ == '__main__':
    main()

