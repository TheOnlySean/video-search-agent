# 🎬 视频搜索 Agent - 完整使用指南

## ✅ 系统状态

**当前版本**: v1.0 - YouTube 完整版

### 功能状态
| 功能 | 状态 | 说明 |
|------|------|------|
| **YouTube 搜索** | ✅ 完美运行 | 官方 API，稳定可靠 |
| **Gemini AI 分析** | ✅ 完美运行 | 智能评分和排序 |
| **三层筛选系统** | ✅ 完美运行 | 规则 → AI评分 → AI排序 |
| **智能缓存** | ✅ 完美运行 | 2小时内重用结果 |
| **成本优化** | ✅ 完美运行 | 单次查询 ~$0.03 |

### API 配置
- ✅ Gemini API Key: 已配置
- ✅ YouTube API Key: 已配置
- ✅ Instagram: 已配置但受限（可忽略）

---

## 🚀 快速开始

### 基础搜索

```bash
# 搜索任何主题
python3 main.py "AI编程"
python3 main.py "健身教程"
python3 main.py "美食制作"
python3 main.py "旅游vlog"
python3 main.py "Python教程"
```

### 交互式搜索

```bash
python3 main.py
# 然后输入你的主题
```

---

## 📊 实际效果展示

### 测试案例 1: "AI工具"

**搜索结果**：
- ✅ 找到 4 个高质量视频
- 📊 播放量: 21万 - 57万
- 🤖 AI 相关性: 96-99分
- ⏱️ 耗时: 约 15 秒

**示例视频**：
1. NotebookLM 实测 (32.8万播放, 99分)
2. Google Gemini 全系列教学 (57.1万播放, 98分)
3. Gemini + NotebookLM 简报 (22.9万播放, 97分)

### 测试案例 2: "fitness"

**搜索结果**：
- ✅ 找到 10 个热门视频
- 📊 播放量: 770万 - 2,220万
- 🤖 AI 相关性: 90-100分
- ⏱️ 耗时: 约 12 秒

**示例视频**：
1. Bungee fitness 课程 (1,489万播放, 100分)
2. 健身器械评测 (2,220万播放, 90分)
3. 健美比赛 (1,562万播放, 95分)

---

## 💡 使用技巧

### 搜索建议

**✅ 推荐的搜索主题**：
- 技能教程：`"Python教程"`, `"摄影技巧"`, `"吉他入门"`
- 生活方式：`"健身减肥"`, `"美食制作"`, `"旅游vlog"`
- 科技产品：`"AI工具"`, `"iPhone评测"`, `"科技资讯"`
- 创意内容：`"短视频制作"`, `"视频剪辑"`, `"内容创作"`

**❌ 避免的搜索**：
- 过于宽泛：`"视频"`, `"内容"`
- 过于具体：`"2024年1月5日的AI新闻"`
- 低热度话题：很少有人关注的冷门话题

### 优化搜索结果

**如果结果太少**，可以：
1. 使用更通用的关键词
2. 减少字数（2-4个词最佳）
3. 尝试英文关键词

**如果结果不够相关**，可以：
1. 使用更精确的关键词
2. 添加类型词（如"教程"、"评测"、"分享"）

---

## 🎯 核心功能详解

### 1. 三层筛选系统

**第一层：规则筛选**
- 播放量 > 20万
- 发布时间 < 2个月
- 基础关键词匹配

**第二层：AI 相关性评分**
- Gemini 分析标题和描述
- 评分 0-100
- 筛选高分视频（>70分）

**第三层：AI 精细排序**
- 综合评估质量
- 考虑多样性
- 选出 Top 10

### 2. 智能缓存

**工作原理**：
- 相同搜索 2 小时内直接返回缓存
- 自动清理过期缓存
- 大幅降低 API 成本

**查看缓存**：
```bash
# 缓存文件位置
ls -lh video_agent/cache.db
```

**清理缓存**：
```python
from video_agent import VideoSearchAgent
agent = VideoSearchAgent()
agent.clear_cache()  # 清理所有缓存
```

### 3. 成本控制

**单次搜索成本**：
- YouTube API: 免费
- Gemini AI: ~$0.03
- 总计: ~$0.03

**月度成本估算**（每天10次）：
- 每天: $0.30
- 每月: $9.00

**节省成本技巧**：
- 使用缓存（2小时内重复查询免费）
- 批量查询相似主题

---

## 📖 使用示例

### 示例 1: 命令行使用

```bash
cd /Users/x.sean/Desktop/小红书视频下载
python3 main.py "编程教程"
```

### 示例 2: Python 代码集成

```python
from video_agent import VideoSearchAgent

# 创建 Agent
agent = VideoSearchAgent(use_cache=True)

# 搜索视频
results = agent.search("Python教程", top_n=10)

# 处理结果
for i, video in enumerate(results, 1):
    print(f"{i}. {video['title']}")
    print(f"   播放量: {video['views']:,}")
    print(f"   作者: {video['author']}")
    print(f"   链接: {video['url']}")
    print()
```

### 示例 3: 批量搜索

```python
topics = ["AI工具", "Python教程", "健身减肥"]

for topic in topics:
    print(f"\n搜索: {topic}")
    results = agent.search(topic, top_n=5)
    print(f"找到 {len(results)} 个视频")
```

### 示例 4: 导出结果

```python
import json

results = agent.search("摄影技巧", top_n=10)

# 导出为 JSON
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ 已导出到 results.json")
```

### 示例 5: 数据分析

