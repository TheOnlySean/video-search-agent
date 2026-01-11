# 🚨 立即更新 API Key - 详细步骤（带截图说明）

## 📍 你现在需要做的（5分钟）

### 步骤 1：打开 Streamlit Cloud

1. **点击这个链接**：https://share.streamlit.io/
2. **登录**你的账号

---

### 步骤 2：找到你的应用

在应用列表中找到：**video-search-agent**

如果找不到，说明你可能用了不同的账号部署，请确认。

---

### 步骤 3：进入设置

1. 点击应用右下角的 **"⋮"** (三个点) 或 **"Manage app"**
2. 在左侧菜单中，点击 **"⚙️ Settings"**

---

### 步骤 4：更新 Secrets（最关键！）

1. 在 Settings 页面，找到 **"Secrets"** 标签页
2. 你会看到一个文本编辑框
3. **删除所有旧内容**
4. **复制下面这段文本**：

```toml
GEMINI_API_KEY = "AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0"
YOUTUBE_API_KEY = "AIzaSyAVYeFP0jyEJLWiW38ploY0vs8i2GjiSi0"
```

5. **粘贴到编辑框**
6. **点击 "Save"** 按钮（非常重要！）

---

### 步骤 5：重启应用

1. 点击右上角的 **"⋮"** (三个点)
2. 选择 **"Reboot app"**
3. 等待应用重启（大约 30 秒 - 2 分钟）

---

### 步骤 6：验证部署

1. 在 **Manage app** 页面，点击 **"Logs"**
2. 滚动到最底部
3. 查看是否有：
   - ✅ `App is live at: https://...` - 部署成功
   - ❌ 红色错误信息 - 有问题（截图发给我）

---

### 步骤 7：测试新功能

1. **清除浏览器缓存**：
   - Windows: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

2. **访问应用**：https://video-search-agent-smfrxp96bjth8s4bh7zyj7.streamlit.app/

3. **搜索一个新的关键词**（不要用之前搜索过的）：
   - ✅ "youtube growth"
   - ✅ "content creation tips"
   - ✅ "自媒体运营"

4. **检查结果**，应该看到每个视频下方有：
   ```
   🎣 核心吸引点: xxxxx
   ♻️ 可复制性: 🟢 8/10 分
   💡 关键学习点: xxx,xxx,xxx
   ⭐ 成功原因: xxxxxxxxx
   ```

---

## ⚠️ 常见问题

### Q1: 找不到 "Secrets" 标签
**A**: 确保你点击的是左侧的 "Settings"，不是其他菜单

### Q2: 保存后还是不工作
**A**: 
1. 检查是否真的点击了 "Save"
2. 手动 "Reboot app"
3. 等待 2-3 分钟
4. 强制刷新浏览器

### Q3: 看到的还是旧结果
**A**: 这是**缓存**！请：
1. 搜索一个**全新的关键词**（从未搜索过的）
2. 或者在左侧边栏取消勾选 "启用缓存"

---

## 🆘 如果还是不行

请运行本地测试：

```bash
cd /Users/x.sean/Desktop/小红书视频下载
python3 demo_ui.py
```

如果本地能看到新功能，说明：
- ✅ 代码没问题
- ❌ Streamlit Cloud 的 API Key 或部署有问题

然后告诉我：
1. 本地测试的结果
2. Streamlit Cloud Logs 的最后 20 行（截图）

---

**现在就去操作，5分钟后告诉我结果！** 🚀

