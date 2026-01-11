import streamlit as st
import sys
import os
from datetime import datetime
import json
import pandas as pd
from pathlib import Path
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from video_agent import VideoSearchAgent, format_results

# 页面配置
st.set_page_config(
    page_title="绝对情报局 - 视频搜索 Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'DISCOVER'  # DISCOVER, ANALYZE, REPORT

# 自定义 CSS - 参考同事项目的深色专业风格
st.markdown("""
<style>
    /* 深色主题 */
    :root {
        --primary: #dc2626;  /* red-600 */
        --secondary: #1e293b;  /* slate-900 */
        --accent: #10b981;  /* emerald-500 */
    }
    
    /* 主容器 */
    .stApp {
        background: #0f172a;  /* slate-950 */
    }
    
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 卡片样式 */
    .video-card {
        background: white;
        border-radius: 2rem;
        padding: 2rem;
        margin: 1rem 0;
        border: 4px solid #e2e8f0;
        transition: all 0.3s;
    }
    
    .video-card:hover {
        border-color: rgba(220, 38, 38, 0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: white !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -0.05em;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: #dc2626 !important;
        color: white !important;
        border: none !important;
        border-radius: 9999px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: black !important;
        transform: scale(1.05);
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* 指标卡片 */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    /* 进度条 */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        margin: 0 0.5rem;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .step.active {
        background: #dc2626;
        border-color: #dc2626;
    }
</style>
""", unsafe_allow_html=True)

# ===== 侧边栏 =====
with st.sidebar:
    # Logo 和标题
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem;">
        <div style="width: 80px; height: 80px; background: #dc2626; border-radius: 2rem; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 1rem; font-size: 3rem; font-weight: 900; color: white;">
            🎯
        </div>
        <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 900;">绝对情报局</h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 0.5rem 0;">
            INTELLIGENCE BUREAU
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 统计信息
    st.markdown("### 📊 情报统计")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("搜索次数", len(st.session_state.search_history))
    with col2:
        total_videos = sum(len(h['results']) for h in st.session_state.search_history if 'results' in h)
        st.metric("发现视频", total_videos)
    
    st.markdown("---")
    
    # 搜索历史
    st.markdown("### 🕐 搜索历史")
    
    if st.session_state.search_history:
        for i, history in enumerate(reversed(st.session_state.search_history[-5:])):
            with st.expander(f"🔍 {history['query'][:20]}...", expanded=False):
                st.write(f"时间: {history['timestamp']}")
                st.write(f"结果: {len(history.get('results', []))} 个视频")
                if st.button(f"重新加载 #{len(st.session_state.search_history)-i}", key=f"reload_{i}"):
                    st.session_state.current_results = history.get('results', [])
                    st.rerun()
    else:
        st.info("暂无搜索历史")
    
    st.markdown("---")
    
    # 系统信息
    st.markdown("### ⚙️ 系统信息")
    st.markdown(f"""
    - **版本**: v2.0 Enhanced
    - **数据源**: YouTube Data API
    - **AI 模型**: Gemini 2.5 Flash
    - **最后更新**: 2026-01-11
    """)

# ===== 主内容区 =====
# 步骤指示器
st.markdown("""
<div class="step-indicator">
    <div class="step {}" style="{}">
        <div style="font-size: 2rem;">🔍</div>
        <div style="font-weight: bold; margin-top: 0.5rem;">DISCOVER</div>
        <div style="font-size: 0.75rem; opacity: 0.7;">搜索目标</div>
    </div>
    <div class="step {}" style="{}">
        <div style="font-size: 2rem;">📊</div>
        <div style="font-weight: bold; margin-top: 0.5rem;">ANALYZE</div>
        <div style="font-size: 0.75rem; opacity: 0.7;">AI 分析</div>
    </div>
    <div class="step {}" style="{}">
        <div style="font-size: 2rem;">📄</div>
        <div style="font-weight: bold; margin-top: 0.5rem;">REPORT</div>
        <div style="font-size: 0.75rem; opacity: 0.7;">情报报告</div>
    </div>
</div>
""".format(
    'active' if st.session_state.current_step == 'DISCOVER' else '',
    'color: white;' if st.session_state.current_step == 'DISCOVER' else '',
    'active' if st.session_state.current_step == 'ANALYZE' else '',
    'color: white;' if st.session_state.current_step == 'ANALYZE' else '',
    'active' if st.session_state.current_step == 'REPORT' else '',
    'color: white;' if st.session_state.current_step == 'REPORT' else ''
), unsafe_allow_html=True)

# 标题和搜索框
st.markdown("""
<div style="text-align: center; padding: 3rem 1rem;">
    <h1 style="font-size: 4rem; margin: 0;">🎯 绝对情报局</h1>
    <p style="color: rgba(255,255,255,0.7); font-size: 1.25rem; margin-top: 1rem;">
        AI 驱动的多平台情报嗅探 Agent · 专注欧美爆款视频分析
    </p>
</div>
""", unsafe_allow_html=True)

# 搜索区域
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    search_query = st.text_input(
        "",
        placeholder="🎯 设定目标赛道（支持中文，如：AI工具、数字营销、自媒体运营）",
        key="search_input",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        search_button = st.button("🚀 启动全网嗅探", use_container_width=True, type="primary")

# 初始化 Agent
if 'agent' not in st.session_state:
    with st.spinner("⚡ 初始化 AI Agent..."):
        st.session_state.agent = VideoSearchAgent(use_cache=True)

# 执行搜索
if search_button and search_query:
    st.session_state.current_step = 'DISCOVER'
    
    with st.spinner(f"🔍 正在全网嗅探「{search_query}」相关情报..."):
        # 显示搜索进度
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("⏳ 连接 YouTube Data API...")
        progress_bar.progress(20)
        
        status_text.text("🔎 正在筛选欧美区爆款视频...")
        progress_bar.progress(50)
        
        results = st.session_state.agent.search(search_query, top_n=10)
        
        status_text.text("🤖 AI 正在深度解析...")
        progress_bar.progress(80)
        
        st.session_state.current_results = results
        st.session_state.current_step = 'REPORT'
        
        # 保存到历史
        st.session_state.search_history.append({
            'query': search_query,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'results': results
        })
        
        progress_bar.progress(100)
        status_text.text("✅ 情报获取完成！")
        
        st.balloons()
        st.rerun()

# 显示结果
if st.session_state.current_results:
    results = st.session_state.current_results
    
    # 操作栏
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"### 🎯 发现 {len(results)} 个高价值目标")
    
    with col2:
        sort_option = st.selectbox(
            "排序",
            ["AI 推荐", "播放量", "发布时间", "可复制性"],
            label_visibility="collapsed"
        )
    
    with col3:
        if st.button("📥 导出 CSV"):
            df = pd.DataFrame([{
                '标题': v['title'],
                '作者': v['author'],
                '播放量': v['views'],
                '发布时间': f"{v['days_ago']}天前",
                '链接': v['url'],
                '核心吸引点': v.get('hookText', ''),
                '可复制性': v.get('replicabilityScore', ''),
                '关键学习点': v.get('keyLearningPoints', ''),
                '成功原因': v.get('reasonForSuccess', '')
            } for v in results])
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "⬇️ 下载",
                csv,
                f"情报_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv",
                key='download-csv'
            )
    
    with col4:
        if st.button("📄 生成 PDF 报告"):
            st.info("PDF 导出功能开发中...")
    
    st.markdown("---")
    
    # 显示视频卡片
    for idx, video in enumerate(results, 1):
        # 创建卡片容器
        with st.container():
            st.markdown(f"""
            <div class="video-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <span style="background: #1e293b; color: white; padding: 0.25rem 0.75rem; 
                                     border-radius: 9999px; font-size: 0.75rem; font-weight: bold;">
                            #{idx} TARGET
                        </span>
                        <span style="background: #dc2626; color: white; padding: 0.25rem 0.75rem; 
                                     border-radius: 9999px; font-size: 0.75rem; font-weight: bold; margin-left: 0.5rem;">
                            {video['platform']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.75rem; color: #64748b; font-weight: bold;">
                            热度指数
                        </div>
                        <div style="font-size: 2rem; font-weight: 900; color: #dc2626;">
                            {video.get('ai_score', 'N/A')}
                        </div>
                    </div>
                </div>
                
                <h3 style="color: #1e293b; font-size: 1.5rem; font-weight: 900; 
                           margin: 1rem 0; line-height: 1.3; letter-spacing: -0.025em;">
                    {video['title']}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 详细信息
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**👤 情报来源**: [{video['author']}]({video['author_url']})")
                st.markdown(f"**📅 发布时间**: {video['days_ago']} 天前")
                st.markdown(f"**👁️ 曝光量**: {video['views']:,} 次")
                
                # 新增深度分析维度
                if video.get('hookText'):
                    st.markdown(f"**🎣 核心吸引点**: {video['hookText']}")
                
                if video.get('keyLearningPoints'):
                    st.success(f"**💡 关键学习点**: {video['keyLearningPoints']}")
                
                if video.get('reasonForSuccess'):
                    st.info(f"**⭐ 成功原因**: {video['reasonForSuccess']}")
            
            with col2:
                # 可复制性评分
                if video.get('replicabilityScore'):
                    score = video['replicabilityScore']
                    color = "#10b981" if score >= 7 else ("#f59e0b" if score >= 4 else "#ef4444")
                    emoji = "🟢" if score >= 7 else ("🟡" if score >= 4 else "🔴")
                    
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border: 2px solid rgba(255,255,255,0.1); 
                                border-radius: 1.5rem; padding: 1.5rem; text-align: center;">
                        <div style="font-size: 0.75rem; color: #94a3b8; font-weight: bold; 
                                    text-transform: uppercase; margin-bottom: 0.5rem;">
                            可复制性评分
                        </div>
                        <div style="font-size: 3rem; font-weight: 900; color: {color};">
                            {emoji} {score}/10
                        </div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.5rem;">
                            {'极易复制' if score >= 7 else ('中等难度' if score >= 4 else '较难复制')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 操作按钮
                st.markdown("<br>", unsafe_allow_html=True)
                st.link_button("🎬 观看视频", video['url'], use_container_width=True)
                st.link_button("👤 访问主页", video['author_url'], use_container_width=True)
            
            st.markdown("---")

else:
    # 空状态 - 引导用户搜索
    st.markdown("""
    <div style="text-align: center; padding: 6rem 2rem; max-width: 800px; margin: 0 auto;">
        <div style="font-size: 6rem; opacity: 0.3; margin-bottom: 2rem;">
            🎯
        </div>
        <h2 style="color: white; font-size: 3rem; margin-bottom: 1rem;">
            情报等待启动
        </h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.25rem; line-height: 1.8;">
            设定目标赛道，AI Agent 将穿透多平台 (TikTok/Instagram/YouTube)，
            嗅探最具可复制性的英语区自媒体大咖爆款视频，拆解高阶运营逻辑与变现策略。
        </p>
        
        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 3rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.1); padding: 0.75rem 1.5rem; 
                         border-radius: 9999px; font-weight: bold; color: white;">
                #AI工具
            </span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.75rem 1.5rem; 
                         border-radius: 9999px; font-weight: bold; color: white;">
                #数字营销
            </span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.75rem 1.5rem; 
                         border-radius: 9999px; font-weight: bold; color: white;">
                #高颜值生活
            </span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.75rem 1.5rem; 
                         border-radius: 9999px; font-weight: bold; color: white;">
                #语言学习
            </span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.75rem 1.5rem; 
                         border-radius: 9999px; font-weight: bold; color: white;">
                #短剧剪辑
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 2rem;">
    <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">
        Powered by YouTube API + Google Gemini AI
    </p>
    <p style="font-size: 0.75rem;">
        🎯 绝对情报局 v2.0 (Enhanced AI Analysis) | 最后更新: 2026-01-11
    </p>
    <p style="font-size: 0.7rem; opacity: 0.6; margin-top: 1rem;">
        INTERNAL USE ONLY // ABSOLUTE INTELLIGENCE BUREAU
    </p>
</div>
""", unsafe_allow_html=True)

