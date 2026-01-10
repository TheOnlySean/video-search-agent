# 🚀 Streamlit Cloud 部署教程（5分钟完成）

## 📋 准备工作

### 1. 确保你有以下账号

- ✅ **GitHub 账号**（免费）：https://github.com/
- ✅ **Streamlit Cloud 账号**（免费）：https://share.streamlit.io/

如果没有，请先注册（都是免费的）。

---

## 🎯 部署步骤

### 步骤 1: 将代码推送到 GitHub

#### 1.1 初始化 Git 仓库（如果还没有）

```bash
cd /Users/x.sean/Desktop/小红书视频下载

# 初始化 git
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit: Video Search Agent with Streamlit"
```

#### 1.2 创建 GitHub 仓库

1. 访问：https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `video-search-agent` （或其他名字）
   - **Description**: Video Search Agent - AI-powered video discovery tool
   - **Visibility**: Private（推荐，团队内部使用）
3. 点击 **"Create repository"**

#### 1.3 推送代码到 GitHub

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/video-search-agent.git

# 推送代码
git branch -M main
git push -u origin main
```

**提示**: 如果推送失败，可能需要配置 GitHub 认证（Personal Access Token）。

---

### 步骤 2: 部署到 Streamlit Cloud

#### 2.1 登录 Streamlit Cloud

1. 访问：https://share.streamlit.io/
2. 点击 **"Sign in with GitHub"**
3. 授权 Streamlit 访问你的 GitHub

#### 2.2 创建新应用

1. 点击 **"New app"** 按钮
2. 选择部署配置：
   - **Repository**: 选择你刚创建的仓库（`video-search-agent`）
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. 点击 **"Advanced settings"**（可选，建议设置）

#### 2.3 配置环境变量（重要！）

在 "Advanced settings" 中，找到 **"Secrets"** 部分，添加以下内容：

```toml
GEMINI_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
YOUTUBE_API_KEY = "AIzaSyCB10ltHbZpsc0AW6rAtsg1VgsEcbZPBAY"
```

**注意**: 
- 格式必须是 TOML 格式
- 每个 key = "value" 一行
- 不要包含额外的引号或空格

#### 2.4 部署

1. 点击 **"Deploy!"** 按钮
2. 等待 2-3 分钟，Streamlit 会自动：
   - 安装依赖（requirements.txt）
   - 启动应用
   - 分配一个公共 URL

#### 2.5 获取访问地址

部署成功后，你会得到一个公共 URL，类似：

```
https://video-search-agent.streamlit.app
```

或

```
https://your-username-video-search-agent-app-xyz123.streamlit.app
```

---

## ✅ 完成！分享给团队

现在你的团队成员可以通过这个 URL 访问应用了！

### 分享方式

发送给团队成员：

```
🎬 视频搜索 Agent 已上线！

访问地址：https://your-app.streamlit.app

使用方法：
1. 输入搜索主题（建议使用英文，如 "social media marketing"）
2. 调整筛选条件（左侧边栏）
3. 点击搜索按钮
4. 查看 AI 推荐的热门视频

推荐搜索主题：
- social media marketing
- content creation tips
- viral video strategy
- YouTube growth
```

---

## 🔒 设置访问权限（可选）

如果你的仓库是 Private，只有你授权的人才能访问应用。

### 管理访问权限

1. 在 Streamlit Cloud 的应用设置中
2. 找到 **"Sharing"** 部分
3. 可以：
   - 设为 Public（任何人都可访问）
   - 设为 Private（需要登录才能访问）
   - 添加特定的邮箱地址（白名单）

---

## 🔄 更新应用

当你修改代码后，只需：

```bash
# 提交更改
git add .
git commit -m "Update features"
git push

# Streamlit Cloud 会自动检测并重新部署（约 2 分钟）
```

---

## 🐛 常见问题

### Q1: 部署失败，显示 "ModuleNotFoundError"

**原因**: requirements.txt 可能不完整

**解决**: 检查 requirements.txt 文件，确保包含所有依赖

### Q2: 应用启动但显示 API 错误

**原因**: Secrets 配置不正确

**解决**:
1. 在 Streamlit Cloud 应用页面
2. 点击 Settings → Secrets
3. 检查 API Keys 格式是否正确
4. 保存后点击 "Reboot app"

### Q3: 推送到 GitHub 失败，要求身份验证

**解决**:
1. 访问：https://github.com/settings/tokens
2. 生成 Personal Access Token
3. 使用 token 作为密码推送

或使用 SSH：
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/video-search-agent.git
```

### Q4: 想要自定义域名

Streamlit Cloud 免费版不支持自定义域名，但你可以：
- 使用付费版（$20/月）
- 使用短链接服务（bit.ly）

---

## 💰 费用说明

### Streamlit Cloud
- ✅ **完全免费**（Community Plan）
- ✅ 无限制的公共应用
- ✅ 1 个私有应用
- ✅ 自动 HTTPS
- ✅ 自动更新

### API 调用费用
- YouTube API: 免费（10,000 配额/天）
- Gemini API: ~$0.03/次搜索

### 总成本
- **托管**: $0
- **使用**: $0.03/次搜索
- **团队（10人）**: 约 $5-10/月

---

## 📱 移动端访问

部署后，你的应用自动支持移动端：
- 手机浏览器访问同样的 URL
- 界面自动适配手机屏幕
- 所有功能在手机上都能正常使用

---

## 🎉 部署完成检查清单

- [ ] 代码已推送到 GitHub
- [ ] Streamlit Cloud 已连接 GitHub
- [ ] Secrets 已正确配置（API Keys）
- [ ] 应用已成功部署
- [ ] 获得公共访问 URL
- [ ] 在浏览器中测试应用
- [ ] 分享 URL 给团队成员
- [ ] 团队成员确认可以访问

---

## 🆘 需要帮助？

如果遇到问题：
1. 查看 Streamlit Cloud 的部署日志
2. 检查 GitHub Actions（如果有）
3. 参考官方文档：https://docs.streamlit.io/streamlit-community-cloud

---

## 🎊 恭喜！

你的应用现在可以被全球访问了！团队成员只需要：
1. 打开浏览器
2. 访问你分享的 URL
3. 开始搜索视频

**无需安装任何软件！** 🚀

