#!/bin/bash

echo "🎬 视频搜索 Agent - Web 版"
echo "=========================="
echo ""
echo "正在启动 Streamlit 应用..."
echo ""

cd "$(dirname "$0")"

# 检查依赖
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit 未安装"
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  警告: .env 文件不存在"
    echo "请先配置 API Keys："
    echo "  GEMINI_API_KEY=your_key"
    echo "  YOUTUBE_API_KEY=your_key"
    exit 1
fi

# 启动应用
echo "✅ 启动成功！"
echo ""
echo "访问地址："
echo "  - 本地: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止应用"
echo ""

streamlit run app.py

