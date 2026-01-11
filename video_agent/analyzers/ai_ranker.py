"""
AI 排序分析器 - 使用 Gemini 进行智能分析和排序
"""
import google.generativeai as genai
from typing import List, Dict
import logging
import json

logger = logging.getLogger(__name__)


class AIRanker:
    """AI 排序器（使用 Gemini）"""
    
    def __init__(self, api_key: str):
        """
        初始化 Gemini API
        
        Args:
            api_key: Gemini API 密钥
        """
        genai.configure(api_key=api_key)
        # 使用最新的 Gemini 模型
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("✅ Gemini AI 初始化成功")
    
    def score_relevance(self, videos: List[Dict], topic: str, 
                       target_count: int = 15) -> List[Dict]:
        """
        批量评估视频相关性（轻量分析）
        
        Args:
            videos: 候选视频列表
            topic: 搜索主题
            target_count: 目标保留数量
            
        Returns:
            带有AI评分的视频列表
        """
        if not videos:
            return []
        
        logger.info(f"开始 AI 相关性评分: {len(videos)} 个视频")
        
        try:
            # 构建批量分析的 prompt
            video_texts = []
            for i, video in enumerate(videos):
                video_text = f"{i+1}. [{video['platform']}] {video['title'][:100]}\n"
                video_text += f"   作者: {video['author']}\n"
                video_text += f"   描述: {video['description'][:150]}\n"
                video_text += f"   播放量: {video['views']:,} | {video['days_ago']}天前\n"
                video_texts.append(video_text)
            
            prompt = f"""
你是一个自媒体内容分析专家。请深度分析以下真实YouTube视频与主题"{topic}"的相关性。

⚠️ 重要：这些都是真实存在的视频，有真实的播放量和作者信息。请基于这些真实数据进行分析。

评分标准：
- 90-100分：完全相关，内容直接匹配主题，值得深度学习
- 70-89分：高度相关，涉及主题核心方面，有参考价值
- 50-69分：中度相关，部分内容相关
- 30-49分：弱相关，仅标题提及
- 0-29分：不相关或标题党

视频列表（真实YouTube数据）：
{chr(10).join(video_texts)}

请输出JSON数组，每个视频包含：
- id: 视频序号（1开始）
- score: 相关性评分（0-100）
- reason: 简短理由（15字内）
- hook: 这个视频的核心吸引点/钩子（15字内，如"7天涨粉10万"）

只输出JSON，不要其他文字：
[{{"id": 1, "score": 85, "reason": "完整教程覆盖核心要点", "hook": "从0到100万粉丝实战"}}, ...]
"""
            
            # 调用 Gemini
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # 清理可能的markdown代码块标记
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # 解析 JSON
            scores = json.loads(result_text)
            
            # 将评分添加到视频中
            for score_item in scores:
                idx = score_item['id'] - 1
                if 0 <= idx < len(videos):
                    videos[idx]['ai_score'] = score_item['score']
                    videos[idx]['ai_reason'] = score_item['reason']
                    videos[idx]['hook_text'] = score_item.get('hook', '')  # 钩子文本
            
            # 筛选高分视频
            filtered = [v for v in videos if v.get('ai_score', 0) >= 70]
            filtered = sorted(filtered, key=lambda x: x.get('ai_score', 0), reverse=True)
            
            # 限制数量
            filtered = filtered[:target_count]
            
            logger.info(f"✅ AI 评分完成: 保留 {len(filtered)} 个高相关视频")
            return filtered
            
        except Exception as e:
            logger.error(f"AI 评分失败: {e}")
            logger.warning("降级使用播放量排序")
            # 降级：使用播放量排序
            return sorted(videos, key=lambda x: x['views'], reverse=True)[:target_count]
    
    def rank_top_n(self, videos: List[Dict], topic: str, top_n: int = 10) -> List[Dict]:
        """
        精细排序，选出最终的 Top N
        
        Args:
            videos: 高质量候选视频
            topic: 搜索主题
            top_n: 最终返回数量
            
        Returns:
            排序后的 Top N 视频
        """
        if not videos:
            return []
        
        if len(videos) <= top_n:
            return videos
        
        logger.info(f"开始 AI 精细排序: 从 {len(videos)} 个中选出 Top {top_n}")
        
        try:
            # 构建视频列表
            video_texts = []
            for i, video in enumerate(videos):
                video_text = f"{i+1}. [{video['platform']}] {video['title'][:80]}\n"
                video_text += f"   作者: @{video['author']}\n"
                video_text += f"   播放量: {video['views']:,} | {video['days_ago']}天前\n"
                video_text += f"   相关性: {video.get('ai_score', 'N/A')}\n"
                video_texts.append(video_text)
            
            prompt = f"""
你是一个视频推荐专家。从以下视频中选出最好的{top_n}个，推荐给对"{topic}"感兴趣的用户。

选择标准：
1. 相关性：内容与主题高度匹配
2. 质量：播放量、互动率显示受欢迎程度
3. 时效性：较新的视频优先（但不是唯一标准）
4. 多样性：尽量覆盖主题的不同角度
5. 平台平衡：YouTube和Instagram都要有代表

候选视频：
{chr(10).join(video_texts)}

请输出JSON数组，选出最好的{top_n}个视频：
[
  {{
    "rank": 1,
    "id": 视频序号,
    "reason": "推荐理由（15字内）"
  }},
  ...
]

只输出JSON，不要其他文字。
"""
            
            # 调用 Gemini
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # 清理可能的markdown代码块标记
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # 解析 JSON
            rankings = json.loads(result_text)
            
            # 按排名组装结果
            ranked_videos = []
            for rank_item in rankings:
                idx = rank_item['id'] - 1
                if 0 <= idx < len(videos):
                    video = videos[idx].copy()
                    video['final_rank'] = rank_item['rank']
                    video['final_score'] = rank_item.get('finalScore', rank_item.get('score', 0))
                    video['recommendation_reason'] = rank_item.get('reasonForSuccess', rank_item.get('reason', ''))
                    video['replicability_score'] = rank_item.get('replicabilityScore', 0)
                    video['key_takeaway'] = rank_item.get('keyTakeaway', '')
                    ranked_videos.append(video)
            
            # 按排名排序
            ranked_videos = sorted(ranked_videos, key=lambda x: x['final_rank'])
            
            logger.info(f"✅ AI 排序完成: Top {len(ranked_videos)} 视频已选出")
            return ranked_videos[:top_n]
            
        except Exception as e:
            logger.error(f"AI 排序失败: {e}")
            logger.warning("降级使用综合排序")
            # 降级：使用综合评分排序
            for video in videos:
                # 综合评分 = AI相关性 * 0.6 + 归一化播放量 * 0.3 + 时效性 * 0.1
                max_views = max([v['views'] for v in videos])
                normalized_views = (video['views'] / max_views) * 100 if max_views > 0 else 0
                time_score = max(0, 100 - video['days_ago'] * 2)  # 越新越高分
                
                video['combined_score'] = (
                    video.get('ai_score', 50) * 0.6 +
                    normalized_views * 0.3 +
                    time_score * 0.1
                )
            
            sorted_videos = sorted(videos, key=lambda x: x.get('combined_score', 0), reverse=True)
            return sorted_videos[:top_n]


def test_ai_ranker():
    """测试 AI 排序器"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ 请先设置 GEMINI_API_KEY")
        return
    
    # 模拟视频数据
    test_videos = [
        {
            'platform': 'YouTube',
            'title': 'Learn AI Coding with ChatGPT',
            'description': 'Complete tutorial on using AI for programming',
            'views': 500000,
            'days_ago': 15,
            'author': 'TechGuru'
        },
        {
            'platform': 'Instagram',
            'title': 'Quick AI Programming Tips',
            'description': 'Short form content on AI coding',
            'views': 300000,
            'days_ago': 5,
            'author': 'CodeMaster'
        }
    ]
    
    ranker = AIRanker(api_key)
    
    print("\n=== 测试相关性评分 ===")
    scored = ranker.score_relevance(test_videos, "AI coding")
    for video in scored:
        print(f"  {video['title']}: {video.get('ai_score', 'N/A')} - {video.get('ai_reason', 'N/A')}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_ai_ranker()

