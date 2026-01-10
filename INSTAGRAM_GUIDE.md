# Instagram 搜索功能说明

## 📊 当前状态

### ✅ 功能已实现
- Instagram Reels 搜索代码已完成
- 使用 `instaloader` 库
- 支持话题标签搜索
- 支持登录和未登录两种模式

### ⚠️ 当前限制
由于 Instagram 的反爬虫机制，未登录状态下可能遇到：
- 404 错误（话题不存在或无法访问）
- 访问频率限制
- IP 限制

---

## 🔧 解决方案

### 方案 1: 添加 Instagram 登录（推荐）✅

编辑 `.env` 文件，添加你的 Instagram 账号：

```env
INSTAGRAM_USERNAME=你的Instagram用户名
INSTAGRAM_PASSWORD=你的Instagram密码
```

**建议使用小号！**

#### 测试登录：
```bash
python3 << 'EOF'
import instaloader
L = instaloader.Instaloader()
L.login('你的用户名', '你的密码')
print("✅ 登录成功！")
EOF
```

### 方案 2: 使用其他搜索方式

#### A. Instagram Graph API（官方，但限制多）
- 需要 Business 账号
- 需要应用审核
- 只能搜索自己的内容

#### B. RapidAPI Instagram API（付费服务）
- $10-30/月
- 更稳定
- 更少限制

#### C. 暂时只用 YouTube（当前推荐）
YouTube 搜索已经很强大了，建议先用：
```bash
python3 main.py "你的主题"
```

---

## 🎯 Instagram 使用建议

### 适合搜索的话题
✅ 英文常用标签：
- #fitness
- #cooking
- #travel
- #photography
- #coding

❌ 避免：
- 中文标签（可能不存在）
- 生僻话题
- 过于具体的关键词

### 搜索技巧

1. **使用流行标签**
   ```python
   agent.search("fitness", top_n=10)  # ✅ 好
   agent.search("健身", top_n=10)    # ❌ 可能失败
   ```

2. **降低期望**
   - Instagram Reels 的播放量通常比 YouTube 低
   - 可能找不到 20 万播放的视频
   - 可以调整最小播放量要求

3. **添加登录**
   - 大幅提高成功率
   - 减少被限制的可能
   - 使用小号测试

---

## 🔍 当前系统能力对比

| 平台 | 状态 | 说明 |
|------|------|------|
| **YouTube** | ✅ 完全可用 | 官方API，稳定可靠 |
| **Instagram** | ⚠️ 需要登录 | 未登录容易被限制 |
| **TikTok** | 🔄 未实现 | 可扩展 |

---

## 💡 推荐使用方式

### 当前最佳实践

1. **主要使用 YouTube**
   ```bash
   python3 main.py "AI编程"
   ```
   - 搜索结果质量高
   - API 稳定
   - 完全免费

2. **如果需要 Instagram**
   - 添加登录信息到 `.env`
   - 使用英文标签
   - 降低最小播放量要求

3. **调整配置**（如果需要）
   编辑 `video_agent/config.py`：
   ```python
   MIN_VIEWS = 100000  # 降低到10万
   ```

---

## 🧪 测试 Instagram（如果添加了登录）

### 测试脚本：
```python
from video_agent.fetchers import InstagramFetcher

# 使用你的登录信息
fetcher = InstagramFetcher(
    username='你的用户名',
    password='你的密码'
)

# 搜索流行话题
videos = fetcher.search_videos(
    topic='fitness',
    max_results=5,
    min_views=50000  # 降低要求
)

print(f"找到 {len(videos)} 个视频")
for v in videos:
    print(f"- {v['title'][:50]}... ({v['views']:,} 播放)")
```

---

## 📝 总结

### 现在可以做的：
✅ 使用 YouTube 搜索（完全正常）
✅ Gemini AI 分析（完全正常）
✅ 查看代码和示例

### 如果想用 Instagram：
1. 添加 Instagram 登录到 `.env`
2. 使用英文话题标签
3. 降低播放量要求（50K-100K）

### 最简单的方式：
**先用 YouTube！效果已经很好了！**

```bash
python3 main.py "你的主题"
```

---

## 🎯 下一步

选择你想要的方式：

### A. 继续使用 YouTube（推荐）
```bash
python3 main.py "AI工具"
python3 main.py "编程教程"
```

### B. 添加 Instagram 支持
1. 准备一个 Instagram 小号
2. 添加到 `.env` 文件
3. 测试搜索英文话题

### C. 暂时跳过 Instagram
- YouTube 已经很强大
- 未来可以随时添加
- 或者等 TikTok 支持

---

**建议：先用 YouTube，效果已经非常好了！** 🚀

