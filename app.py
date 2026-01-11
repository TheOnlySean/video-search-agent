import streamlit as st
import sys
import os
from datetime import datetime
import json
import pandas as pd
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from video_agent import VideoSearchAgent, format_results

# 页面配置
st.set_page_config(
    page_title="视频搜索 Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS - 毛玻璃风格
st.markdown("""
<style>
    /* 主题色 */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 毛玻璃效果 */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 主容器背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 标题样式 */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* 搜索框样式 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 12px 20px;
        font-size: 1.1rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* 视频卡片 */
    .video-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: all 0.3s ease;
    }
    
    .video-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.25);
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* 数据框样式 */
    .dataframe {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
    }
    
    /* 进度条 */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 信息框 */
    .stAlert {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'agent' not in st.session_state:
    st.session_state.agent = None

# 标题
st.markdown('<h1 class="main-title">🎬 视频搜索 Agent</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 3rem;">发现全球热门视频，AI 驱动的智能推荐</p>', unsafe_allow_html=True)

# 侧边栏 - 高级选项
with st.sidebar:
    st.markdown("### ⚙️ 高级设置")
    
    # 筛选选项
    min_views = st.number_input(
        "最小播放量",
        min_value=10000,
        max_value=10000000,
        value=200000,
        step=50000,
        help="只显示播放量大于此值的视频"
    )
    
    max_results = st.slider(
        "结果数量",
        min_value=5,
        max_value=20,
        value=10,
        help="返回的视频数量"
    )
    
    max_days = st.slider(
        "最近天数",
        min_value=7,
        max_value=180,
        value=60,
        help="只显示最近N天内发布的视频"
    )
    
    use_cache = st.checkbox("使用缓存", value=True, help="启用后，相同搜索会使用缓存结果")
    
    st.markdown("---")
    
    # 排序选项
    st.markdown("### 📊 排序方式")
    sort_by = st.radio(
        "排序依据",
        ["AI 推荐", "播放量", "发布时间"],
        help="选择结果的排序方式"
    )
    
    st.markdown("---")
    
    # 搜索历史
    st.markdown("### 📝 搜索历史")
    if st.session_state.search_history:
        for i, item in enumerate(reversed(st.session_state.search_history[-5:])):
            if st.button(f"🔍 {item['query']}", key=f"history_{i}"):
                st.session_state.search_query = item['query']
                st.rerun()
    else:
        st.info("暂无搜索历史")
    
    if st.session_state.search_history:
        if st.button("🗑️ 清空历史"):
            st.session_state.search_history = []
            st.rerun()

# 主搜索区域
col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    search_query = st.text_input(
        "",
        placeholder="输入搜索主题（支持中文，会自动翻译。如：自媒体运营 / social media marketing）",
        key="search_input",
        label_visibility="collapsed"
    )
    
    search_button = st.button("🔍 搜索视频", use_container_width=True, type="primary")

# 搜索建议
with st.expander("💡 搜索建议"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**自媒体运营**")
        suggestions_1 = [
            "social media marketing",
            "content creation tips",
            "YouTube strategy",
            "viral video tips"
        ]
        for sug in suggestions_1:
            if st.button(sug, key=f"sug1_{sug}"):
                st.session_state.search_query = sug
                st.rerun()
    
    with col2:
        st.markdown("**技能教程**")
        suggestions_2 = [
            "video editing tutorial",
            "photography tips",
            "music production",
            "design tutorial"
        ]
        for sug in suggestions_2:
            if st.button(sug, key=f"sug2_{sug}"):
                st.session_state.search_query = sug
                st.rerun()
    
    with col3:
        st.markdown("**热门话题**")
        suggestions_3 = [
            "AI tools",
            "fitness workout",
            "travel vlog",
            "cooking recipe"
        ]
        for sug in suggestions_3:
            if st.button(sug, key=f"sug3_{sug}"):
                st.session_state.search_query = sug
                st.rerun()

# 执行搜索
if search_button and search_query:
    # 初始化 Agent
    if st.session_state.agent is None:
        with st.spinner("初始化搜索引擎..."):
            try:
                # 临时修改配置
                from video_agent import config
                config.MIN_VIEWS = min_views
                config.MAX_DAYS_AGO = max_days
                
                st.session_state.agent = VideoSearchAgent(use_cache=use_cache)
                st.success("✅ 搜索引擎初始化成功！")
            except Exception as e:
                st.error(f"❌ 初始化失败: {e}")
                st.stop()
    
    # 检测中文并提示翻译
    import re
    is_chinese = bool(re.search(r'[\u4e00-\u9fff]', search_query))
    
    # 执行搜索
    search_text = f"🔍 正在搜索「{search_query}」..."
    if is_chinese:
        search_text = f"🌐 检测到中文输入，正在翻译并搜索「{search_query}」..."
    
    with st.spinner(search_text):
        try:
            results = st.session_state.agent.search(search_query, top_n=max_results)
            
            if results:
                st.session_state.current_results = results
                
                # 添加到搜索历史
                st.session_state.search_history.append({
                    'query': search_query,
                    'timestamp': datetime.now().isoformat(),
                    'count': len(results)
                })
                
                # 显示翻译信息（如果是中文）
                if is_chinese:
                    st.info(f"💡 已自动将中文翻译为英文进行搜索，以获取欧美热门内容")
                
                st.success(f"✅ 找到 {len(results)} 个视频！")
            else:
                st.warning("😕 未找到符合条件的视频，请尝试其他关键词或降低筛选条件")
                
        except Exception as e:
            st.error(f"❌ 搜索失败: {e}")

# 显示结果
if st.session_state.current_results:
    results = st.session_state.current_results
    
    # 应用排序
    if sort_by == "播放量":
        results = sorted(results, key=lambda x: x['views'], reverse=True)
    elif sort_by == "发布时间":
        results = sorted(results, key=lambda x: x['days_ago'])
    # AI 推荐已经是默认排序
    
    # 统计信息
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("视频数量", len(results))
    with col2:
        total_views = sum(v['views'] for v in results)
        st.metric("总播放量", f"{total_views:,.0f}")
    with col3:
        avg_views = total_views / len(results) if results else 0
        st.metric("平均播放量", f"{avg_views:,.0f}")
    with col4:
        avg_score = sum(v.get('ai_score', 0) for v in results) / len(results) if results else 0
        st.metric("平均相关性", f"{avg_score:.0f}分")
    
    # 导出功能
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # 导出 JSON
        json_data = json.dumps(results, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 导出 JSON",
            data=json_data,
            file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # 导出 CSV
        df = pd.DataFrame([{
            '平台': v['platform'],
            '标题': v['title'],
            '作者': v['author'],
            '播放量': v['views'],
            '发布天数': v['days_ago'],
            '视频链接': v['url'],
            '作者主页': v['author_url']
        } for v in results])
        
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 导出 CSV",
            data=csv_data,
            file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # 显示视频列表
    st.markdown("---")
    st.markdown("## 🎥 搜索结果")
    
    for i, video in enumerate(results, 1):
        with st.container():
            # 视频卡片
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # 缩略图
                if video.get('thumbnail'):
                    st.image(video['thumbnail'], use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/320x180?text=Video", use_column_width=True)
            
            with col2:
                # 视频信息
                st.markdown(f"### {i}. {video['title'][:80]}{'...' if len(video['title']) > 80 else ''}")
                
                # 标签
                tags_html = f"""
                <div style="margin: 8px 0;">
                    <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                 color: white; padding: 4px 12px; border-radius: 12px; 
                                 font-size: 0.9rem; margin-right: 8px;">
                        {video['platform']}
                    </span>
                    <span style="background: rgba(102, 126, 234, 0.1); color: #667eea; 
                                 padding: 4px 12px; border-radius: 12px; font-size: 0.9rem;">
                        📊 {video['views']:,} 播放
                    </span>
                """
                
                if video.get('ai_score'):
                    tags_html += f"""
                    <span style="background: rgba(118, 75, 162, 0.1); color: #764ba2; 
                                 padding: 4px 12px; border-radius: 12px; font-size: 0.9rem; 
                                 margin-left: 8px;">
                        🤖 {video['ai_score']}分
                    </span>
                    """
                
                tags_html += "</div>"
                st.markdown(tags_html, unsafe_allow_html=True)
                
                # 作者和时间
                st.markdown(f"👤 **作者**: [{video['author']}]({video['author_url']})")
                st.markdown(f"📅 **发布**: {video['days_ago']} 天前")
                
                # 钩子文本（如果有）
                if video.get('hookText'):
                    st.markdown(f"🎣 **核心吸引点**: {video['hookText']}")
                
                # 可复制性评分（如果有）
                if video.get('replicabilityScore'):
                    score = video['replicabilityScore']
                    emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
                    st.markdown(f"♻️ **可复制性**: {emoji} {score}/10 分")
                
                # 关键学习点（如果有）
                if video.get('keyLearningPoints'):
                    st.success(f"💡 **关键学习点**: {video['keyLearningPoints']}")
                
                # 成功原因（如果有）
                if video.get('reasonForSuccess'):
                    st.info(f"⭐ **成功原因**: {video['reasonForSuccess']}")
                
                # 推荐理由（如果有，但不重复显示）
                elif video.get('recommendation_reason'):
                    st.info(f"💬 **推荐理由**: {video['recommendation_reason']}")
                
                # 操作按钮
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                
                with col_btn1:
                    st.link_button("🎬 观看视频", video['url'], use_container_width=True)
                
                with col_btn2:
                    st.link_button("👤 访问主页", video['author_url'], use_container_width=True)
            
            st.markdown("---")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Powered by YouTube API + Google Gemini AI
    </p>
    <p style="font-size: 0.8rem; opacity: 0.6;">
        🎬 视频搜索 Agent - 发现全球优质内容
    </p>
    <p style="font-size: 0.7rem; opacity: 0.5;">
        版本: v2.0 (Enhanced AI Analysis) | 最后更新: 2026-01-11
    </p>
</div>
""", unsafe_allow_html=True)

