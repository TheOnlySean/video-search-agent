# 视频搜索 Agent - Streamlit 部署指南

## 🚀 本地运行

### 1. 安装依赖

```bash
cd /Users/x.sean/Desktop/小红书视频下载
pip install -r requirements.txt
```

### 2. 配置环境变量

确保 `.env` 文件已配置：
```env
GEMINI_API_KEY=your_key
YOUTUBE_API_KEY=your_key
```

### 3. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开：http://localhost:8501

---

## 🌐 部署到 Streamlit Cloud（免费）

### 优点
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 自动更新
- ✅ 适合团队内部使用（<10人）

### 部署步骤

#### 1. 准备 GitHub 仓库

```bash
cd /Users/x.sean/Desktop/小红书视频下载

# 初始化 git（如果还没有）
git init
git add .
git commit -m "Add Streamlit web app"

# 推送到 GitHub
git remote add origin https://github.com/your-username/video-search-agent.git
git push -u origin main
```

#### 2. 部署到 Streamlit Cloud

1. 访问：https://share.streamlit.io/
2. 点击 "New app"
3. 连接你的 GitHub 账号
4. 选择仓库和分支
5. 主文件路径：`app.py`
6. 点击 "Deploy"

#### 3. 配置环境变量（重要）

在 Streamlit Cloud 的部署页面：
1. 点击 "Settings" → "Secrets"
2. 添加以下内容：

```toml
GEMINI_API_KEY = "your_gemini_key"
YOUTUBE_API_KEY = "your_youtube_key"
```

3. 保存并重新部署

### 访问地址

部署完成后，你会得到一个链接：
```
https://your-app-name.streamlit.app
```

---

## 🏠 其他部署选项

### 方案 2: Render（免费）

**优点**：
- 免费托管
- 支持环境变量
- 自动 HTTPS

**步骤**：
1. 访问：https://render.com/
2. 创建 "Web Service"
3. 连接 GitHub 仓库
4. 设置启动命令：`streamlit run app.py --server.port=$PORT`
5. 添加环境变量

**限制**：
- 免费版会在 15 分钟不活动后休眠
- 第一次访问需要等待唤醒（~30秒）

### 方案 3: Railway（免费额度）

**优点**：
- $5 免费额度/月
- 不会休眠
- 速度快

**步骤**：
1. 访问：https://railway.app/
2. 连接 GitHub 仓库
3. 自动检测 Python 项目
4. 添加环境变量
5. 部署

---

## 💰 成本对比

| 平台 | 成本 | 稳定性 | 推荐度 |
|------|------|--------|--------|
| **Streamlit Cloud** | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Render** | 免费（会休眠） | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Railway** | $5/月额度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Heroku** | $7/月 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**推荐**：Streamlit Cloud（免费且完美适合内部使用）

---

## 🔒 安全建议

### 1. 添加密码保护（可选）

在 `app.py` 开头添加：

```python
import streamlit as st

def check_password():
    """返回 True 如果用户输入了正确的密码"""
    
    def password_entered():
        if st.session_state["password"] == "your_team_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        st.text_input(
            "请输入密码", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "请输入密码", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 密码错误")
        return False
    else:
        return True

# 在主程序开始前检查
if not check_password():
    st.stop()
```

### 2. 限制访问（Streamlit Cloud）

在 Streamlit Cloud 设置中：
- 设置为 "Private"
- 只有授权的 email 可以访问

---

## 📱 移动端适配

界面已自动适配移动端，在手机上也能完美使用！

---

## 🐛 问题排查

### 问题 1: "ModuleNotFoundError"

```bash
# 重新安装依赖
pip install -r requirements.txt
```

### 问题 2: "API Key 错误"

检查 `.env` 文件或 Streamlit Cloud 的 Secrets 配置

### 问题 3: "应用加载慢"

第一次运行会初始化 Agent，需要几秒钟

---

## 🎨 自定义样式

如果想修改颜色和样式，编辑 `app.py` 中的 CSS 部分。

---

## 📞 获取帮助

- Streamlit 文档：https://docs.streamlit.io/
- 部署指南：https://docs.streamlit.io/streamlit-community-cloud/get-started

---

**推荐部署方式**：Streamlit Cloud（完全免费，最简单）

