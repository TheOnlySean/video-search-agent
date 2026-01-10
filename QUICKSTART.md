# 快速开始指南

## 第一次使用？跟着这个步骤走！

### 步骤 1: 获取 API Keys

#### 1.1 获取 Gemini API Key (必需)

1. 打开浏览器，访问：https://ai.google.dev/
2. 点击右上角 "Get API Key" 或 "Get started"
3. 登录你的 Google 账号
4. 点击 "Create API Key"
5. 选择一个项目或创建新项目
6. 复制生成的 API Key（类似：AIzaSy...）

**免费额度**：每分钟 60 次请求，完全够用！

#### 1.2 获取 YouTube API Key (必需)

1. 访问：https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 在左侧菜单点击 "APIs & Services" → "Library"
4. 搜索 "YouTube Data API v3"
5. 点击 "Enable"（启用）
6. 返回 "APIs & Services" → "Credentials"
7. 点击 "Create Credentials" → "API Key"
8. 复制生成的 API Key

**免费额度**：每天 10,000 配额，相当于 100 次搜索！

#### 1.3 Instagram 账号（可选）

- 如果你有 Instagram 账号，可以登录获得更好的效果
- 没有也没关系，不登录也能用（但可能遇到限制）
- **建议**：使用小号测试，避免主号被限制

### 步骤 2: 安装项目

打开终端（Terminal），执行以下命令：

```bash
# 进入项目目录
cd /Users/x.sean/Desktop/小红书视频下载

# 安装依赖
pip install -r requirements.txt
```

等待安装完成（大约 1-2 分钟）。

### 步骤 3: 配置 API Keys

1. 在项目目录中找到 `env_template.txt` 文件
2. 复制并重命名为 `.env`：

```bash
cp env_template.txt .env
```

3. 用文本编辑器打开 `.env` 文件
4. 填入你的 API Keys：

```env
# 必填：Gemini API Key
GEMINI_API_KEY=你从步骤1.1获取的key

# 必填：YouTube API Key
YOUTUBE_API_KEY=你从步骤1.2获取的key

# 可选：Instagram 账号
INSTAGRAM_USERNAME=你的instagram用户名
INSTAGRAM_PASSWORD=你的instagram密码

# 保持默认即可
CACHE_ENABLED=true
CACHE_EXPIRY_HOURS=2
```

5. 保存文件

### 步骤 4: 运行测试

先测试一下各个模块是否正常：

```bash
# 测试 YouTube
python -m video_agent.fetchers.youtube

# 测试 Instagram
python -m video_agent.fetchers.instagram

# 测试 AI 分析
python -m video_agent.analyzers.ai_ranker
```

如果都显示成功，就可以开始使用了！

### 步骤 5: 开始搜索

```bash
# 搜索视频
python main.py "AI编程工具"
```

或者交互式使用：

```bash
python main.py
# 然后输入你想搜索的主题
```

## 示例搜索主题

- "AI编程工具"
- "健身减肥教程"
- "Python教程"
- "旅游vlog"
- "美食制作"
- "摄影技巧"

## 常见错误解决

### 错误 1: "请设置 GEMINI_API_KEY"

**原因**：API Key 未正确配置

**解决**：
1. 确认 `.env` 文件存在（不是 `env_template.txt`）
2. 检查 API Key 是否正确复制（没有多余空格）
3. 确保 `.env` 文件在项目根目录

### 错误 2: "YouTube API 配额不足"

**原因**：今天的免费配额用完了

**解决**：
1. 等到第二天（配额每天重置）
2. 或申请提升配额
3. 或使用缓存减少查询

### 错误 3: "Instagram 登录失败"

**原因**：Instagram 账号密码错误或被限制

**解决**：
1. 检查用户名和密码是否正确
2. 先不登录试试（删除 `.env` 中的 Instagram 配置）
3. 使用小号而不是主号

### 错误 4: "模块未找到"

**原因**：依赖未正确安装

**解决**：
```bash
pip install -r requirements.txt --upgrade
```

## 下一步

成功运行后，你可以：

1. **调整参数**：编辑 `video_agent/config.py` 调整筛选条件
2. **查看缓存**：检查 `video_agent/cache.db` 文件
3. **导出结果**：搜索完成后选择导出为 JSON
4. **集成到你的项目**：参考 `README.md` 中的 Python API 使用方法

## 需要帮助？

- 查看 `README.md` 了解更多功能
- 检查错误日志中的详细信息
- 提交 Issue 寻求帮助

祝你使用愉快！🎉

