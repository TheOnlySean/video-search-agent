# 开发者文档

## 项目架构

### 整体设计

```
┌─────────────────────────────────────┐
│         用户/应用层                  │
│   main.py / examples.py            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│         Agent 协调层                │
│      VideoSearchAgent              │
│   (video_agent/agent.py)           │
└──────────────┬──────────────────────┘
               ↓
    ┌──────────┴──────────┐
    ↓                     ↓
┌─────────────┐    ┌─────────────┐
│  数据获取层  │    │  分析处理层  │
│  Fetchers   │    │  Analyzers  │
└─────────────┘    └─────────────┘
    ↓                     ↓
┌─────────────┐    ┌─────────────┐
│  YouTube    │    │ RuleFilter  │
│  Instagram  │    │  AIRanker   │
└─────────────┘    └─────────────┘
               ↓
┌─────────────────────────────────────┐
│         支持层                       │
│   Cache / Config / Utils           │
└─────────────────────────────────────┘
```

### 核心模块

#### 1. VideoSearchAgent (agent.py)

主控制器，协调所有模块完成搜索流程。

**职责**：
- 接收用户查询
- 协调数据获取和分析
- 管理缓存
- 返回最终结果

**关键方法**：
```python
search(topic, top_n) -> List[Dict]
    执行完整的搜索流程
    
_fetch_from_all_platforms(topic) -> List[Dict]
    并行从所有平台获取数据
    
clear_cache(topic)
    清理缓存
```

#### 2. Fetchers (fetchers/)

数据获取层，负责从各平台获取原始数据。

**YouTubeFetcher** (`youtube.py`)
- 使用官方 YouTube Data API v3
- 支持按播放量排序
- 自动获取视频详细信息

**InstagramFetcher** (`instagram.py`)
- 使用 `instaloader` 库
- 支持 hashtag 搜索
- 可选登录以减少限制

**接口规范**：
```python
search_videos(topic, max_results, days_ago) -> List[Dict]
```

**返回格式**：
```python
{
    'platform': str,      # 'YouTube' or 'Instagram'
    'video_id': str,
    'title': str,
    'description': str,
    'url': str,
    'thumbnail': str,
    'views': int,
    'likes': int,
    'comments': int,
    'author': str,
    'author_url': str,
    'published_at': str,  # ISO format
    'days_ago': int,
    'tags': List[str]
}
```

#### 3. Analyzers (analyzers/)

分析处理层，负责筛选和排序。

**RuleFilter** (`rule_filter.py`)
- 基于硬性规则的快速筛选
- 播放量、时间、关键词匹配
- 无 API 调用，速度快

**AIRanker** (`ai_ranker.py`)
- 使用 Gemini 进行智能分析
- 批量处理降低成本
- 两阶段排序：相关性评分 + 精细排序

**方法**：
```python
RuleFilter.filter(videos, topic, target_count) -> List[Dict]
AIRanker.score_relevance(videos, topic, target_count) -> List[Dict]
AIRanker.rank_top_n(videos, topic, top_n) -> List[Dict]
```

#### 4. Cache (cache.py)

缓存管理，使用 SQLite 存储查询结果。

**特性**：
- 自动过期（默认 2 小时）
- 主题标准化（避免重复缓存）
- 支持清理过期缓存

#### 5. Config (config.py)

配置管理，集中管理所有配置项。

**配置项**：
```python
# API Keys
GEMINI_API_KEY
YOUTUBE_API_KEY
INSTAGRAM_USERNAME
INSTAGRAM_PASSWORD

# 搜索参数
MAX_RESULTS_PER_PLATFORM = 50
MIN_VIEWS = 200000
MAX_DAYS_AGO = 60
TOP_N_RESULTS = 10

# 筛选参数
RULE_FILTER_COUNT = 30
AI_FILTER_COUNT = 15

# 缓存配置
CACHE_ENABLED = True
CACHE_EXPIRY_HOURS = 2
```

## 数据流

### 完整搜索流程

```
1. 用户输入 "AI编程"
   ↓
2. 检查缓存 (cache.py)
   ├─ 命中 → 直接返回
   └─ 未命中 → 继续
   ↓
3. 并行获取数据 (fetchers/)
   ├─ YouTubeFetcher.search_videos()  [50个]
   └─ InstagramFetcher.search_videos() [50个]
   ↓ 合并
   [100个候选视频]
   ↓
4. 规则筛选 (analyzers/rule_filter.py)
   ├─ views >= 200,000
   ├─ days_ago <= 60
   └─ 关键词匹配
   ↓
   [~30个视频]
   ↓
5. AI相关性评分 (analyzers/ai_ranker.py)
   ├─ Gemini批量分析标题+描述
   ├─ 评分 0-100
   └─ 筛选 score >= 70
   ↓
   [~15个高分视频]
   ↓
6. AI精细排序 (analyzers/ai_ranker.py)
   ├─ 综合评估
   ├─ 平台平衡
   └─ 多样性考虑
   ↓
   [Top 10]
   ↓
7. 保存缓存
   ↓
8. 返回结果
```

## 成本优化策略

### API 调用优化

1. **批量处理**
   - 一次 Gemini 调用处理 20-30 个视频
   - 减少往返次数

2. **分层筛选**
   - 先用免费的规则筛选
   - 再用付费的 AI 分析

