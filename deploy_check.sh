#!/bin/bash

echo "🚀 准备部署到 Streamlit Cloud"
echo "=============================="
echo ""

# 检查是否有 GitHub 远程仓库
if git remote | grep -q origin; then
    echo "✅ 已配置 GitHub 远程仓库"
    git remote -v
else
    echo "⚠️  尚未配置 GitHub 远程仓库"
    echo ""
    echo "请按以下步骤操作："
    echo ""
    echo "1. 访问 https://github.com/new 创建新仓库"
    echo "2. 仓库名称建议：video-search-agent"
    echo "3. 设置为 Private（团队内部使用）"
    echo "4. 创建后，运行以下命令（替换 YOUR_USERNAME）："
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/video-search-agent.git"
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "📝 下一步："
echo "1. 确保代码已推送到 GitHub"
echo "2. 访问 https://share.streamlit.io/"
echo "3. 点击 'Sign in with GitHub'"
echo "4. 点击 'New app' 创建应用"
echo "5. 选择你的仓库和 app.py"
echo "6. 在 Secrets 中添加 API Keys"
echo ""
echo "详细步骤请查看: STREAMLIT_DEPLOY.md"

