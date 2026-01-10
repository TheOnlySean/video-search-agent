# ✅ 使用前检查清单

在开始使用视频搜索 Agent 之前，请完成以下检查：

## 📋 准备工作

### 1. 系统要求
- [ ] Python 3.7 或更高版本
- [ ] pip 已安装
- [ ] 网络连接正常

检查 Python 版本：
```bash
python --version  # 或 python3 --version
```

### 2. 安装依赖

- [ ] 进入项目目录
```bash
cd /Users/x.sean/Desktop/小红书视频下载
```

- [ ] 安装所有依赖
```bash
pip install -r requirements.txt
```

预期输出：成功安装 5 个包
- `google-api-python-client`
- `google-generativeai`
- `instaloader`
- `python-dotenv`
- `requests`

### 3. API Keys 准备

#### Gemini API Key（必需）⭐
- [ ] 访问 https://ai.google.dev/
- [ ] 登录 Google 账号
- [ ] 创建 API Key
- [ ] 复制 Key（格式类似：`AIzaSy...`）

#### YouTube Data API Key（必需）⭐
- [ ] 访问 https://console.cloud.google.com/
- [ ] 创建或选择项目
- [ ] 启用 "YouTube Data API v3"
- [ ] 创建 API Key
- [ ] 复制 Key

#### Instagram 账号（可选）
- [ ] 准备 Instagram 用户名
- [ ] 准备 Instagram 密码
- [ ] （建议使用小号）

### 4. 配置文件

- [ ] 复制模板文件
```bash
cp env_template.txt .env
```

- [ ] 编辑 `.env` 文件
```bash
# 使用任意文本编辑器打开
nano .env
# 或
vim .env
# 或使用图形界面编辑器
```

- [ ] 填入以下内容：
```env
GEMINI_API_KEY=你的_gemini_key
YOUTUBE_API_KEY=你的_youtube_key
INSTAGRAM_USERNAME=你的instagram用户名（可选）
INSTAGRAM_PASSWORD=你的instagram密码（可选）
CACHE_ENABLED=true
CACHE_EXPIRY_HOURS=2
```

- [ ] 保存文件

### 5. 验证配置

运行配置验证：
```bash
python -c "from video_agent import config; config.validate_config(); print('✅ 配置验证成功')"
```

预期输出：`✅ 配置验证成功`

如果出错，检查：
- `.env` 文件是否在正确位置
- API Keys 是否正确复制（无多余空格）
- API Keys 是否有效

## 🧪 测试运行

### 测试 1: YouTube 获取器
```bash
python -m video_agent.fetchers.youtube
```

预期输出：
```
✅ 找到 X 个视频：
1. [视频标题]
   播放量: XXX
   ...
```

### 测试 2: Instagram 获取器
```bash
python -m video_agent.fetchers.instagram
```

预期输出：
```
✅ 找到 X 个视频：
1. [视频标题]
   ...
```

### 测试 3: AI 排序器
```bash
python -m video_agent.analyzers.ai_ranker
```

预期输出：
```
✅ AI 评分完成
```

### 测试 4: 完整搜索
```bash
python main.py "测试"
```

预期流程：
1. 显示 "开始搜索"
2. 获取各平台数据
3. 规则筛选
4. AI 分析
5. 显示结果

## ✅ 检查清单总结

在运行正式搜索前，确保以下都已完成：

- [ ] ✅ Python 环境正常
- [ ] ✅ 依赖已安装
- [ ] ✅ Gemini API Key 已配置
- [ ] ✅ YouTube API Key 已配置
- [ ] ✅ `.env` 文件创建并配置正确
- [ ] ✅ 配置验证通过
- [ ] ✅ 至少一个测试通过

## 🚀 准备就绪！

如果所有检查都通过，你可以开始使用了：

```bash
# 快速搜索
python main.py "你的主题"

# 查看示例
python examples.py

# 查看帮助
python main.py --help
```

## ❌ 常见问题

### 问题 1: 找不到模块

**错误**：`ModuleNotFoundError: No module named 'xxx'`

**解决**：
```bash
pip install -r requirements.txt --upgrade
```

### 问题 2: API Key 无效

**错误**：`配置错误: 请设置 GEMINI_API_KEY`

**解决**：
1. 确认 `.env` 文件存在
2. 检查 API Key 是否正确
3. 确保没有多余的引号或空格

### 问题 3: YouTube API 配额不足

**错误**：`YouTube API quota exceeded`

**解决**：
- 等到第二天（配额每天重置）
- 或者暂时只使用 Instagram

### 问题 4: Instagram 限流

**警告**：`Instagram rate limit`

**解决**：
- 添加登录信息到 `.env`
- 减少搜索频率
- 等待几分钟后重试

## 📞 需要帮助？

- 查看 `README.md` - 完整文档
- 查看 `QUICKSTART.md` - 快速开始指南
- 查看 `DEVELOPER.md` - 开发者文档
- 运行 `python examples.py` - 查看示例

---

**准备好了吗？开始搜索吧！** 🎉

```bash
python main.py "你感兴趣的主题"
```

