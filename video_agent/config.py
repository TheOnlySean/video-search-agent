import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# 缓存配置
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', '2'))
CACHE_FILE = 'video_agent/cache.db'

# 搜索配置
MAX_RESULTS_PER_PLATFORM = 50  # 每个平台获取的候选视频数
MIN_VIEWS = 100000  # 最小播放量（降低到10万，提高通过率）
MAX_DAYS_AGO = 60  # 最近N天内的视频
TOP_N_RESULTS = 10  # 最终返回的视频数量

# 筛选配置
RULE_FILTER_COUNT = 30  # 规则筛选后保留的数量
AI_FILTER_COUNT = 15  # AI轻量筛选后保留的数量

# 验证配置
def validate_config():
    """验证必需的配置是否存在"""
    errors = []
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
        errors.append("请设置 GEMINI_API_KEY")
    
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == 'your_youtube_api_key_here':
        errors.append("请设置 YOUTUBE_API_KEY")
    
    if errors:
        raise ValueError(f"配置错误:\n" + "\n".join(f"- {e}" for e in errors))
    
    return True

