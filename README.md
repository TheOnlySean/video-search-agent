# 视频搜索 Agent 🎬

一个智能视频搜索助手，可以帮你在 **YouTube** 和 **Instagram** 上找到最热门、最相关的视频内容。

## ✨ 功能特点

- 🔍 **多平台搜索**：同时搜索 YouTube 和 Instagram
- 🤖 **AI 智能分析**：使用 Google Gemini 进行内容相关性分析
- 📊 **精准筛选**：
  - 播放量 > 20万
  - 发布时间 < 2个月
  - AI 相关性评分
- 💾 **智能缓存**：避免重复查询，节省成本
- ⚡ **并行处理**：快速获取多平台数据
- 💰 **成本优化**：单次查询约 $0.03

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Keys

复制配置模板并填入你的 API keys：

```bash
cp env_template.txt .env
```

编辑 `.env` 文件，填入以下内容：

```env
# Google Gemini API Key
# 获取地址: https://ai.google.dev/
GEMINI_API_KEY=你的_gemini_api_key

# YouTube Data API v3 Key
# 获取地址: https://console.cloud.google.com/
YOUTUBE_API_KEY=你的_youtube_api_key

# Instagram 登录（可选，不填也能用但可能有限制）
INSTAGRAM_USERNAME=你的instagram用户名
INSTAGRAM_PASSWORD=你的instagram密码

# 缓存配置
CACHE_ENABLED=true
CACHE_EXPIRY_HOURS=2
```

### 3. 运行搜索

```bash
# 方式1：命令行参数
python main.py "AI编程工具"

# 方式2：交互式
python main.py
# 然后输入主题
```

## 📋 API Keys 获取指南

### Google Gemini API

1. 访问 https://ai.google.dev/
2. 点击 "Get API Key"
3. 登录 Google 账号
4. 创建新项目或选择现有项目
5. 复制 API Key

**免费额度**：每分钟 60 次请求，足够个人使用

### YouTube Data API v3

1. 访问 https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用 "YouTube Data API v3"
4. 创建凭据 → API 密钥
5. 复制 API Key

**免费额度**：每天 10,000 配额单位

### Instagram（可选）

- **不登录**：可以搜索，但可能遇到限流
- **登录**：提供你的 Instagram 账号信息，减少限制
- **建议**：使用小号测试

## 💡 使用示例

### 基础搜索

```python
from video_agent import VideoSearchAgent

# 初始化 Agent
agent = VideoSearchAgent(use_cache=True)

# 搜索视频
results = agent.search("健身减肥", top_n=10)

# 查看结果
for video in results:
    print(f"{video['title']} - {video['views']:,} 播放量")
```

### 导出结果

```bash
python main.py "AI编程"
# 搜索完成后选择导出为 JSON
```

### 清理缓存

```python
# 清理特定主题
agent.clear_cache("AI编程")

# 清理所有缓存
agent.clear_cache()
```

## 📊 工作流程

```
用户输入主题
    ↓
【步骤1】并行获取数据 (5-10秒)
├─ YouTube API: 50个候选视频
└─ Instagram: 50个候选视频
    ↓
【步骤2】规则筛选 (1秒)
├─ 播放量 > 20万
├─ 2个月内发布
├─ 基础关键词匹配
└─ 保留 ~30个
    ↓
【步骤3】AI相关性评分 (3秒, $0.01)
├─ Gemini分析标题+描述
├─ 相关性评分 (0-100)
└─ 保留 ~15个高分视频
    ↓
【步骤4】AI精细排序 (2秒, $0.02)
├─ 综合评估质量
├─ 平台平衡
└─ 输出 Top 10
    ↓
【结果】
├─ 总耗时: 10-15秒
└─ 总成本: ~$0.03
```

## 🏗️ 项目结构

```
video_agent/
├── fetchers/           # 数据获取模块
│   ├── youtube.py      # YouTube API
│   └── instagram.py    # Instagram 爬虫
├── analyzers/          # 分析模块
│   ├── rule_filter.py  # 规则筛选
│   └── ai_ranker.py    # AI排序
├── config.py           # 配置管理
├── cache.py            # 缓存管理
└── agent.py            # 主程序

main.py                 # 入口文件
requirements.txt        # 依赖列表
.env                    # API配置（需自己创建）
```

## ⚙️ 配置说明

在 `video_agent/config.py` 中可以调整：

```python
# 搜索配置
MAX_RESULTS_PER_PLATFORM = 50  # 每个平台获取的候选数
MIN_VIEWS = 200000             # 最小播放量
MAX_DAYS_AGO = 60              # 最近N天内的视频
TOP_N_RESULTS = 10             # 最终返回数量

# 缓存配置
CACHE_ENABLED = True           # 是否启用缓存
CACHE_EXPIRY_HOURS = 2         # 缓存有效期（小时）
```

## 🧪 测试模块

每个模块都可以独立测试：

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

## 💰 成本说明

### Gemini API

- **单次搜索**：~$0.03
- **每天10次**：~$0.30
- **每月**：~$9

### YouTube API

- **完全免费**（配额限制内）
- 每天 10,000 配额单位
- 单次搜索消耗 ~100 单位
- 每天可查询 ~100 次

### Instagram

- **免费**（使用开源库）
- 注意频率限制

## 🔧 常见问题

### Q1: Instagram 登录失败？

**A**: Instagram 的反爬虫机制较严格，可能需要：
- 使用小号
- 降低请求频率
- 考虑使用代理

### Q2: YouTube API 配额不够？

**A**: 
- 减少 `MAX_RESULTS_PER_PLATFORM`
- 启用缓存减少重复查询
- 考虑申请配额提升

### Q3: Gemini API 调用失败？

**A**:
- 检查 API Key 是否正确
- 确认账号是否有额度
- 查看错误日志了解具体原因

### Q4: 搜索结果太少？

**A**:
- 降低 `MIN_VIEWS` 阈值
- 增加 `MAX_DAYS_AGO` 时间范围
- 调整搜索关键词

## 📈 未来计划

- [ ] 添加 TikTok 支持
- [ ] Web 界面 (Streamlit)
- [ ] 视频内容深度分析
- [ ] 创作者画像分析
- [ ] 趋势预测功能
- [ ] 定期监控和推送

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 支持

如有问题，请提交 Issue 或联系开发者。

---

**快速开始命令**：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Keys
cp env_template.txt .env
# 编辑 .env 文件

# 3. 开始搜索
python main.py "你的主题"
```

Happy Searching! 🎉
