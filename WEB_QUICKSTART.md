# 🎬 视频搜索 Agent - Web 版快速入门

## ✅ 应用已启动！

你的 Web 应用现在可以访问了：

### 本地访问地址
- **主地址**: http://localhost:8501
- **局域网地址**: http://192.168.0.72:8501
- **外网地址**: http://113.149.215.193:8501

---

## 🎨 界面预览

你会看到一个**简洁现代的毛玻璃风格**界面：

```
┌─────────────────────────────────────────┐
│  🎬 视频搜索 Agent                       │
│  发现全球热门视频，AI 驱动的智能推荐     │
│  ─────────────────────────────────────  │
│                                         │
│  [搜索框]                               │
│  输入主题（建议使用英文）               │
│                                         │
│  💡 搜索建议                            │
│  - social media marketing              │
│  - content creation tips               │
│  - video editing tutorial              │
│  ...                                   │
│                                         │
│  📊 搜索结果（卡片展示）                │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🚀 如何使用

### 1. 打开浏览器

访问：http://localhost:8501

### 2. 输入搜索主题

**推荐英文搜索词（欧美博主）**：

**自媒体运营**：
- `social media marketing`
- `content creation tips`
- `YouTube growth strategy`
- `viral video tips`
- `Instagram marketing`
- `TikTok content ideas`
- `influencer marketing`
- `personal branding`

**视频制作**：
- `video editing tutorial`
- `filmmaking tips`
- `camera techniques`
- `storytelling for videos`

**其他热门**：
- `AI tools for creators`
- `passive income ideas`
- `productivity hacks`
- `fitness motivation`

### 3. 调整筛选条件（左侧边栏）

- **最小播放量**: 默认 200,000
- **结果数量**: 默认 10 个
- **最近天数**: 默认 60 天
- **排序方式**: AI 推荐 / 播放量 / 发布时间

### 4. 查看搜索结果

每个视频卡片会显示：
- 🎬 视频标题
- 👤 作者名称和主页链接
- 📊 播放量
- 🤖 AI 相关性评分
- 📅 发布时间
- 💡 推荐理由

### 5. 导出数据

点击页面上的按钮：
- **📥 导出 JSON** - 包含完整数据
- **📥 导出 CSV** - 适合 Excel 打开

---

## ⚙️ 高级功能

### 搜索历史

- 左侧边栏会自动记录最近 5 次搜索
- 点击历史记录可快速重新搜索

### 排序选项

- **AI 推荐**（默认）：综合评分最高的视频
- **播放量**：按播放量从高到低
- **发布时间**：按最新发布排序

### 缓存机制

- 相同搜索会使用缓存，速度更快，成本更低
- 可以在侧边栏关闭缓存

---

## 💰 使用成本

- **每次搜索**: ~$0.03
- **缓存命中**: $0
- **团队 10 人**: 每月估计 $5-10（假设每人每天搜索 2 次）

---

## 🔧 停止应用

在终端按 `Ctrl + C` 停止 Streamlit 服务器

---

## 🌐 部署到云端（推荐）

### 选项 1: Streamlit Cloud（免费）⭐⭐⭐⭐⭐

**优点**：
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 无需服务器
- ✅ 适合团队使用

**步骤**：
1. 将代码推送到 GitHub
2. 访问：https://share.streamlit.io/
3. 连接 GitHub 仓库
4. 配置环境变量（Secrets）
5. 一键部署

**详细步骤**：查看 [DEPLOYMENT.md](DEPLOYMENT.md)

### 选项 2: Render（免费，但会休眠）

- 免费版 15 分钟不活动后休眠
- 适合低频使用

### 选项 3: Railway（$5/月额度）

- 不会休眠
- 速度更快
- 稳定性更好

---

## 🎨 界面特点

### 毛玻璃风格设计
- 渐变紫色背景
- 半透明卡片
- 模糊效果
- 阴影和过渡动画

### 响应式布局
- 自动适配桌面和移动端
- 在手机上也能完美使用

### 现代交互
- 按钮悬停效果
- 卡片悬停放大
- 平滑过渡动画

---

## 📱 移动端使用

1. 使用局域网地址：http://192.168.0.72:8501
2. 在手机浏览器打开
3. 界面会自动适配手机屏幕

---

## 🐛 常见问题

### Q1: 搜索很慢？

第一次搜索需要初始化 AI Agent，需要 5-10 秒。后续搜索会快很多。

### Q2: 找不到视频？

- 尝试用英文搜索
- 降低最小播放量（如改为 100,000）
- 增加时间范围（如改为 90 天）

### Q3: API 错误？

检查 `.env` 文件中的 API Keys 是否正确配置。

### Q4: 想添加密码保护？

参考 [DEPLOYMENT.md](DEPLOYMENT.md) 中的"安全建议"部分。

---

## 🎉 开始使用吧！

**现在就打开浏览器访问**：
http://localhost:8501

搜索你的第一个主题，比如：
- `social media marketing`
- `content creation tips`
- `viral video strategy`

享受探索全球优质内容的乐趣！🚀

---

## 📞 获取帮助

- 查看完整文档：[DEPLOYMENT.md](DEPLOYMENT.md)
- Streamlit 官方文档：https://docs.streamlit.io/

---

**Powered by YouTube API + Google Gemini AI** 🎬✨