3. **缓存机制**
   - 相同查询 2 小时内重用结果
   - 避免重复 API 调用

4. **降级策略**
   - AI 失败时使用规则排序
   - 确保系统可用性

### 成本分解

单次查询约 $0.03：
- YouTube API: $0（免费）
- Instagram: $0（开源库）
- Gemini 相关性评分: ~$0.01
- Gemini 精细排序: ~$0.02

## 扩展指南

### 添加新平台（如 TikTok）

1. 创建 `fetchers/tiktok.py`：

```python
class TikTokFetcher:
    def __init__(self, api_key):
        # 初始化
        pass
    
    def search_videos(self, topic, max_results, days_ago):
        # 返回标准格式的视频列表
        return [...]
```

2. 在 `agent.py` 中添加：

```python
self.tiktok_fetcher = TikTokFetcher(config.TIKTOK_API_KEY)

# 在 _fetch_from_all_platforms 中添加
executor.submit(
    self.tiktok_fetcher.search_videos,
    topic, max_results, days_ago
): 'TikTok'
```

### 自定义筛选规则

编辑 `analyzers/rule_filter.py`：

```python
def _is_relevant(self, video, topic):
    # 添加你的自定义逻辑
    if '广告' in video['title']:
        return False
    return True
```

### 调整 AI Prompt

编辑 `analyzers/ai_ranker.py`：

```python
def score_relevance(self, videos, topic, target_count):
    prompt = f"""
    你的自定义 prompt...
    评分标准：
    1. ...
    2. ...
    """
```

### 添加新的输出格式

在 `agent.py` 中添加：

```python
def export_to_markdown(videos):
    """导出为 Markdown 格式"""
    output = []
    for video in videos:
        output.append(f"## {video['title']}")
        output.append(f"- Author: {video['author']}")
        output.append(f"- Views: {video['views']:,}")
        output.append(f"- URL: {video['url']}")
        output.append("")
    return "\n".join(output)
```

## 测试

### 运行单元测试

每个模块都有内置测试：

```bash
# 测试 YouTube 获取器
python -m video_agent.fetchers.youtube

# 测试 Instagram 获取器
python -m video_agent.fetchers.instagram

# 测试规则筛选器
python -m video_agent.analyzers.rule_filter

# 测试 AI 排序器
python -m video_agent.analyzers.ai_ranker

# 测试缓存
python -m video_agent.cache
```

### 集成测试

```bash
# 运行完整搜索
python main.py "测试主题"

# 运行示例
python examples.py
```

## 调试技巧

### 启用详细日志

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 检查中间结果

在 `agent.py` 中添加断点：

```python
# 在规则筛选后
filtered_videos = self.rule_filter.filter(...)
import json
print(json.dumps(filtered_videos[0], indent=2, ensure_ascii=False))
```

### 监控 API 调用

记录每次 API 调用：

```python
# 在 fetchers/youtube.py
logger.info(f"API调用: search.list, 配额消耗: 100")
```

## 性能优化

### 并行处理

当前已实现平台并行获取，可进一步优化：

```python
# 异步处理
import asyncio

async def fetch_all():
    tasks = [
        fetch_youtube(),
        fetch_instagram(),
        fetch_tiktok()
    ]
    return await asyncio.gather(*tasks)
```

### 减少 token 使用

```python
# 截断描述
video['description'][:150]  # 只用前150字符
```

### 数据库索引

如果缓存表很大，添加索引：

```sql
CREATE INDEX idx_expires_at ON video_cache(expires_at);
```

## 故障排查

### 常见问题

1. **YouTube API 配额不足**
   - 减少 `MAX_RESULTS_PER_PLATFORM`
   - 启用缓存
   - 等到第二天（配额重置）

2. **Instagram 限流**
   - 增加请求间隔
   - 使用登录
   - 考虑使用代理

3. **Gemini API 超时**
   - 减少批处理大小
   - 添加重试逻辑
   - 使用降级策略

4. **缓存问题**
   - 清理过期缓存：`agent.cache.clear_expired()`
   - 删除数据库文件重新开始

## 部署建议

### 环境变量

生产环境使用环境变量而非 .env 文件：

```bash
export GEMINI_API_KEY="..."
export YOUTUBE_API_KEY="..."
```

### 日志管理

使用 logging 配置文件：

```python
import logging.config
logging.config.fileConfig('logging.conf')
```

### 监控

添加性能监控：

```python
import time

start = time.time()
results = agent.search(topic)
duration = time.time() - start

# 记录到监控系统
log_metrics({
    'duration': duration,
    'results_count': len(results),
    'cache_hit': cache_hit
})
```

## 贡献指南

### 代码规范

- 使用 PEP 8 风格
- 添加类型注解
- 编写 docstring
- 保持函数简短（< 50 行）

### 提交规范

```bash
git commit -m "feat: 添加 TikTok 支持"
git commit -m "fix: 修复 Instagram 登录问题"
git commit -m "docs: 更新 API 文档"
```

### Pull Request

1. Fork 项目
2. 创建功能分支
3. 编写测试
4. 提交 PR

## 许可证

MIT License - 详见 LICENSE 文件

## 联系方式

- Issue: 提交到 GitHub Issues
- Email: your-email@example.com

---

**Happy Coding!** 🚀

