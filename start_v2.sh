#!/bin/bash
# 启动增强版 UI

cd "$(dirname "$0")"

echo "🎯 正在启动绝对情报局 v2.0..."
echo ""

streamlit run app_v2.py \
    --server.port=8501 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --theme.primaryColor="#dc2626" \
    --theme.backgroundColor="#0f172a" \
    --theme.secondaryBackgroundColor="#1e293b" \
    --theme.textColor="#ffffff"