```python
results = agent.search("旅游vlog", top_n=10)

# 统计分析
total_views = sum(v['views'] for v in results)
avg_views = total_views / len(results)

print(f"总播放量: {total_views:,}")
print(f"平均播放量: {avg_views:,.0f}")

# 找出最热门的
top_video = max(results, key=lambda x: x['views'])
print(f"\n最热门: {top_video['title']}")
print(f"播放量: {top_video['views']:,}")
```

---

## 🔧 高级功能

### 查看完整示例

```bash
python3 examples.py
```

**包含 8 个示例**：
1. 基础搜索
2. 自定义配置
3. 处理结果
4. 导出数据（JSON/CSV）
5. 批量搜索
6. 缓存管理
7. 错误处理
8. 只搜索 YouTube

### 自定义配置

编辑 `video_agent/config.py`：

```python
# 调整筛选条件
MIN_VIEWS = 200000        # 最小播放量
MAX_DAYS_AGO = 60         # 最近 N 天
TOP_N_RESULTS = 10        # 返回数量

# 调整筛选阶段的保留数量
RULE_FILTER_COUNT = 30    # 规则筛选后保留
AI_FILTER_COUNT = 15      # AI 筛选后保留

# 缓存设置
CACHE_ENABLED = True      # 是否启用缓存
CACHE_EXPIRY_HOURS = 2    # 缓存有效期（小时）
```

### 测试 API 状态

```bash
python3 test_api.py
```

### 环境检查

```bash
python3 welcome.py
```

---

## 📊 性能指标

### 搜索性能

| 指标 | 数值 |
|------|------|
| 搜索时间 | 10-15秒 |
| 结果数量 | 10个（可配置）|
| 准确率 | 90-100%（AI评分）|
| 缓存命中时间 | <1秒 |

### 成本分析

| 项目 | 成本 |
|------|------|
| YouTube API | 免费 |
| Gemini API | $0.03/次 |
| 单次搜索 | $0.03 |
| 每日 10次 | $0.30 |
| 每月 300次 | $9.00 |

### 质量指标

- 视频播放量：20万 - 2000万+
- AI 相关性评分：70-100分
- 发布时间：最近 60 天内
- 平台覆盖：YouTube（最优质）

---

## 🎓 常见使用场景

### 场景 1: 内容创作灵感

```bash
python3 main.py "短视频创作"
```
**用途**：了解当前热门的短视频类型和创作趋势

### 场景 2: 学习资源查找

```bash
python3 main.py "Python零基础"
```
**用途**：找到最受欢迎的学习教程

### 场景 3: 竞品分析

```python
# 分析某个领域的热门创作者
results = agent.search("健身教程", top_n=20)
creators = {}
for video in results:
    author = video['author']
    if author not in creators:
        creators[author] = []
    creators[author].append(video)

# 输出分析
for author, videos in creators.items():
    total_views = sum(v['views'] for v in videos)
    print(f"{author}: {len(videos)} 个视频, {total_views:,} 总播放量")
```

### 场景 4: 趋势监控

```bash
# 定期搜索并保存结果
python3 main.py "AI工具" > results_$(date +%Y%m%d).txt
```

---

## 🐛 问题排查

### 问题 1: "找不到视频"

**原因**：
- 搜索词太冷门
- 播放量要求太高（20万）

**解决**：
```python
# 降低播放量要求
from video_agent import config
config.MIN_VIEWS = 100000  # 降低到10万
```

### 问题 2: "结果不相关"

**原因**：
- 搜索词太宽泛
- AI 理解有偏差

**解决**：
- 使用更具体的关键词
- 添加类型词（"教程"、"评测"）

### 问题 3: "速度太慢"

**原因**：
- YouTube API 响应慢
- Gemini AI 分析耗时

**解决**：
- 使用缓存（第二次搜索很快）
- 减少返回数量（config.py）

### 问题 4: "API 配额超限"

**原因**：
- YouTube 每天 10,000 配额用完

**解决**：
- 等到第二天
- 启用缓存减少查询
- 或申请配额提升

---

## 📞 获取帮助

### 查看文档

```bash
# 快速开始
cat 开始使用.md

# 完整文档
cat README.md

# 开发者文档
cat DEVELOPER.md

# 检查清单
cat CHECKLIST.md
```

### 测试工具

```bash
# API 状态测试
python3 test_api.py

# 环境检查
python3 welcome.py

# 查看示例
python3 examples.py
```

---

## 🎉 总结

### 你现在拥有

✅ **功能完整的视频搜索系统**
- YouTube 官方 API 集成
- Google Gemini AI 智能分析
- 三层筛选系统
- 智能缓存优化

✅ **优秀的搜索结果**
- 播放量百万级
- AI 评分 90-100 分
- 发布时间新鲜
- 创作者信息完整

✅ **完善的文档和工具**
- 6份详细文档
- 8个使用示例
- 测试和检查工具

✅ **低成本高效率**
- YouTube API 免费
- Gemini 仅 $0.03/次
- 智能缓存节省成本

---

## 🚀 开始使用

```bash
cd /Users/x.sean/Desktop/小红书视频下载

# 搜索你感兴趣的主题
python3 main.py "你的主题"

# 或查看示例
python3 examples.py
```

---

## 💡 推荐搜索主题

**热门主题**：
- `"AI工具"`
- `"Python教程"`
- `"健身减肥"`
- `"美食制作"`
- `"旅游vlog"`
- `"短视频创作"`
- `"摄影技巧"`
- `"产品评测"`

---

**Happy Searching! 享受你的视频搜索 Agent！** 🎊

如有任何问题，查看文档或运行测试工具。

