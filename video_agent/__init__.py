"""
Video Search Agent - 智能视频搜索助手
"""
__version__ = '1.0.0'
__author__ = 'Video Agent Team'

from .agent import VideoSearchAgent, format_results
from .config import validate_config

__all__ = ['VideoSearchAgent', 'format_results', 'validate_config']

