# 🎬 视频搜索 Agent - Web 版本

## 项目说明
基于 Streamlit 的视频搜索 Web 应用，支持搜索 YouTube 热门视频。

## 主要文件
- `app.py` - Streamlit 应用主文件
- `video_agent/` - 核心搜索引擎
- `.streamlit/config.toml` - Streamlit 配置

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量（创建 .env 文件）
GEMINI_API_KEY=your_key
YOUTUBE_API_KEY=your_key

# 3. 运行应用
streamlit run app.py
```

访问：http://localhost:8501

## 部署到 Streamlit Cloud（推荐）

完全免费，适合团队内部使用：
1. 推送代码到 GitHub
2. 访问 https://share.streamlit.io/
3. 连接仓库并配置环境变量
4. 一键部署

详细步骤见：[DEPLOYMENT.md](DEPLOYMENT.md)

## 功能特点

- ✅ 简洁现代的毛玻璃风格
- ✅ 智能搜索和 AI 排序
- ✅ 高级筛选和排序
- ✅ 搜索历史记录
- ✅ 导出 JSON/CSV
- ✅ 移动端适配

## 成本
- 托管：免费（Streamlit Cloud）
- API 调用：~$0.03/次搜索

## License
MIT

